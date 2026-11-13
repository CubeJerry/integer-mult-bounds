# Actual mixed handoffs: an invariant of source colour pairs

Status: root mathematical proof and independent source calculation; external proof review pending. This is a scoped obstruction and a necessary interface, not a complete source or kappa improvement.

## Physical endpoint freedom

For each of the96 hosted complex ports, original source roles X_j and B_j begin on the same line and finish at Hub; Y_j and D_j both begin at zero and finish on the same facet. Thus invertible input colour changes on each (X_j,B_j) and invertible output colour changes on each (Y_j,D_j) can be performed cocharted, with their ordinary cost retained. To strengthen the obstruction we may grant arbitrary invertible mixing of ALL200 receiver outputs, arbitrary mixing of initial receiver inputs at zero, and arbitrary final Hub decoding. Initial receiver mixing does not change source-input columns; Hub decoding does not act on receiver rows. Invertible source-pair and receiver transformations preserve the rank of the receiver transfer from each source pair.

The required original complete source has receiver transfer rank V from each hosted pair (X_j,B_j): the X_j column sends x_j to Y_j, while B_j has no receiver contribution. The partial parent also has rank V for each such pair, despite its many other incorrect endpoints. It is not a complete target.

## Exact admitted-source data

Let H be the200-by96 source-X receiver matrix of the frozen partial parent a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc, and write its columns u_j. Its source-B receiver matrix is zero. Let W be the span of the eight literal Gram-packet decoder columns, including every Y and D receiver output. A separate dense integer interpreter, not the construction author's sparse engine, gives

    rank(H)=20, dim(W)=8, rank([W,H])=28.

All96 columns u_j are nonzero and pairwise nonproportional. Therefore their images modulo W are nonzero and pairwise independent. These are exact finite source identities. The verifier supplies an explicit28-rank minor, spanning coefficients, and all4560 pair tests; they do not classify a changed early source.

## One genuinely mixed mode, all block volumes

Work over characteristic zero with arbitrary V>=1. Keep the old source transfer modulo W tensor F^V: a hosted X_j column block may change to

    U_j + W K_j + Gamma C_j,

where U_j=u_j tensor I_V, W now denotes the8V-dimensional old decoder embedding, and Gamma:F^V->F^(200V) is an arbitrary new mode decoder, even with noncommuting block coefficients. Suppose one actual new packet payload has original-B part sum_j h_j b_j, with scalar h_j, so its B_j transfer is h_j Gamma. At least two h_j are nonzero. No other new B-dependent acquisition is granted.

Claim: if Gamma is nonzero, some hosted source pair has receiver-transfer rank greater than V. Hence no allowed invertible source-colour/receiver recoding turns this source into either the parent receiver map or the complete target map.

Proof: assume every pair has rank at most V. For any j with h_j nonzero, its column span equals that of U_j+W K_j and Gamma, since the Gamma C_j term can be eliminated using the B_j columns. Quotient by W. The resulting span contains the full V-dimensional image of U_j and the image of Gamma. Rank at most V forces image(Gamma modulo W) to lie in image(U_j modulo W). Two distinct supported ports have disjoint such images, because their scalar columns are independent modulo W. Hence Gamma has image in W. The X_j block still has full rank V modulo W, so its span intersects W only at zero. Any nonzero Gamma then increases the unquotiented pair rank above V, a contradiction. This uses no invertibility of Gamma and covers a rank-deficient decoder as well. QED.

Changing the eight old X encoder/decoder modes within W does not evade this statement. Inserting independently acquired B functions into other packets is an additional acquisition, not just a basis change of the old X payloads. If arbitrary W-valued B corrections are also granted, the same quotient argument forces Gamma modulo W=0, and then forces every NET B receiver column to vanish. Such a cancellation can leave a useful pure-D observation; its actual source access and costs must be constructed. The theorem does not declare it impossible.

For the literal exchanged source cb77301a8f402fcc0f8dc069faefa0f0b3c6dfaedb6122a5a7d65b04802e2514, the new B support is {1,106} with coefficients of opposite sign. The actual fixed decoder gives rank-two scalar source pairs at both ports, and the old source columns are independent modulo W. The all-V theorem therefore verifies and strengthens the author's single-mode colour obstruction.

## Necessary condition for coordinated scalar modes

For scalar values, allow k new decoded modes, with all their receiver directions in L=span(Gamma), dim L<=k. Let J be the ports where the NET B receiver column is nonzero after all permitted cancellations. Suppose X_j differs from u_j only by a vector in W+L and B_j lies in W+L. If each pair has rank at most one, then its X_j column is a scalar multiple of its nonzero B_j column. Consequently u_j belongs to W+L for all j in J, and

    rank({u_j mod W : j in J}) <= dim((W+L)/W) <= k.

In particular contaminating every hosted B input requires at least20 new independent decoder modes in this fixed-source interface. This is only a necessary condition: k=2 on support{1,106} passes this rank test, but no source, endpoint or cost conclusion follows. For arbitrary blocks one cannot replace partial-rank B_j blocks by whole scalar ports; no direct all-V cardinality version is claimed.

## Complete source-rank requirement in the same fixed interface

The complete source-to-receiver matrix from all104 X and96 B inputs has rank104: every first-Y receives a nonzero multiple of its own X input, and D receives no source input. The parent has rank20. If every permitted modification to the receiver transfer lies in W+L, where L has dimension at most k, the full changed transfer has rank at most20+8+k. Invertible input colour changes and invertible receiver decoding preserve this rank. Therefore complete endpoints require k>=76. This counts independent new RECEIVER DIRECTIONS outside the granted old decoder space, not packets, MOVEs or historical modes. It does not prove76 transport calls: one funded trajectory can create several directions, and changing the earlier raw-source transfer is outside this fixed-interface premise. A proposed coordinated handoff should report which genuinely new directions it supplies and how it changes the raw source, not merely which packet payloads differ.

The restriction is on the fixed primal source modulo its existing Gram decoder space. Changed earlier raw-source operations, coordinated captures that alter that quotient, genuinely acquired cancellation modes, nonlocal source-input transport, and different endpoint interfaces require fresh analysis. No global impossibility, supplier, or new kappa is asserted.
