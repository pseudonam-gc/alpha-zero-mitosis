import sys
sys.path.append('..')
from utils import *

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data, Batch
from torch_geometric.nn import global_mean_pool

class MitosisNNet(nn.Module):
    def __init__(self, game, args):
        # game params
        self.input_size = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.edge_index = game.getEdgeIndex()  
        self.args = args

        super(MitosisNNet, self).__init__()
        self.conv1 = GCNConv(1, args.num_channels)
        self.conv2 = GCNConv(args.num_channels, args.num_channels)
        self.conv3 = GCNConv(args.num_channels, args.num_channels)

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
        # s is (batch_size, 19) 
        if s.shape[0] > self.input_size:
            # then we have to batch unfortunately
            data_list = []
            for i in range(s.shape[0]):
                x = s[i].view(-1, 1)  
                data = Data(x=x, edge_index=self.edge_index)
                data_list.append(data)
            batch = Batch.from_data_list(data_list)
            x = batch.x
            edge_index = batch.edge_index
            batch_vector = batch.batch  # Get the batch vector
        else:
            x = s.view(-1, 1)  
            edge_index = self.edge_index
            batch_vector = None
        # x is now (batch_size, 19, 1) tensor

        x = self.bn1(F.relu(self.conv1(x, edge_index)))  # Apply batch normalization and ReLU activation
        x = global_mean_pool(x, batch_vector)  # Global mean pooling to aggregate node features
        #x = self.bn2(F.relu(self.conv2(x, edge_index)))
        #x = self.bn3(F.relu(self.conv3(x, edge_index)))
        
        x = F.dropout(F.relu(self.fc_bn1(self.fc1(x))), p=self.args.dropout, training=self.training)
        x = F.dropout(F.relu(self.fc_bn2(self.fc2(x))), p=self.args.dropout, training=self.training)
        pi = self.fc3(x)
        v = self.fc4(x)

        # display the model layers + sizes like model summary

        return F.log_softmax(pi, dim=1), torch.tanh(v) 
    
# TODO: test neural network on a toy example to learn a function
# example function: there is a thing surrounded by other thing
# very easy


