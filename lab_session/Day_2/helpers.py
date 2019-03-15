def show_atoms(atoms,dis=True):
    import nglview
    v = nglview.show_ase(atoms)
    v.clear_representations()
    v.add_unitcell()
    v.camera='orthographic'
    v.add_spacefill(radius_type='vdw',radius_scale=0.5,
                    roughness=1,metalness=0)
    v.parameters = dict(clipDist=-100, sampleLevel=3)
    if dis:
        display(v)
    else:
        return v
    
def show_traj(traj,dis=True):
    # traj can be list of atoms
    import nglview
    v = nglview.show_asetraj(traj)
    v.clear_representations()
    # it seems that nglview traj cannot handle unit cell right now
    #v.add_unitcell()
    v.camera='orthographic'
    v.add_spacefill(radius_type='vdw',radius_scale=0.5,
                    roughness=1,metalness=0)
    v.parameters = dict(clipDist=-100, sampleLevel=3)
    if dis:
        display(v)
    else:
        return v



def show_dataset(dataset):
    
    import ipywidgets as widgets
    from ipywidgets import Layout,HBox,VBox
    import tensorflow as tf
    import nglview as nv
    from ase import Atoms
    import numpy as np
    items = dataset.make_one_shot_iterator().get_next()
    sess = tf.Session()
    
    def updata_view(v, item, c):
        if c:
            v.remove_component(c)
        n_atoms = np.count_nonzero(item['atoms'])
        a = Atoms(item['atoms'], positions=item['coord'])[:n_atoms]
        c = v.add_structure(nv.ASEStructure(a))
        c.clear()
        c.add_spacefill(radius_type='vdw',radius_scale=0.5,
                        roughness=1,metalness=0)
        v._remote_call('zoom', target='viewerControls', args=[-10,])
        return c
    
                        

    v = nv.NGLWidget()
    v.camera='orthographic'
    v._set_size('300px','300px')
    v.parameters = dict(clipDist=-100, sampleLevel=2)
    
    class FnScope:
        item_list = []
        i = 0
        c = None
        
    FnScope.item_list = [sess.run(items) for i in range(10)]
    FnScope.c = updata_view(v, FnScope.item_list[0], FnScope.c)
    p = widgets.Select(options=['Sample 1']+['{}: {:.6f}'.format(k,v) for k,v in 
                                FnScope.item_list[0].items()
                                if (k!='coord' and k!='atoms')],
                       layout=Layout(width='200px',height='270px'))
    
    b1 = widgets.Button(description='Prev',layout=Layout(width='98px'))
    b2 = widgets.Button(description='Next',layout=Layout(width='98px'))



    def on_prev(b):
        if FnScope.i == 0:
            return
        else:
            FnScope.i -= 1
            FnScope.c = updata_view(v, FnScope.item_list[FnScope.i], FnScope.c)
            p.options = ['Sample {}'.format(FnScope.i+1)] + ['{}: {:.6f}'.format(k,v) for k,v in 
                                FnScope.item_list[FnScope.i].items()
                                if (k!='coord' and k!='atoms')]
            
    def on_next(b):
        if FnScope.i==len(FnScope.item_list)-1:
            try:
                FnScope.item_list.append(sess.run(items))
            except:
                return
        FnScope.i += 1
        FnScope.c = updata_view(v, FnScope.item_list[FnScope.i], FnScope.c)
        p.options = ['Sample {}'.format(FnScope.i+1)] + ['{}: {:.6f}'.format(k,v) for k,v in 
                                FnScope.item_list[FnScope.i].items()
                                if (k!='coord' and k!='atoms')]
    
    b1.on_click(on_prev)
    b2.on_click(on_next)
    vib_viewer = HBox([v, VBox([p, HBox([b1,b2])])])
    display(vib_viewer)

from pinn.datasets.qm9 import qm9_format

label_map = {k:k for k in ['A', 'B', 'C', 'mu', 'alpha', 'homo', 'lumo', 'gap',
           'r2', 'zpve', 'U0', 'U', 'H', 'G', 'Cv']}
qm9_full = qm9_format(label_map=label_map)