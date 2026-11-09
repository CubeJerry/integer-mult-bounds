"""The actual complete Core replaces the inherited destructive core double.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from format_bridge import FormatBridge
from original_layout import OriginalCore
from words import need


class AttachedCore:
    def __init__(self, root, halo, observe=None, observe_bridge=None):
        self.halo = halo
        self.core = OriginalCore(root, observe=observe)
        self.bridge = FormatBridge(halo.B)
        self.observe_bridge = observe_bridge

    def forbidden(self):
        return (*self.core.forbidden(), *self.bridge.forbidden())

    def note(self, name, tape):
        if self.observe_bridge is not None:
            self.observe_bridge(name, tape)

    def mutate(self, transport, routes, inverse_code, forward_code,
               inverse_banks, forward_banks, keys,
               inverse_parameters, forward_parameters, union_parameters,
               halo_width, common_width, q, P, drop):
        need(transport.phase == 'saved', 'save original halo before any Core mutation')
        payload = self.bridge.lift(transport.source, halo_width, common_width, q, P)
        self.note('lifted_input', payload)
        returned = self.core.run(payload, routes.forward, routes.inverse, routes.parameters,
            inverse_code, forward_code, inverse_banks, forward_banks, keys,
            inverse_parameters, forward_parameters, union_parameters)
        try:
            self.note('original_core_return', returned)
            self.bridge.normalized_return(returned, transport.source,
                                          halo_width, common_width, drop)
            self.note('normalized_source', transport.source)
        finally:
            if self.core.pending:
                self.core.consume()
            self.bridge.clear_input()
        transport.phase = 'core'

    def run(self, transport, shape, archive, workspace, bill, routes,
            inverse_code, forward_code, inverse_banks, forward_banks, keys,
            inverse_parameters, forward_parameters, union_parameters,
            halo_width, common_width, q, P, drop):
        transport.gather()
        transport.sort(transport.saved)
        self.note('saved_original_halo', transport.saved)
        self.mutate(transport, routes, inverse_code, forward_code,
            inverse_banks, forward_banks, keys, inverse_parameters,
            forward_parameters, union_parameters, halo_width, common_width, q, P, drop)
        codec = self.halo.Codec(transport, shape, archive, workspace, bill)
        codec.run()
        transport.merge_returns()
        return codec
