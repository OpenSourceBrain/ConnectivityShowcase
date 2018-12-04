
from pygraphml import GraphMLParser
from pygraphml import Graph
from neuromllite import *
import random

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

def read_graphml(filename):
    parser = GraphMLParser()
    g = parser.parse(filename)
    
    g.set_root('n0')
    
    print dir(g)
    
    net = Network(id='%s'%filename.split('.')[0])
    net.notes = "...."
    #net.parameters = {}

    dummy_cell = Cell(id='testcell', pynn_cell='IF_cond_alpha')
    dummy_cell.parameters = { "tau_refrac":5, "i_offset":0 }
    net.cells.append(dummy_cell)

    net.synapses.append(Synapse(id='ampa', 
                                pynn_receptor_type='excitatory', 
                                pynn_synapse_type='cond_alpha', 
                                parameters={'e_rev':0, 'tau_syn':2}))

    for node in g.nodes():
        print('Node: %s '%(node))
        
        p0 = Population(id=node.id, 
                        size=1, 
                        component=dummy_cell.id, 
                        properties={'color':'%s %s %s'%(random.random(),random.random(),random.random())})

        net.populations.append(p0)
        
    for edge in g.edges():
        #print dir(edge)
        print edge.attributes()
        print edge.attr['e_weight']
        src = edge.node1.id
        tgt = edge.node2.id
        weight = float(str(edge.attr['e_weight'].value))
        print('>> Edge from %s -> %s, weight %s'%(src, tgt, weight))
        
        net.projections.append(Projection(id='proj_%s_%s'%(src,tgt),
                                          presynaptic=src, 
                                          postsynaptic=tgt,
                                          synapse='ampa',
                                          weight=weight,
                                          random_connectivity=RandomConnectivity(probability=1)))

    #g.show()
    
    #print(net)
    
    #print(net.to_json())
    new_file = net.to_json_file('%s.json'%net.id)
    
    duration=1000
    dt = 0.1
    
    sim = Simulation(id='Sim%s'%net.id,
                     network=new_file,
                     duration=duration,
                     dt=dt,
                     recordRates={'all':'*'})
    
    check_to_generate_or_run(sys.argv, sim)
    
    

if __name__ == '__main__':
    
    #read_graphml('mouse_visual.cortex_1.graphml')
    read_graphml('mouse_visual.cortex_2.graphml')
