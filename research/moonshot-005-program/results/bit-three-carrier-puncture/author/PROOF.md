# Three fixed carriers for the punctured pivot decoder

**Proved static bridge and conditional decoder identity. No emitted source extension, complete invoice, or new kappa.**

The fixed 111-root BIT source has SHA-256 51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78. Roots are recovered from the admitted flat-cubic certificate, SHA-256 4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc. This is not a fresh compressed-native replay. All coefficient identities hold over every characteristic-two field and every block width.

## Three totals and six moments

Normalize roots to norm squared 4. Put r=r92,z=r15,w=r106; r=z-w. The binary polar form is B(i,j)=(r_i dot r_j)/2 modulo 2. The three axes span an anisotropic binary plane. Set alpha_j=B(j,z), beta_j=B(j,r), a_j=alpha_j*r+beta_j*z. The complementary component u_j lies in a six-dimensional space. Then

K_ij=1+B_A2(a_i,a_j)+B_E6(u_i,u_j).

The native partition is 32 common roots, wings of sizes 25,25,26, and the three axes. Let T_a sum all inputs with a_j=0 or a_j=a, including axis a. These are exactly the three canonical axis rows. Their sum is the all-input total.

For a_i nonzero, K_iX=T_(a_i)+B_E6(u_i,sum_j u_jX_j). For a_i=0, replace T_(a_i) by T_r+T_z+T_w. The total space has rank 3, the moment space rank 6, and their joint rank is 9. No physical availability follows.

## Three-coordinate fitting

Set p_j=beta_j and A_ij=K_ij when p_i=p_j, zero otherwise. Its blocks have sizes 58,53 and ranks 7,8. Thus rank A=15 and rank(row A+row K)=16.

Let T={92,15,106}. Define C_i=e_i for i in T; elsewhere delete the T columns from A_i. This preserves the own diagonal and every required zero. Exact ranks are rank C=18 and rank(row C+row K)=19. RESULT.json includes an echelon certificate. F2 row identities and nonzero pivot minors lift to every characteristic-two field.

## Fixed proper covers

For p_i=0 and i not equal to 92, every remaining foreign source lies in F_i intersection F92. These 57 supports have exact real rank 6, so their minimum proper-cover number is 1.

For p_i=1 and i outside T, a foreign root v is orthogonal to r_i and has binary pairing 1 with r. All three axis lines have been deleted. Orient v so r dot v=2. Since v is not parallel to r,z,w, its products with z,w belong to {-2,0,2}. Their difference is 2, forcing (2,0) or (0,-2). Every foreign source therefore lies in F_i intersection F15 or F_i intersection F106. Both intersections are proper rank 6. All 51 supports have exact rank 7, so their minimum cover number is 2.

The three completed rows have empty support. There are 3 empty, 57 one-cover and 51 two-cover rows. The capped charge min(2,max(0,m_i-1)) sums to chi=51.

Excluding the r92 axis from the preliminary root argument is essential: its self-product is 4, not 2. Independent review corrected this wording; the paid-axis and p=1 conditions already impose the exclusion. The useful change is the common carrier geometry, not the numerical improvement from chi52 to51.

## Conditional decoder identity

Suppose an actual prefix owns pure ground x_t for t in T, completes Y_t=y_t+x_t, and preloads each remaining Y_i with sum_(t in T) A_it*x_t. If a continuation supplies A_iX and the proper foreign correction at legal charts on Y_i's route, cancellation gives y_i+x_i.

This provides no point copy, code word, correction sum, route, or erasure. The earlier two-loan prefix retains an actual source-line x106 copy, but no third-loan extension was emitted here. Its movement costs, margins, and punctured rigidity bounds are not automatically transferred after deleting role 106.

## Verification and continuation

The checker authenticates the certificate, recovers the native indices, checks all 111-squared identities, coefficient ranks, and foreign ranks. Exact orthogonal upper witnesses accompany modular103 lower witnesses; modular rank is never used alone to infer a rational upper bound.

Leaving coordinate 15 unpaid fails the proposed cover at receiver3/source15. Leaving106 unpaid fails at receiver2/source106. These exact controls exclude free puncturing. The construction worker independently reviewed the geometric argument and conditional identity; this is not a second run of the finite checker.

```sh
node author/check.js flat_RESULT.json
```

Expected: PASS_THREE_CARRIER_PUNCTURE_AND_SIX_MOMENT_BRIDGE. The pure function actually ran in cloud V8 during the local-executor outage.

The next task is a legal chronological construction using these carriers, or a new fitting for the induced 76-wing instance. This package proves only canonical rank9 for that instance. Strict compatible suppliers, complete recursion, and all five foundations remain.

Credit the pivot-filter and two-point-puncture authors, A2/Hesse worker, native and quadratic/cubic predecessors, independent construction-worker review, and @CubeJerry. Developed with substantial OpenAI assistance.
