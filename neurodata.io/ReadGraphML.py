
from pygraphml import GraphMLParser
from pygraphml import Graph
from neuromllite import *
import random

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

def read_graphml(filename, color_map=[]):
    parser = GraphMLParser()
    g = parser.parse(filename)
    
    g.set_root('n0')
    
    print dir(g)
    id = '%s_%s'%(filename.split('.')[0],filename.split('.')[1])
    net = Network(id=id)
    net.notes = "NeuroMLlite conversion of %s from https://www.neurodata.io/project/connectomes/"%filename
    #net.parameters = {}

    dummy_cell = Cell(id='testcell', pynn_cell='IF_cond_alpha')
    dummy_cell.parameters = { "tau_refrac":5, "i_offset":0 }
    net.cells.append(dummy_cell)

    net.synapses.append(Synapse(id='ampa', 
                                pynn_receptor_type='excitatory', 
                                pynn_synapse_type='cond_alpha', 
                                parameters={'e_rev':0, 'tau_syn':2}))

    for node in g.nodes():
        
        info = ''
        for a in node.attributes():
            info+=node.attr[a].value+'; '
        if len(info)>2: info = info[:-4]
            
        color = '%s %s %s'%(random.random(),random.random(),random.random()) \
                    if not info in color_map else color_map[info]
                    
        print('> Node: %s (%s), color: %s'%(node.id, info, color))
        p0 = Population(id=node.id, 
                        size=1, 
                        component=dummy_cell.id, 
                        properties={'color':color})

        net.populations.append(p0)
        
    for edge in g.edges():
        #print dir(edge)
        #print edge.attributes()
        src = edge.node1.id
        tgt = edge.node2.id
        weight = float(str(edge.attr['e_weight'].value)) if 'e_weight' in edge.attr else 1
        
        #print('>> Edge from %s -> %s, weight %s'%(src, tgt, weight))
        
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
    
    color_map = {'Cell body in EM volume; NA':'0.8 0 0',
                 'Characterized pyramidal neuron; NA':'0 0 0.8',
                 'Dendritic fragment; Postsynaptic inhibitory target':'0 0.8 0.8',
                 'Cell body in EM volume; Postsynaptic inhibitory target':'0.8 0.8 0',
                 'Dendritic fragment; Postsynaptic excitatory target': '0.5 0.5 0.2'}
                 
    read_graphml('mouse_visual.cortex_1.graphml',color_map)
    
    #read_graphml('mouse_visual.cortex_2.graphml',color_map)
    #read_graphml('mixed.species_brain_1.graphml')
