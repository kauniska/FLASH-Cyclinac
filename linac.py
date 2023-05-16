import numpy as np

import xobjects as xo
import xtrack as xt
import xpart as xp

class Linac():
    """
    A Class for creating linac accelerator objects based on Xsuite, that can be used to
    make a single-particle tracking simulation that returns things like the particle
    coordinates and Twiss parameters of the accelerator.
    """
    def __init__(self, elements, element_names, ref_particle_type='p', ref_energy='150') -> None:
        """_summary_

        Args:
            elements (list): A list of accelerator elements as Xsuite objects
            element_names (list): A list of strings giving the names of the corresponding elements
            ref_particle_type (str, optional): Particle species. Defaults to 'p' for proton.
            ref_energy (str, optional): Energy of the reference particle in MeV. Defaults to '150'.

        Raises:
            Exception: if input particle type not supported
        """
        self._line = xt.Line(elements=elements, element_names=element_names)
        self._context = None
        self._tracker = None
        if ref_particle_type == 'p' or ref_particle_type =='proton':
            self._line.particle_ref = xp.Particles(p0c=ref_energy*10**6, q0=1, mass0=xp.PROTON_MASS_EV)
        else:
            raise Exception("Particle types other than protons not supported yet")
        
    def adjust_magnet(self,name,strength):
        self._line[name].knl[1]=strength
        
    def tracker(self,context):
        # Set up context for tracker
        if context=='CPU':
            self._context = xo.ContextCpu()
        elif context =="CUDA":
            self._context = xo.ContextCupy()
        else:
            raise Exception("Context type not supported. Please choose either 'CPU' or 'CUDA'.")
        self._tracker = self._line.build_tracker(_context=self._context)
        
    def twiss(self,context='CPU'):
        self.tracker(context)
        return self._line.twiss()
    
    def simulate(self, particles, context='CPU', turns=1):
        self.tracker(context)
        self._line.track(particles, num_turns=turns, turn_by_turn_monitor=True)
        x = self._line.record_last_track.x
        px = self._line.record_last_track.px
        return x, px
        
    

        
    
        
    