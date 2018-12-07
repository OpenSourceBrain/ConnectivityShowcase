
from neuromllite import *
import random
from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

id = 'Hagmannetal2008'

net = Network(id=id)
net.notes = "NeuroMLlite conversion of network from https://github.com/JohnGriffiths/temp_tvb_tutorials. "+ \
    "NOTE: clarification required on pre/post: https://github.com/JohnGriffiths/temp_tvb_tutorials/issues/1"

dummy_cell = Cell(id='testcell', pynn_cell='IF_cond_alpha')
dummy_cell.parameters = { "tau_refrac":5, "i_offset":0 }
net.cells.append(dummy_cell)

net.synapses.append(Synapse(id='ampa', 
                            pynn_receptor_type='excitatory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':0, 'tau_syn':2}))

  
regions = {}
region_colors = {}

f = open('Regions.txt')
for line in f:
    words = line.split()
    regions[words[0]] = ' '.join(words[1:])

populations = {}

f = open('connectivity_Hagmannetal2008_66/centres.txt')
i =0
for line in f:
    
    words = line.split()
    id = words[0]
    x,y,z = float(words[1])*1000, float(words[2])*1000, float(words[3])*1000
    region = regions[id[1:]]
    
    if region in region_colors:
        color = region_colors[region]
    else:
        color = '%s %s %s'%(random.random(),random.random(),random.random())
        region_colors[region] = color

    print('Imported: %s: (%s,%s,%s), color: %s'%(id,x,y,z, color))
    
    if 'IN' in id or True: 
        
        ll = SingleLocation()
        
        ll.location = Location(x=x,y=y,z=z)
        properties={'color':color, 'radius':5000}
        
        notes = '%s (%s)'%(region,'left' if id[0]=='l' else 'right')
        populations[i]=id
        i+=1
        p0 = Population(id=id, 
                        size=1, 
                        notes=notes,
                        component=dummy_cell.id, 
                        properties=properties)
                        
        p0.single_location=ll 

        #exit()
        net.populations.append(p0)
        
W = {}
f = open('connectivity_Hagmannetal2008_66/weights.txt')
i =0
for line in f:
    words = line.split()
    W[i] = {}
    for j in range(len(words)):
        W[i][j] = float(words[j])
        
    i+=1

    
for pre in W:
    for post in W[pre]:
        pre_pop = populations[pre]
        post_pop = populations[post]
        weight = W[pre][post]
        if weight>0:
            print("Connecting %s -> %s, %s, %s"%(pre_pop,post_pop, weight,weight>0))

            net.projections.append(Projection(id='proj_%s_%s'%(pre_pop,post_pop),
                                              presynaptic=pre_pop, 
                                              postsynaptic=post_pop,
                                              synapse='ampa',
                                              weight=weight,
                                              random_connectivity=RandomConnectivity(probability=1)))
    
    
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
