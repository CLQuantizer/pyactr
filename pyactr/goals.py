"""
Goals.
"""

import collections

import pyactr.chunks as chunks
import pyactr.utilities as utilities
import pyactr.buffers as buffers

class Goal(buffers.Buffer):
    """
    Goal buffer module.
    """

    def __init__(self, data=None, default_harvest=None, set_delay=0.05):
        buffers.Buffer.__init__(self, default_harvest, data)
        self.set_delay = set_delay

    def add(self, elem, time=0, harvest=None):
        """
        Clears current buffer (into a memory) and adds a new chunk. Decl. memory is either specified as default_harvets, when Goal is initialized, or it can be specified as the argument of harvest.

        """
        self.clear(time, harvest)
        super().add(elem)
        
    def clear(self, time=0, harvest=None):
        """
        Clears buffer, adds cleared chunk into decl. memory. Decl. memory is either specified as default_harvest, when Goal is initialized, or it can be specified as harvest here.
        """
        if harvest != None:
            if self._data:
                harvest.add(self._data.pop(), time)
        else:
            if self._data:
                self.dm.add(self._data.pop(), time)


    def copy(self, harvest=None):
        """
        Copies the buffer. Unlike other buffers, this one does not copy the memory that is used for its harvest. This is because goal buffer will always share the memory to which it harvests with another retrieval buffer. You have to specify harvest if you want clearing to work in the copied buffer.
        """
        if harvest == None:
            harvest = self.dm
        copy_goal = Goal(self._data.copy(), harvest)
        return copy_goal

    def retrieve(self, otherchunk, actrvariables=None):
        """
        Retrieve a chunk does not work in goal buffer.
        """
        raise AttributeError("Attempt to retrieve from goal. This is not possible.")

    def create(self, otherchunk, harvest=None, actrvariables=None):
        """
        Creates (aka sets) a chunk in goal buffer.
        """
        mod_attr_val = {x[0]: utilities.check_bound_vars(actrvariables, x[1]) for x in otherchunk.removeunused()} #creates dict of attr-val pairs according to otherchunk

        new_chunk = chunks.Chunk(otherchunk.typename, **mod_attr_val) #creates new chunk

        self.add(new_chunk, harvest) #put chunk using add - i.e., clear first, then add

