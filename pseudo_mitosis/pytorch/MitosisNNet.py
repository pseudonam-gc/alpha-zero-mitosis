import sys
sys.path.append('..')
from utils import *

import argparse
import logging
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.nn import Linear, ReLU, Sequential as Seq
from torch_geometric.nn import GCNConv, NNConv
from torch_geometric.data import Data, Batch
from torch_geometric.nn import global_mean_pool

#logging.basicConfig(level=logging.NOTSET)
# set level to none
#logging.basicConfig(level=logging.ERROR)

class MitosisNNet(nn.Module):
    def __init__(self, game, args):
        # game params
        self.input_size = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.edge_index = game.getEdgeIndex()  
        self.edge_attr = game.getEdgeAttr()  # Edge attributes if needed, otherwise can be None 
        self.args = args

        super(MitosisNNet, self).__init__()
        #self.conv1 = GCNConv(1, args.num_channels)
        #self.conv2 = GCNConv(args.num_channels, args.num_channels)
        #self.conv3 = GCNConv(args.num_channels, args.num_channels)
        #self.c1_linear = nn.Linear(6, args.num_channels)
        #self.c2_linear = nn.Linear(6, args.num_channels * args.num_channels)
        #self.c3_linear = nn.Linear(6, args.num_channels * args.num_channels)
        lin_size = 16
        self.edge_mlp1 = Seq(Linear(6, lin_size), ReLU(), Linear(lin_size, args.num_channels * 1))
        self.conv1 = NNConv(1, args.num_channels, self.edge_mlp1, aggr='mean')

        self.edge_mlp2 = Seq(Linear(6, lin_size), ReLU(), Linear(lin_size, args.num_channels * args.num_channels))
        self.conv2 = NNConv(args.num_channels, args.num_channels, self.edge_mlp2, aggr='mean')

        self.edge_mlp3 = Seq(Linear(6, lin_size), ReLU(), Linear(lin_size, args.num_channels * args.num_channels))
        self.conv3 = NNConv(args.num_channels, args.num_channels, self.edge_mlp3, aggr='mean')

        self.bn1 = nn.BatchNorm1d(args.num_channels)
        self.bn2 = nn.BatchNorm1d(args.num_channels)
        self.bn3 = nn.BatchNorm1d(args.num_channels)
        
        self.fc1 = nn.Linear(args.num_channels, 1024)
        self.fc_bn1 = nn.BatchNorm1d(1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc_bn2 = nn.BatchNorm1d(512)
        self.fc3 = nn.Linear(512, self.action_size)
        self.fc4 = nn.Linear(512, 1)


    def forward(self, s):
        #logger = logging.getLogger(__name__)
        # s is (batch_size, 19) 
        if s.shape[0] > self.input_size:
            # then we have to batch unfortunately
            data_list = []
            for i in range(s.shape[0]):
                x = s[i].view(-1, 1)  
                data = Data(x=x, edge_index=self.edge_index, edge_attr=self.edge_attr)
                data_list.append(data)
            batch = Batch.from_data_list(data_list)
            x = batch.x
            edge_index = batch.edge_index
            edge_attr = batch.edge_attr
            batch_vector = batch.batch  # Get the batch vector
        else:
            x = s.view(-1, 1)  
            edge_index = self.edge_index
            edge_attr = self.edge_attr
            batch_vector = None
        # x is now (batch_size, 19, 1) tensor
        
        #logger.info("Input shape: %s", x.shape, "Edge_index: %s", edge_index.shape, "Edge_attr: %s", edge_attr.shape if edge_attr is not None else "None")
        # ERROR: argument input must be Tensor, not NoneType
        try:
            x = self.conv1(x, edge_index, edge_attr)  # Apply the first convolution layer
        except:
            print ("Input shape: ", x.shape, "Edge_index: ", edge_index.shape, "Edge_attr: ", edge_attr.shape if edge_attr is not None else "None")
        # The error is that edge_attr is NONE 
        # as it turns out Input shape:  torch.Size([2368, 1]) Edge_index:  torch.Size([2, 11520]) Edge_attr:  None
        # and notably batch.edge_attr is nonexistent
        #logger.info("Conv1 output shape: %s", x.shape)
        x = self.bn1(F.relu(x))
        #logger.info("BN1 output shape: %s", x.shape)
        x = self.conv2(x, edge_index, edge_attr)
        #logger.info("Conv2 output shape: %s", x.shape)
        x = self.bn2(F.relu(x))
        #logger.info("BN2 output shape: %s", x.shape)
        x = self.conv3(x, edge_index, edge_attr)
        #logger.info("Conv3 output shape: %s", x.shape)
        x = self.bn3(F.relu(x))
        #logger.info("BN3 output shape: %s", x.shape)


        x = global_mean_pool(x, batch_vector)  # Global mean pooling to aggregate node features
        
        x = F.dropout(F.relu(self.fc_bn1(self.fc1(x))), p=self.args.dropout, training=self.training)
        x = F.dropout(F.relu(self.fc_bn2(self.fc2(x))), p=self.args.dropout, training=self.training)
        pi = self.fc3(x)
        v = self.fc4(x)

        # display the model layers + sizes like model summary

        return F.log_softmax(pi, dim=1), torch.tanh(v) 
    
# TODO: test neural network on a toy example to learn a function
# example function: there is a thing surrounded by other thing
# very easy


