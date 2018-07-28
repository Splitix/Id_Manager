import json
from browser import console
from renderer import RenderMixin

class PNet(RenderMixin):
    """
    data structure for rendering state machine source as a Petri-Net
    """

    def __init__(self, source, editor=None):
        """ persistent Petri-Net object """ 
        self.net = source['machine']
        self.editor = editor

        self.places = {}
        self.place_names = {}
        self.place_defs = {}

        self.vector_size = 0
        self.token_ledger = {}

        self.arcs = []
        self.arc_defs = {}

        self.transition_defs = {}
        self.transitions = {}

        self.handles = {}
        self.reindex()

    def reindex(self):
        """ rebuild data points """

        for name, attr in self.net['places'].items():
            self.place_names[attr['offset']] = name
            self.place_defs[name] = attr

            if name not in self.token_ledger:
                self.token_ledger[name] = attr['initial']

        self.vector_size = len(self.place_defs)

        for name, attr in self.net['transitions'].items():
            # once refactor is in place
            if name not in self.arc_defs:
                self.arc_defs[name] = []

            for i in range(0, self.vector_size):
                delta = attr['delta'][i]

                if delta == 0:
                    continue

                place = self.place_names[i]

                if delta > 0:
                    arc_transaction = {
                        'source': name,
                        'target': place,
                        'weight': delta,
                        'offset': i,
                        'delta': delta
                    }

                elif delta < 0:
                    arc_transaction = {
                        'source': place,
                        'target': name,
                        'weight': 0 - delta,
                        'offset': i,
                        'delta': delta
                    }

                self.arc_defs[name].append(arc_transaction)

            self.transition_defs[name] = attr

    def reset_tokens(self):
        """ rebuild token counters to initial state """
        # FIXME: clearing all ledger entries causes an error when a petri-net
        # def is created in the browser rather than loaded from the server
        #self.token_ledger = {}

        for name, attr in self.net['places'].items():
            self.token_ledger[name] = attr['initial']

    def _new_place_name(self):
        for i in range(0, self.vector_size):
            label = 'p%i' % i

            if label not in self.place_defs:
                return label

        return None

    def insert_place(self, coords, initial=0):
        """ add place symbol to net """
        _offset = self.vector_size
        self.vector_size = _offset + 1

        label = self._new_place_name()
        assert label

        self.place_defs[label] = {
            'position': coords,
            'initial': initial,
            'offset': _offset
        }

        self.place_names[_offset] = label
        self.token_ledger[label] = initial

        for name, attr in self.transition_defs.items():
            attr['delta'].append(0)

    def _new_transition_name(self):
        for i in range(0, len(self.transition_defs) + 1):
            label = 't%i' % i

            if label not in self.transition_defs:
                return label

        return None

    def insert_transition(self, coords):
        """ add transition symbol to net """
        label = self._new_transition_name()

        self.transition_defs[label] = {
            'position': coords,
            'delta': [0] * self.vector_size
        }

    def update(self, statevector):
        """
        update token counters by
        setting a new statevector
        """

        for name, attr in self.place_defs.items():
            self.token_ledger[name] = statevector[attr['offset']]

    def update_place_tokens(self, name, token_count):
        """
        update token counters for specific place
        """

        self.token_ledger[name] = token_count

    def delete_place(self, refid):
        """ remove a place symbol from net """

        # FIXME this seems to leave some place names
        # REVIEW: does this problem persist?
        #console.log(self.place_defs[refid])
        offset = self.place_defs[refid]['offset']

        for idx, name in self.place_names.items():
            if name == refid:
                del self.place_names[idx]
                break

        for label in self.transition_defs.keys():
            del self.transition_defs[label]['delta'][offset]


        for _, attr in self.place_defs.items():
            if attr['offset'] > offset:
                attr['offset'] = attr['offset'] - 1

        del self.token_ledger[refid]
        del self.place_defs[refid]
        del self.places[refid]

        self.delete_arcs_for_symbol(refid)
        self.vector_size = len(self.place_defs)

    def delete_transition(self, refid):
        """ remove a transition symbol from net """
        try:
            del self.transition_defs[refid]
            del self.arc_defs[refid]
            del self.transitions[refid]
        except:
            pass

    def delete_arcs_for_symbol(self, refid):
        """ remove arcs associated with a given place or transition """
        for label, txns in self.arc_defs.items():
            for i, txn in enumerate(txns):
                if refid == txn['target'] or refid == txn['source']:
                    del self.arc_defs[label][i]
