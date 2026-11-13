# Sharp order-four ring candidate — review pending

Root proposed an error-one exact-sum Gaussian integer bijection with F²=wire swap, F⁴=id and optimal forward/bilateral radial slack beta=sqrt19-sqrt13. B is reviewing the universal lower bound; A is independently checking construction and arithmetic. This checkpoint is not publication approval.

Use H=[[1,1],[1,-1]],T=H/2,J(a,b)=(-b,a),Q=-J. At sum s and difference d, equal-parity sums use d′=Jd exactly. Otherwise t=TJd is half-integral and d′=HM(t). The pair norm squared is c+||t||² with c=||s||²/2>=1/2.

Pair square rings of radii a and a+1, a=2m+1/2. Join(a,a)to(a+1,a) and its three90-degree rotations. Remove endpoints; inner arcs have4m vertices, outer arcs4m+2. Match consecutive vertices, rotating choices. This gives an involutive unit-neighbor matching M commuting with Q. In t coordinates F is g=QM, so g²=-I. Exact inverse is swap after F. Sum, global i and wire-swap covariance hold; mixed-parity combined error is1.

Tangential edges have radial jump<1/sqrt2. Connector jumps decrease with c, and at c=1/2 equal delta(a)=sqrt(2a²+2a+3/2)-sqrt(2a²+1/2). Derivative sign is sign(-2a²+2a+1/2), hence decrease for a>=5/2. delta(1/2)=sqrt3-1<3/4<delta(5/2)=beta. Therefore beta is attained and bounds all edges.

Universal lower: fix exact sum1. Any F²=swap is bijective on the fiber and its difference map f squares to-I. t=TJd identifies input differences with even-sum half-grid color A. M_A=T f (TJ)^-1 is a unit-neighbor bijection A to opposite color B: exact-sum error<=1 forces the two integer difference errors to be±1. Since g=QM_A and g²=Q², M_A Q M_A=Q. Extend M on B by M_A^-1. This identity gives MQ=QM on BOTH colors, with no phase premise. In the36-point box maxabs<=5/2, internal matching-edge rotation orbits cover8 vertices. No unit edge is fixed by a half-turn. Thus some edge leaves the box; its endpoints are(±5/2,y),(±7/2,y), |y|<=5/2. At c=1/2 radial jump>=sqrt19-sqrt13. F²=swap reverses each radial jump on the next call, so forward outward and bilateral suprema coincide for every competing map.

Exact sum+F²=swap cannot also have conjugation K F K=F^-1. At real input(1,0), outputs would be conjugates summing1, impossible over Gaussian integers because their real sum is even. No error/phase premise is used.

Known #6778 at f711bd201a037ba6a7e3fed72d00bfcbf4f0420a blocks same-stateless-map tensor commutation under Gaussian-unit covariance and integral-image exactness. It applies here; root rediscovery of n1 is not new work. No physical tariff, selected caller, kappa or assumption discharge.

Prepared for @CubeJerry with substantial OpenAI assistance. B found the initial order-four alternative and parity/energy obstructions; root proposed this sharper ring construction and36-box bound. Complementary reviews are pending. Root checker passes1024half-grid points,6561pairs,40cases through1024bits and exact beta attainment; universal claims rely on the written proof, not finite tests.
