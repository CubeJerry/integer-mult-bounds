# Exploratory reclosure correction

The first, unadmitted screen counted only blocked routes that left the initial
source closure. When new edges enlarge that closure, a blocked route whose
tail was initially outside can become a new outgoing boundary occurrence.
Failing to count it can falsely report a rank deficit.

Before admission, the generator was changed to retain every blocked boundary
occurrence except the actual deletions. It now also enumerates all original
routes directly for each discovered certificate and requires equality with
the computed boundary. All target minors are replayed exactly.

The corrected runs for e43,e96404,e96513 happened to reproduce the earlier
zero-survivor counts. That coincidence does not validate the old method.
Their initial SCREEN receipts are retained as
INVALIDATED-INITIAL-SCREEN.json and prove no theorem. The original e89777 main
package always directly counted full boundaries and was unaffected.

The final proof checker does not perform reclosure at all: it verifies the
retained chart sets, exact target minors, full old boundaries, both new routes
and complete endpoint coverage. Thus its correctness does not depend on the
repaired exploration routine or a search failure.
