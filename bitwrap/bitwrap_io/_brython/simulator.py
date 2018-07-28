class Simulation(object):
    """ use pnet to run a simulation """

    def __init__(self, oid, editor):
        editor.ctx.log('loading simulation %s' % oid)
        self.pnet = editor.instance
        self.editor = editor
        self.history = []
        self.hilight_live_transitions()
        self.oid = oid

    def state_vector(self):
        """ return current state vector from token_ledger """
        vector = [0] * self.pnet.vector_size

        for name, attr  in self.pnet.place_defs.items():
            vector[attr['offset']] = self.pnet.token_ledger[name]

        return vector

    def commit(self, action, input_state=None, dry_run=False):
        """ transform state_vector """
        out = [0] * self.pnet.vector_size

        if not input_state:
            state = self.state_vector()
        else:
            state = input_state

        txn = self.pnet.transition_defs[action]['delta']

        for i in range(0, self.pnet.vector_size):
            out[i] = state[i] + txn[i]
            if out[i] < 0:
                return False

        if not dry_run:
            self.pnet.update(out)

        return True

    def is_alive(self, action, from_state=None):
        """ test that input transition can fire """
        return  self.commit(action, input_state=from_state, dry_run=True)

    def trigger(self, event):
        """ callback to trigger live transition during simulation """
        target_id = str(event.target.id)

        if not self.editor.is_selectable(target_id):
            return

        refid, symbol = target_id.split('-')

        if self.pnet and symbol == 'transition':
            return self.execute(refid)

    def execute(self, action):
        if self.commit(action):
            self.history.append(action)
            self.editor.reset(callback=self.redraw)

        return action

    def reset(self):
        """ render SVG and disable hilight """
        self.pnet.reset_tokens()
        self.editor.reset(callback=self.editor.render)

    def redraw(self):
        """ render SVG and hilight live transitions """
        self.editor.render(callback=self.hilight_live_transitions)

    def hilight_live_transitions(self):
        """ visually indiciate which transitions can fire """
        current_state = self.state_vector()

        for action in self.pnet.transitions.keys():
            if self.is_alive(action, from_state=current_state):
                self.pnet.handles[action].attr({ 'fill': 'red' })

