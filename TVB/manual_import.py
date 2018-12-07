
from neuromllite import *
import random
from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

id = 'Hagmannetal2008'

net = Network(id=id)
net.notes = "NeuroMLlite conversion of network from https://github.com/JohnGriffiths/temp_tvb_tutorials"

dummy_cell = Cell(id='testcell', pynn_cell='IF_cond_alpha')
dummy_cell.parameters = { "tau_refrac":5, "i_offset":0 }
net.cells.append(dummy_cell)

net.synapses.append(Synapse(id='ampa', 
                            pynn_receptor_type='excitatory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':0, 'tau_syn':2}))

  
            

f = open('connectivity_Hagmannetal2008_66/centres.txt')
for line in f:
    
    words = line.split()
    id = words[0]
    x,y,z = float(words[1]), float(words[2]), float(words[3])

    color = '%s %s %s'%(random.random(),random.random(),random.random())

    print('Imported: %s: (%s,%s,%s), color: %s'%(id,x,y,z, color))
    
    if 'IN' in id or True: 
        
        ll = SingleLocation()
        
        ll.location = Location(x=x,y=y,z=z)
        
        
        p0 = Population(id=id, 
                        size=1, 
                        component=dummy_cell.id, 
                        properties={'color':color})
                        
        p0.single_location=ll

        #exit()
        net.populations.append(p0)
    
print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)

duration=1000
dt = 0.1

sim = Simulation(id='Sim%s'%net.id,
                 network=new_file,
                 duration=duration,
                 dt=dt,
                 recordRates={'all':'*'})

check_to_generate_or_run(sys.argv, sim)
