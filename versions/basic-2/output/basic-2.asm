; Constants
osbyte_read_himem = &84
osbyte_read_oshwm = &83

; Memory locations
l0000  = &00
; &00 referenced 4 times by &af56, &bd22, &be20, &be46
l0001  = &01
; &01 referenced 4 times by &af5a, &bd28, &be1b, &be4a
l0002  = &02
; &02 referenced 15 times by &8c2f, &8c4c, &8c61, &8c6f, &951a, &9521, &952a, &9534, &953b, &9556, &af5e, &bd24, &be16, &be3c, &be4e
l0003  = &03
; &03 referenced 12 times by &8c33, &8c53, &8c64, &8c71, &9516, &953f, &9541, &af62, &bd2a, &be11, &be36, &be52
l0004  = &04
; &04 referenced 60 times by &8c68, &9549, &9ab6, &9abd, &9ac4, &9acb, &9add, &9adf, &9af6, &9b08, &9b43, &9b5e, &9b8a, &9c23, &9c5e, &9c65, &9c6c, &9c73, &9c7a, &9c7e, &9cc5, &9ccc, &9cd3, &9cda, &9e5c, &bd40, &bd51, &bd5d, &bd6c, &bd71, &bd76, &bd7b, &bd7e, &bd85, &bd94, &bda0, &bda5, &bdaa, &bdaf, &bdb3, &bdc1, &bdc8, &bdcd, &bdd4, &bdde, &bde1, &bde3, &bdec, &bdf1, &bdf6, &bdfb, &be00, &be04, &be0f, &be14, &be19, &be1e, &be23, &be27, &be2e
l0005  = &05
; &05 referenced 13 times by &8c6b, &9543, &9ae3, &9c84, &9e60, &bd44, &bd87, &bd8d, &bde7, &be08, &be2b, &be32, &be34
l0006  = &06
; &06 referenced 3 times by &8028, &bcbc, &bd3e
l0007  = &07
; &07 referenced 3 times by &802a, &bcc0, &bd42
l000a  = &0a
; &0a referenced 33 times by &8512, &8517, &8577, &857e, &85d3, &85d5, &85d7, &8617, &8715, &874e, &8780, &8795, &87cc, &8829, &883c, &883e, &8a97, &8a99, &8b28, &8b60, &8b7f, &8b96, &8ba3, &8ba5, &8be2, &95d1, &97dd, &97df, &9801, &9857, &9879, &98b9, &9b25
l000b  = &0b
; &0b referenced 29 times by &8567, &8582, &8590, &85d9, &861a, &8840, &8a9b, &8afc, &8b1e, &8b63, &8b76, &8b83, &8b9d, &8ba7, &8bbf, &95c9, &97e1, &97ec, &97f4, &97fc, &985b, &986f, &9871, &9891, &989c, &98a0, &98af, &98b1, &9b1d
l000c  = &0c
; &0c referenced 10 times by &8596, &8af8, &8b22, &8b78, &8b8b, &8bc3, &95cd, &9875, &98b5, &9b21
l000d  = &0d
; &0d referenced 2 times by &804d, &8059
l000e  = &0e
; &0e referenced 2 times by &804f, &805d
l000f  = &0f
; &0f referenced 2 times by &8051, &8061
l0010  = &10
; &10 referenced 1 time by &8053
l0011  = &11
; &11 referenced 1 time by &804b
l0012  = &12
; &12 referenced 18 times by &8ae5, &8ae9, &8aee, &8af1, &aee6, &bc3a, &bc57, &bc6f, &bc8a, &bcaa, &bcbe, &bd20, &be75, &be79, &be80, &be86, &be93, &be95
l0013  = &13
; &13 referenced 12 times by &8ae1, &aee8, &bc42, &bc62, &bc6b, &bc84, &bcae, &bcb7, &bcc2, &bd26, &be71, &be99
l0014  = &14
; &14 referenced 2 times by &9925, &9951
l0016  = &16
; &16 referenced 2 times by &8b00, &8b0d
l0017  = &17
; &17 referenced 2 times by &8b04, &8b11
l0018  = &18
; &18 referenced 5 times by &8031, &8adf, &9974, &bd3a, &be6f
l0019  = &19
; &19 referenced 22 times by &8a90, &8bc1, &95cb, &95d7, &95ee, &95f9, &9606, &9663, &9817, &9b1f, &9bc3, &9beb, &9e28, &a09a, &a141, &a14c, &a159, &adcc, &addb, &adf0, &ae79, &aede
l001a  = &1a
; &1a referenced 4 times by &8bc5, &95cf, &9608, &9b23
l001b  = &1b
; &1b referenced 40 times by &8827, &8a8c, &8a8e, &8bc7, &8bd0, &95a8, &95b0, &95d5, &9603, &9617, &965f, &9661, &966e, &9683, &96c1, &96e4, &9705, &9813, &9815, &984d, &9b27, &9b34, &9bc1, &9bd4, &9bdf, &9be9, &9bfa, &9e24, &9e26, &a0e8, &ade4, &adec, &adee, &ae20, &ae38, &ae59, &ae77, &aea5, &aedc, &aee4
l001c  = &1c
; &1c referenced 1 time by &bd4e
l001d  = &1d
; &1d referenced 1 time by &bd3c
l001e  = &1e
; &1e referenced 4 times by &851e, &b56a, &b572, &bc2a
l001f  = &1f
; &1f referenced 1 time by &8035
l0020  = &20
; &20 referenced 2 times by &8ae7, &9895
l0021  = &21
; &21 referenced 1 time by &9907
l0022  = &22
; &22 referenced 1 time by &990b
l0023  = &23
; &23 referenced 2 times by &803e, &b568
l0024  = &24
; &24 referenced 1 time by &bd48
l0025  = &25
; &25 referenced 1 time by &bd4c
l0026  = &26
; &26 referenced 1 time by &bd4a
l0027  = &27
; &27 referenced 21 times by &85b2, &8bf1, &8c01, &99cb, &9a39, &9a56, &9a62, &9b37, &9c94, &9ca1, &9ca7, &9cea, &9cfa, &9d26, &9d34, &9d55, &9dc6, &9def, &9dfb, &b4bd, &b4e0
l0028  = &28
; &28 referenced 10 times by &84ff, &8506, &8519, &8632, &8691, &881a, &886a, &8873, &8b15, &ae30
l0029  = &29
; &29 referenced 4 times by &8623, &8651, &8832, &8837
l002a  = &2a
; &2a referenced 97 times by &867b, &86a6, &8818, &8c29, &8c46, &8c4a, &8c51, &8c5c, &8c76, &8c7d, &8c82, &8c88, &8c8e, &8c93, &8cac, &8cb4, &9242, &924b, &9255, &94aa, &94e4, &95e7, &968e, &9696, &9698, &96e9, &96f1, &972a, &972e, &9760, &9762, &9786, &9788, &978c, &9790, &9792, &979b, &979f, &97a4, &97a6, &97af, &97b1, &97c4, &97f6, &9905, &992e, &993d, &9994, &99ea, &9a14, &9ab8, &9aba, &9ad3, &9b45, &9b48, &9b60, &9b63, &9b8c, &9b8f, &9bb5, &9c60, &9c62, &9cc7, &9cc9, &9d93, &9da6, &9e9a, &a12b, &a2cf, &a3f5, &ad97, &ad99, &ae6f, &ae94, &aeea, &af58, &b338, &b33d, &b342, &b346, &b348, &b34f, &b355, &b35a, &b35f, &b364, &b369, &b38a, &b392, &b397, &b3ad, &b3c0, &b4c8, &bcf9, &bdad, &bdfd, &be44
l002b  = &2b
; &2b referenced 66 times by &8681, &86c8, &8738, &8809, &9246, &924d, &9257, &94b0, &94ea, &95b5, &95eb, &968b, &969b, &969d, &96ec, &9730, &9734, &9766, &9768, &9784, &978a, &978e, &9795, &9797, &979d, &97a1, &97aa, &97b5, &97b7, &97ba, &97c9, &97fe, &9909, &9934, &993b, &997c, &99ec, &9a19, &9abf, &9ac1, &9ad5, &9bb7, &9c67, &9c69, &9cce, &9cd0, &9d4e, &9d69, &9d97, &9da8, &a12f, &a2d3, &a3f1, &ad9c, &ad9e, &ae71, &ae96, &aeec, &af5c, &b34a, &b3a7, &b4d0, &bcf4, &bda8, &bdf8, &be48
l002c  = &2c
; &2c referenced 48 times by &8bda, &8c21, &8c31, &8c80, &8c95, &8c9a, &958e, &95bb, &95f7, &9601, &964c, &96a0, &96b4, &96c5, &96cc, &96d3, &96e6, &977e, &97be, &99ee, &9a1e, &9ac6, &9ac8, &9ad7, &9bb9, &9c6e, &9c70, &9cd5, &9cd7, &9d43, &9d5e, &9d9c, &9daa, &a133, &a2d7, &a3ed, &ada1, &ada3, &ae73, &ae98, &aef0, &af60, &b32c, &b33f, &b4d5, &bda3, &bdf3, &be4c
l002d  = &2d
; &2d referenced 41 times by &8c35, &8c57, &8c79, &8c90, &96fd, &971f, &973e, &97c0, &99c2, &99d4, &99e8, &9a23, &9aad, &9ab1, &9ad1, &9bbb, &9c75, &9c77, &9cdc, &9d41, &9d5c, &9d6d, &9d7c, &9da2, &9dac, &a121, &a2c4, &a2db, &a3e9, &ad71, &ada6, &ada8, &ae75, &ae9a, &aef2, &af64, &b33a, &b4da, &bd9e, &bdee, &be50
l002e  = &2e
; &2e referenced 38 times by &9a6c, &a0fd, &a1e6, &a1ed, &a21e, &a2cd, &a2e6, &a2f6, &a2fb, &a394, &a398, &a39e, &a3c8, &a3d3, &a3dd, &a468, &a4a3, &a4a5, &a4de, &a590, &a5da, &a632, &a636, &a688, &a6f1, &a6f5, &aaa2, &ad83, &ad87, &b366, &b371, &b37b, &b4f0, &b4f4, &b4fa, &bd60, &bd64, &bd6a
l002f  = &2f
; &2f referenced 19 times by &a0fb, &a1f1, &a1fd, &a21b, &a222, &a256, &a2c2, &a2ea, &a332, &a34a, &a3d1, &a4e2, &a61a, &a623, &a680, &a68a, &a6fe, &a707, &b36f
l0030  = &30
; &30 referenced 42 times by &9a76, &9e3f, &a0f7, &a1ef, &a1f5, &a1f9, &a217, &a226, &a24e, &a252, &a2e1, &a2e8, &a301, &a311, &a32e, &a346, &a38f, &a3cd, &a3fe, &a40c, &a418, &a44c, &a486, &a49d, &a4e6, &a513, &a555, &a58e, &a614, &a61f, &a629, &a62d, &a68c, &a6a1, &a6f8, &a703, &a820, &a82e, &aa94, &b36b, &b4eb, &bd5b
l0031  = &31
; &31 referenced 60 times by &9a7c, &a07d, &a0b4, &a0dd, &a125, &a190, &a194, &a19a, &a1ac, &a1b5, &a1cb, &a1d6, &a1da, &a20d, &a22a, &a271, &a28d, &a2a2, &a2b6, &a2dd, &a2fd, &a303, &a313, &a31b, &a336, &a342, &a39a, &a3e1, &a3e7, &a432, &a438, &a43c, &a481, &a483, &a49f, &a4ea, &a570, &a574, &a57f, &a596, &a5d4, &a5d6, &a5fc, &a600, &a68e, &a69e, &a70e, &a738, &a73c, &a74d, &a756, &a780, &a784, &a78f, &a7a4, &a824, &aa9c, &b37f, &b4f6, &bd66
l0032  = &32
; &32 referenced 56 times by &9a82, &a07f, &a0d9, &a11f, &a18a, &a18e, &a19d, &a1aa, &a1b3, &a1c6, &a1c8, &a1d3, &a1dc, &a20f, &a22e, &a275, &a291, &a29f, &a2b2, &a2d9, &a307, &a319, &a31f, &a340, &a3a2, &a3c3, &a3d5, &a3eb, &a42e, &a434, &a43e, &a47b, &a47d, &a4ee, &a56c, &a572, &a581, &a59c, &a5ce, &a5d0, &a5f6, &a5fa, &a690, &a714, &a732, &a736, &a74b, &a75c, &a77a, &a77e, &a78d, &a7a0, &b361, &b373, &b4ff, &bd6f
l0033  = &33
; &33 referenced 55 times by &9a88, &a081, &a0d5, &a131, &a184, &a188, &a1a0, &a1a8, &a1b1, &a1c1, &a1c3, &a1d1, &a1de, &a211, &a232, &a279, &a295, &a2ae, &a2d5, &a309, &a31d, &a323, &a33e, &a3a7, &a3be, &a3d7, &a3ef, &a42a, &a430, &a440, &a475, &a477, &a4f2, &a568, &a56e, &a583, &a5a2, &a5c8, &a5ca, &a5f0, &a5f4, &a692, &a71a, &a72c, &a730, &a749, &a762, &a774, &a778, &a78b, &a79c, &b35c, &b375, &b504, &bd74
l0034  = &34
; &34 referenced 58 times by &9a8e, &a083, &a0d1, &a12d, &a17e, &a182, &a198, &a1a6, &a1af, &a1bc, &a1be, &a1cf, &a1e0, &a213, &a236, &a27d, &a299, &a2aa, &a2d1, &a30b, &a321, &a327, &a33c, &a3ac, &a3b9, &a3d9, &a3f3, &a426, &a42c, &a442, &a46f, &a471, &a494, &a4f6, &a564, &a56a, &a585, &a5a8, &a5c2, &a5c4, &a5ea, &a5ee, &a676, &a67a, &a694, &a720, &a726, &a72a, &a747, &a768, &a76e, &a772, &a789, &a798, &b357, &b377, &b509, &bd79
l0035  = &35
; &35 referenced 38 times by &a073, &a085, &a097, &a0cb, &a0cd, &a129, &a178, &a17c, &a1a3, &a1b7, &a1b9, &a1cd, &a1e2, &a215, &a23a, &a281, &a2a4, &a2a6, &a2c0, &a30d, &a325, &a329, &a33a, &a3cf, &a4fa, &a566, &a587, &a5ae, &a5bc, &a5be, &a5e4, &a5e8, &a65c, &a67e, &a696, &a787, &a794, &b36d
l0036  = &36
; &36 referenced 24 times by &8534, &864c, &8c2b, &8c37, &8c86, &8c9d, &9af2, &9afa, &9b13, &9c25, &9c2b, &9c3b, &a068, &a06f, &ade2, &afc7, &b38c, &b39b, &b3ba, &bdb5, &bdba, &bdc6, &bdcf, &beba
l0037  = &37
; &37 referenced 81 times by &8529, &862e, &87d2, &87e3, &87f4, &8802, &887f, &888b, &8890, &889e, &88e0, &88ec, &88f9, &8902, &8917, &8944, &894e, &8957, &89b5, &89d2, &8a03, &8a07, &8a32, &8a41, &8a72, &8b20, &8bb5, &8bbc, &946b, &949a, &94d4, &94fe, &9528, &9610, &961b, &9651, &96b6, &9716, &9721, &9726, &973c, &9751, &9776, &97ad, &97c6, &97cb, &994f, &9955, &99d6, &9af0, &9b19, &9c1f, &9c3d, &9d7e, &9db8, &9e15, &b399, &b39e, &b4ca, &b4d3, &b4d8, &b4dd, &b4ed, &b4fc, &b501, &b506, &b50b, &b50e, &b525, &bc09, &bc36, &bc48, &bc4b, &bc4d, &bc55, &bc6d, &bc88, &bcb5, &bcd8, &bfd0, &bfe1
l0038  = &38
; &38 referenced 32 times by &8524, &8536, &8552, &8639, &8886, &88e6, &8948, &8b24, &8bba, &9615, &9713, &9719, &974e, &9773, &97b3, &99d2, &9e04, &b394, &b516, &b521, &b52c, &b52e, &b538, &bc0b, &bc40, &bc51, &bc60, &bc69, &bc86, &bcb9, &bcdf, &bfd3
l0039  = &39
; &39 referenced 43 times by &8530, &8630, &8654, &8881, &888e, &88e4, &88ee, &89f2, &89f8, &89ff, &8a0e, &8a19, &8a1d, &8a28, &8a2a, &8a39, &948e, &949e, &94c8, &94d8, &9523, &952c, &9654, &96a7, &96b1, &96ca, &972c, &975e, &99f7, &9a01, &9af8, &9b11, &9d8d, &9dae, &9e0d, &b4b7, &b4cc, &b51a, &b532, &bc0f, &bcac, &bcd6, &bce3
l003a  = &3a
; &3a referenced 38 times by &854c, &8643, &865b, &8888, &88ea, &89f6, &8a21, &8a2e, &9472, &947f, &9484, &9489, &9496, &94a3, &94a8, &94bb, &9501, &9507, &950d, &950f, &9518, &951d, &9551, &9732, &9764, &99f9, &9a03, &9aff, &9b03, &9d8b, &9db0, &9e0f, &b51c, &b542, &bc13, &bcb0, &bcdd, &bce5
l003b  = &3b
; &3b referenced 40 times by &8645, &8990, &899e, &89c4, &89e5, &8a4d, &8a62, &8a69, &8b26, &9477, &9479, &94ac, &94c0, &9505, &9511, &99fb, &9a05, &9a66, &9a6a, &9a70, &9a94, &9e11, &a066, &a06d, &a220, &a361, &a36c, &a376, &a455, &a4dc, &a592, &a5d8, &a634, &a6f3, &a819, &bc17, &bc8d, &bc9a, &bc9f, &bd08
l003c  = &3c
; &3c referenced 25 times by &8992, &89ac, &89c6, &89e7, &8a64, &8a6b, &8a84, &8b17, &9481, &94b9, &94be, &94c3, &94d0, &94dd, &94e2, &9710, &9758, &99fd, &9a07, &9e13, &a224, &a366, &a457, &a4e0, &bc94
l003d  = &3d
; &3d referenced 54 times by &85c1, &85e7, &85f3, &87b6, &8899, &88ad, &88b9, &88bb, &88c0, &88ca, &88cc, &88fc, &8905, &8909, &8911, &8a3b, &8a49, &8a5c, &9486, &94b3, &94e6, &9972, &997a, &9982, &9984, &9986, &9992, &999b, &999d, &99e0, &9a09, &9a12, &9a2f, &9a74, &9db4, &a228, &a36a, &a459, &a4e4, &a515, &a553, &a58c, &a616, &a6fa, &a81e, &bc32, &bc38, &bcea, &bcf6, &bcfb, &bd00, &bd0a, &be57, &be59
l003e  = &3e
; &3e referenced 47 times by &85e9, &85fd, &889b, &88ab, &88b0, &88b5, &88be, &88c7, &88d0, &88f5, &890b, &9976, &998a, &99a1, &99e2, &9a0b, &9a17, &9a2c, &9a7a, &9db6, &a192, &a22c, &a242, &a26f, &a289, &a37a, &a422, &a428, &a444, &a45b, &a4e8, &a534, &a538, &a543, &a598, &a5d2, &a5fe, &a63a, &a710, &a73a, &a758, &a782, &a81b, &bc3c, &bc44, &bced, &be5d
l003f  = &3f
; &3f referenced 47 times by &8522, &8542, &923c, &924f, &9723, &992b, &993f, &994b, &9960, &99e4, &9a0d, &9a1c, &9a29, &9a80, &9d87, &9d9a, &9d9e, &9ea0, &9ea8, &9eb3, &9eb7, &a18c, &a230, &a244, &a273, &a28b, &a35c, &a36e, &a41e, &a424, &a446, &a45d, &a4ec, &a530, &a536, &a545, &a59e, &a5cc, &a5f8, &a63c, &a716, &a734, &a75e, &a77c, &bca6, &bca8, &bcfe
l0040  = &40
; &40 referenced 34 times by &923a, &9251, &9728, &99e6, &9a0f, &9a21, &9a27, &9a86, &9d89, &9da0, &9da4, &a186, &a234, &a246, &a277, &a28f, &a357, &a370, &a41a, &a420, &a448, &a45f, &a4f0, &a52c, &a532, &a547, &a5a4, &a5c6, &a5f2, &a63e, &a71c, &a72e, &a764, &a776
l0041  = &41
; &41 referenced 23 times by &9a8c, &a180, &a238, &a248, &a27b, &a293, &a352, &a372, &a41c, &a44a, &a461, &a4f4, &a528, &a52e, &a549, &a5aa, &a5c0, &a5ec, &a640, &a722, &a728, &a76a, &a770
l0042  = &42
; &42 referenced 15 times by &a17a, &a23c, &a24a, &a27f, &a297, &a364, &a463, &a4f8, &a52a, &a54b, &a5b0, &a5ba, &a5e6, &a62b, &a642
l0043  = &43
; &43 referenced 5 times by &a164, &a16d, &a64a, &a745, &a7a2
l0044  = &44
; &44 referenced 3 times by &a648, &a743, &a79e
l0045  = &45
; &45 referenced 3 times by &a646, &a741, &a79a
l0046  = &46
; &46 referenced 3 times by &a644, &a73f, &a796
l0048  = &48
; &48 referenced 8 times by &a087, &a0a0, &a0a4, &a0ba, &a0c2, &a0ec, &a8a2, &a8cf
l0049  = &49
; &49 referenced 9 times by &a089, &a0be, &a0c6, &a0e4, &a0e6, &a0ea, &a102, &a10b, &a114
l004a  = &4a
; &4a referenced 11 times by &9e50, &9e67, &a156, &a166, &a16a, &a170, &a48c, &a496, &a4a9, &a4ae, &aacc
l004b  = &4b
; &4b referenced 23 times by &9e5e, &a350, &a355, &a35a, &a35f, &a368, &a387, &a391, &a3a0, &a3a5, &a3aa, &a3af, &a3b7, &a3bc, &a3c1, &a3c6, &a3cb, &a7f7, &a857, &a8ac, &a8c2, &aac3, &bd81
l004c  = &4c
; &4c referenced 8 times by &9e62, &a38b, &a7fb, &a85b, &a8b0, &a8ca, &aac7, &bd89
l004d  = &4d
; &4d referenced 6 times by &a897, &a8a0, &a8a4, &a8aa, &a8bc, &a8c0
l004e  = &4e
; &4e referenced 5 times by &a899, &a8a8, &a8ae, &a8c4, &a8c8
l00ff  = &ff
; &ff referenced 1 time by &987b
l01ff  = &01ff
; &01ff referenced 1 time by &8b4c
brkv   = &0202
; &0202 referenced 1 time by &8065
wrchv  = &020e
; &020e referenced 1 time by &b574
l0400  = &0400
; &0400 referenced 2 times by &8042, &946f
l0401  = &0401
; &0401 referenced 2 times by &8046, &9474
l0402  = &0402
; &0402 referenced 1 time by &8037
l0403  = &0403
; &0403 referenced 1 time by &803a
l043c  = &043c
; &043c referenced 2 times by &863d, &8667
l043d  = &043d
; &043d referenced 2 times by &8640, &866c
l0440  = &0440
; &0440 referenced 4 times by &862b, &865d, &867d, &ae3a
l0441  = &0441
; &0441 referenced 4 times by &8636, &8662, &8683, &ae3d
l047f  = &047f
; &047f referenced 1 time by &bd33
l05ff  = &05ff
; &05ff referenced 5 times by &9b0a, &9c2d, &9c30, &bdbe, &bdd6
l0600  = &0600
; &0600 referenced 10 times by &8658, &8c97, &8ca9, &8cb1, &a06a, &add3, &afc2, &b3a0, &b3af, &bebe
l6142  = &6142
; &6142 referenced 1 time by &bea1
osasci = &ffe3
; &ffe3 referenced 1 time by &bfd9
osnewl = &ffe7
; &ffe7 referenced 1 time by &bc25
oswrch = &ffee
; &ffee referenced 1 time by &b55c
osword = &fff1
; &fff1 referenced 1 time by &bc1d
osbyte = &fff4
; &fff4 referenced 2 times by &8025, &802e
oscli  = &fff7
; &fff7 referenced 1 time by &8b7a


    org &8000

.pydis_start
; BASIC v&01
; ***************************************************************************************
; Sideways ROM header — language-entry slot (3 bytes)
;
; MOS dispatches JMP &8000 on language startup.
;
; Byte 0 is &c9 (non-standard placeholder); MOS would still execute JMP &8000 on language
; startup so this ROM relies on never being asked.
;
; Reason code in A on entry:
;
; | A | Meaning                                           |
; |---|---------------------------------------------------|
; | 0 | No language available — MOS calling Tube ROM      |
; | 1 | Normal startup                                    |
; | 2 | Request next byte of softkey expansion (Electron) |
; | 3 | Request length of softkey expansion (Electron)    |
.language_entry
    equb &c9, &01, &f0                                                ; 8000: c9 01 f0    ...   
; ***************************************************************************************
; Service-entry slot (3 bytes)
;
; MOS calls JMP &8003 for service-call dispatch — unrecognised * commands, OSWORDs,
; OSBYTEs, *HELP, filing-system init / select, paged-ROM scans, and many other events.
; The reason code arrives in A.
;
; Byte 0 is &1f (non-standard); a ROM that never wants to handle service calls would set
; rom_type bit 7 clear and use a placeholder here.
.service_entry
    equb &1f, &60, &ea                                                ; 8003: 1f 60 ea    .`.   
; ***************************************************************************************
; ROM identification
;
; Six descriptive fields that follow the entry-point JMPs: ROM type flag byte,
; copyright-string offset, binary version, title string, optional version string, and
; copyright string. The MOS uses these for identification, dispatch-table lookup, and the
; (C)-prefix validity check.
.rom_type
; ***************************************************************************************
; ROM type byte
;
; | Bit | Value | Meaning                         |
; |-----|-------|---------------------------------|
; | 7   | 0     | No service entry                |
; | 6   | 1     | Language entry present          |
; | 5   | 1     | Tube relocation address present |
; | 4   | 0     | No Electron firmkey             |
; | 3-0 | 0000  | Processor: 6502 BASIC           |
    equb %01100000                                                    ; 8006: 60          `        ; ROM type
.copyright_offset
    equb copyright - language_entry                                   ; 8007: 0e          .        ; Offset of NUL preceding copyright (= &0e → copyright at &800e)
.binary_version
    equb &01                                                          ; 8008: 01          .        ; Binary version: &01 (informational, not used by MOS)
.title
    equs "BASIC"                                                      ; 8009: 42 41 53... BAS...
.copyright
    equb &00                                                          ; 800e: 00          .        ; NUL preceding copyright string
.copyright_string
    equs "(C)1982 Acorn", &0a, &0d                                    ; 800f: 28 43 29... (C)...
    equb &00                                                          ; 801e: 00          .        ; NUL terminator
.tube_reloc_addr
    equb &00, &80, &00, &00                                           ; 801f: 00 80 00... ......   ; Tube relocation address (32-bit LE) — where the ROM body relocates on a Tube co-processor
    lda #osbyte_read_himem                                            ; 8023: a9 84       ..    
    jsr osbyte                                                        ; 8025: 20 f4 ff     ..      ; Read top of available user RAM (HIMEM)
    stx l0006                                                         ; 8028: 86 06       ..       ; X and Y contain the address of HIMEM (low, high)
    sty l0007                                                         ; 802a: 84 07       ..    
    lda #osbyte_read_oshwm                                            ; 802c: a9 83       ..    
    jsr osbyte                                                        ; 802e: 20 f4 ff     ..      ; Read top of operating system RAM address (OSHWM)
    sty l0018                                                         ; 8031: 84 18       ..       ; X and Y contain the address of OSHWM (low, high)
    ldx #0                                                            ; 8033: a2 00       ..    
    stx l001f                                                         ; 8035: 86 1f       ..    
    stx l0402                                                         ; 8037: 8e 02 04    ...   
    stx l0403                                                         ; 803a: 8e 03 04    ...   
    dex                                                               ; 803d: ca          .     
    stx l0023                                                         ; 803e: 86 23       .#    
    ldx #&0a                                                          ; 8040: a2 0a       ..    
    stx l0400                                                         ; 8042: 8e 00 04    ...   
    dex                                                               ; 8045: ca          .     
    stx l0401                                                         ; 8046: 8e 01 04    ...   
    lda #1                                                            ; 8049: a9 01       ..    
    and l0011                                                         ; 804b: 25 11       %.    
    ora l000d                                                         ; 804d: 05 0d       ..    
    ora l000e                                                         ; 804f: 05 0e       ..    
    ora l000f                                                         ; 8051: 05 0f       ..    
    ora l0010                                                         ; 8053: 05 10       ..    
    bne c8063                                                         ; 8055: d0 0c       ..    
    lda #&41 ; 'A'                                                    ; 8057: a9 41       .A    
    sta l000d                                                         ; 8059: 85 0d       ..    
    lda #&52 ; 'R'                                                    ; 805b: a9 52       .R    
    sta l000e                                                         ; 805d: 85 0e       ..    
    lda #&57 ; 'W'                                                    ; 805f: a9 57       .W    
    sta l000f                                                         ; 8061: 85 0f       ..    
; &8063 referenced 1 time by &8055
.c8063
    lda #2                                                            ; 8063: a9 02       ..    
    sta brkv                                                          ; 8065: 8d 02 02    ...   
    lda #&b4                                                          ; 8068: a9 b4       ..    
    sta brkv+1                                                        ; 806a: 8d 03 02    ...   
    cli                                                               ; 806d: 58          X     
    jmp c8add                                                         ; 806e: 4c dd 8a    L..   
    equs "AND"                                                        ; 8071: 41 4e 44    AND   
    equb &80, &00                                                     ; 8074: 80 00       ..    
    equs "ABS"                                                        ; 8076: 41 42 53    ABS   
    equb &94, &00                                                     ; 8079: 94 00       ..    
    equs "ACS"                                                        ; 807b: 41 43 53    ACS   
    equb &95, &00                                                     ; 807e: 95 00       ..    
    equs "ADVAL"                                                      ; 8080: 41 44 56... ADV...
    equb &96, &00                                                     ; 8085: 96 00       ..    
    equs "ASC"                                                        ; 8087: 41 53 43    ASC   
    equb &97, &00                                                     ; 808a: 97 00       ..    
    equs "ASN"                                                        ; 808c: 41 53 4e    ASN   
    equb &98, &00                                                     ; 808f: 98 00       ..    
    equs "ATN"                                                        ; 8091: 41 54 4e    ATN   
    equb &99, &00                                                     ; 8094: 99 00       ..    
    equs "AUTO"                                                       ; 8096: 41 55 54... AUT...
    equb &c6, &10                                                     ; 809a: c6 10       ..    
    equs "BGET"                                                       ; 809c: 42 47 45... BGE...
    equb &9a, &01                                                     ; 80a0: 9a 01       ..    
    equs "BPUT"                                                       ; 80a2: 42 50 55... BPU...
    equb &d5, &03                                                     ; 80a6: d5 03       ..    
    equs "COLOUR"                                                     ; 80a8: 43 4f 4c... COL...
    equb &fb, &02                                                     ; 80ae: fb 02       ..    
    equs "CALL"                                                       ; 80b0: 43 41 4c... CAL...
    equb &d6, &02                                                     ; 80b4: d6 02       ..    
    equs "CHAIN"                                                      ; 80b6: 43 48 41... CHA...
    equb &d7, &02                                                     ; 80bb: d7 02       ..    
    equs "CHR$"                                                       ; 80bd: 43 48 52... CHR...
    equb &bd, &00                                                     ; 80c1: bd 00       ..    
    equs "CLEAR"                                                      ; 80c3: 43 4c 45... CLE...
    equb &d8, &01                                                     ; 80c8: d8 01       ..    
    equs "CLOSE"                                                      ; 80ca: 43 4c 4f... CLO...
    equb &d9, &03                                                     ; 80cf: d9 03       ..    
    equs "CLG"                                                        ; 80d1: 43 4c 47    CLG   
    equb &da, &01                                                     ; 80d4: da 01       ..    
    equs "CLS"                                                        ; 80d6: 43 4c 53    CLS   
    equb &db, &01                                                     ; 80d9: db 01       ..    
    equs "COS"                                                        ; 80db: 43 4f 53    COS   
    equb &9b, &00                                                     ; 80de: 9b 00       ..    
    equs "COUNT"                                                      ; 80e0: 43 4f 55... COU...
    equb &9c, &01                                                     ; 80e5: 9c 01       ..    
    equs "DATA"                                                       ; 80e7: 44 41 54... DAT...
    equb &dc                                                          ; 80eb: dc          .     
    equs " DEG"                                                       ; 80ec: 20 44 45...  DE...
    equb &9d, &00                                                     ; 80f0: 9d 00       ..    
    equs "DEF"                                                        ; 80f2: 44 45 46    DEF   
    equb &dd, &00                                                     ; 80f5: dd 00       ..    
    equs "DELETE"                                                     ; 80f7: 44 45 4c... DEL...
    equb &c7, &10                                                     ; 80fd: c7 10       ..    
    equs "DIV"                                                        ; 80ff: 44 49 56    DIV   
    equb &81, &00                                                     ; 8102: 81 00       ..    
    equs "DIM"                                                        ; 8104: 44 49 4d    DIM   
    equb &de, &02                                                     ; 8107: de 02       ..    
    equs "DRAW"                                                       ; 8109: 44 52 41... DRA...
    equb &df, &02                                                     ; 810d: df 02       ..    
    equs "ENDPROC"                                                    ; 810f: 45 4e 44... END...
    equb &e1, &01                                                     ; 8116: e1 01       ..    
    equs "END"                                                        ; 8118: 45 4e 44    END   
    equb &e0, &01                                                     ; 811b: e0 01       ..    
    equs "ENVELOPE"                                                   ; 811d: 45 4e 56... ENV...
    equb &e2, &02                                                     ; 8125: e2 02       ..    
    equs "ELSE"                                                       ; 8127: 45 4c 53... ELS...
    equb &8b, &14                                                     ; 812b: 8b 14       ..    
    equs "EVAL"                                                       ; 812d: 45 56 41... EVA...
    equb &a0, &00                                                     ; 8131: a0 00       ..    
    equs "ERL"                                                        ; 8133: 45 52 4c    ERL   
    equb &9e, &01                                                     ; 8136: 9e 01       ..    
    equs "ERROR"                                                      ; 8138: 45 52 52... ERR...
    equb &85, &04                                                     ; 813d: 85 04       ..    
    equs "EOF"                                                        ; 813f: 45 4f 46    EOF   
    equb &c5, &01                                                     ; 8142: c5 01       ..    
    equs "EOR"                                                        ; 8144: 45 4f 52    EOR   
    equb &82, &00                                                     ; 8147: 82 00       ..    
    equs "ERR"                                                        ; 8149: 45 52 52    ERR   
    equb &9f, &01                                                     ; 814c: 9f 01       ..    
    equs "EXP"                                                        ; 814e: 45 58 50    EXP   
    equb &a1, &00                                                     ; 8151: a1 00       ..    
    equs "EXT"                                                        ; 8153: 45 58 54    EXT   
    equb &a2, &01                                                     ; 8156: a2 01       ..    
    equs "FOR"                                                        ; 8158: 46 4f 52    FOR   
    equb &e3, &02                                                     ; 815b: e3 02       ..    
    equs "FALSE"                                                      ; 815d: 46 41 4c... FAL...
    equb &a3, &01, &46, &4e, &a4, &08                                 ; 8162: a3 01 46... ..F...
    equs "GOTO"                                                       ; 8168: 47 4f 54... GOT...
    equb &e5, &12                                                     ; 816c: e5 12       ..    
    equs "GET$"                                                       ; 816e: 47 45 54... GET...
    equb &be, &00                                                     ; 8172: be 00       ..    
    equs "GET"                                                        ; 8174: 47 45 54    GET   
    equb &a5, &00                                                     ; 8177: a5 00       ..    
    equs "GOSUB"                                                      ; 8179: 47 4f 53... GOS...
    equb &e4, &12                                                     ; 817e: e4 12       ..    
    equs "GCOL"                                                       ; 8180: 47 43 4f... GCO...
    equb &e6, &02                                                     ; 8184: e6 02       ..    
    equs "HIMEM"                                                      ; 8186: 48 49 4d... HIM...
    equb &93                                                          ; 818b: 93          .     
    equs "CINPUT"                                                     ; 818c: 43 49 4e... CIN...
    equb &e8, &02, &49, &46, &e7, &02                                 ; 8192: e8 02 49... ..I...
    equs "INKEY$"                                                     ; 8198: 49 4e 4b... INK...
    equb &bf, &00                                                     ; 819e: bf 00       ..    
    equs "INKEY"                                                      ; 81a0: 49 4e 4b... INK...
    equb &a6, &00                                                     ; 81a5: a6 00       ..    
    equs "INT"                                                        ; 81a7: 49 4e 54    INT   
    equb &a8, &00                                                     ; 81aa: a8 00       ..    
    equs "INSTR("                                                     ; 81ac: 49 4e 53... INS...
    equb &a7, &00                                                     ; 81b2: a7 00       ..    
    equs "LIST"                                                       ; 81b4: 4c 49 53... LIS...
    equb &c9, &10                                                     ; 81b8: c9 10       ..    
    equs "LINE"                                                       ; 81ba: 4c 49 4e... LIN...
    equb &86, &00                                                     ; 81be: 86 00       ..    
    equs "LOAD"                                                       ; 81c0: 4c 4f 41... LOA...
    equb &c8, &02                                                     ; 81c4: c8 02       ..    
    equs "LOMEM"                                                      ; 81c6: 4c 4f 4d... LOM...
    equb &92                                                          ; 81cb: 92          .     
    equs "CLOCAL"                                                     ; 81cc: 43 4c 4f... CLO...
    equb &ea, &02                                                     ; 81d2: ea 02       ..    
    equs "LEFT$("                                                     ; 81d4: 4c 45 46... LEF...
    equb &c0, &00                                                     ; 81da: c0 00       ..    
    equs "LEN"                                                        ; 81dc: 4c 45 4e    LEN   
    equb &a9, &00                                                     ; 81df: a9 00       ..    
    equs "LET"                                                        ; 81e1: 4c 45 54    LET   
    equb &e9, &04                                                     ; 81e4: e9 04       ..    
    equs "LOG"                                                        ; 81e6: 4c 4f 47    LOG   
    equb &ab, &00, &4c, &4e, &aa, &00                                 ; 81e9: ab 00 4c... ..L...
    equs "MID$("                                                      ; 81ef: 4d 49 44... MID...
    equb &c1, &00                                                     ; 81f4: c1 00       ..    
    equs "MODE"                                                       ; 81f6: 4d 4f 44... MOD...
    equb &eb, &02                                                     ; 81fa: eb 02       ..    
    equs "MOD"                                                        ; 81fc: 4d 4f 44    MOD   
    equb &83, &00                                                     ; 81ff: 83 00       ..    
    equs "MOVE"                                                       ; 8201: 4d 4f 56... MOV...
    equb &ec, &02                                                     ; 8205: ec 02       ..    
    equs "NEXT"                                                       ; 8207: 4e 45 58... NEX...
    equb &ed, &02                                                     ; 820b: ed 02       ..    
    equs "NEW"                                                        ; 820d: 4e 45 57    NEW   
    equb &ca, &01                                                     ; 8210: ca 01       ..    
    equs "NOT"                                                        ; 8212: 4e 4f 54    NOT   
    equb &ac, &00                                                     ; 8215: ac 00       ..    
    equs "OLD"                                                        ; 8217: 4f 4c 44    OLD   
    equb &cb, &01, &4f, &4e, &ee, &02                                 ; 821a: cb 01 4f... ..O...
    equs "OFF"                                                        ; 8220: 4f 46 46    OFF   
    equb &87, &00, &4f, &52, &84, &00                                 ; 8223: 87 00 4f... ..O...
    equs "OPENIN"                                                     ; 8229: 4f 50 45... OPE...
    equb &8e, &00                                                     ; 822f: 8e 00       ..    
    equs "OPENOUT"                                                    ; 8231: 4f 50 45... OPE...
    equb &ae, &00                                                     ; 8238: ae 00       ..    
    equs "OPENUP"                                                     ; 823a: 4f 50 45... OPE...
    equb &ad, &00                                                     ; 8240: ad 00       ..    
    equs "OSCLI"                                                      ; 8242: 4f 53 43... OSC...
    equb &ff, &02                                                     ; 8247: ff 02       ..    
    equs "PRINT"                                                      ; 8249: 50 52 49... PRI...
    equb &f1, &02                                                     ; 824e: f1 02       ..    
    equs "PAGE"                                                       ; 8250: 50 41 47... PAG...
    equb &90                                                          ; 8254: 90          .     
    equs "CPTR"                                                       ; 8255: 43 50 54... CPT...
    equb &8f                                                          ; 8259: 8f          .     
    equs "CPI"                                                        ; 825a: 43 50 49    CPI   
    equb &af, &01                                                     ; 825d: af 01       ..    
    equs "PLOT"                                                       ; 825f: 50 4c 4f... PLO...
    equb &f0, &02                                                     ; 8263: f0 02       ..    
    equs "POINT("                                                     ; 8265: 50 4f 49... POI...
    equb &b0, &00                                                     ; 826b: b0 00       ..    
    equs "PROC"                                                       ; 826d: 50 52 4f... PRO...
    equb &f2, &0a                                                     ; 8271: f2 0a       ..    
    equs "POS"                                                        ; 8273: 50 4f 53    POS   
    equb &b1, &01                                                     ; 8276: b1 01       ..    
    equs "RETURN"                                                     ; 8278: 52 45 54... RET...
    equb &f8, &01                                                     ; 827e: f8 01       ..    
    equs "REPEAT"                                                     ; 8280: 52 45 50... REP...
    equb &f5, &00                                                     ; 8286: f5 00       ..    
    equs "REPORT"                                                     ; 8288: 52 45 50... REP...
    equb &f6, &01                                                     ; 828e: f6 01       ..    
    equs "READ"                                                       ; 8290: 52 45 41... REA...
    equb &f3, &02                                                     ; 8294: f3 02       ..    
    equs "REM"                                                        ; 8296: 52 45 4d    REM   
    equb &f4                                                          ; 8299: f4          .     
    equs " RUN"                                                       ; 829a: 20 52 55...  RU...
    equb &f9, &01                                                     ; 829e: f9 01       ..    
    equs "RAD"                                                        ; 82a0: 52 41 44    RAD   
    equb &b2, &00                                                     ; 82a3: b2 00       ..    
    equs "RESTORE"                                                    ; 82a5: 52 45 53... RES...
    equb &f7, &12                                                     ; 82ac: f7 12       ..    
    equs "RIGHT$("                                                    ; 82ae: 52 49 47... RIG...
    equb &c2, &00                                                     ; 82b5: c2 00       ..    
    equs "RND"                                                        ; 82b7: 52 4e 44    RND   
    equb &b3, &01                                                     ; 82ba: b3 01       ..    
    equs "RENUMBER"                                                   ; 82bc: 52 45 4e... REN...
    equb &cc, &10                                                     ; 82c4: cc 10       ..    
    equs "STEP"                                                       ; 82c6: 53 54 45... STE...
    equb &88, &00                                                     ; 82ca: 88 00       ..    
    equs "SAVE"                                                       ; 82cc: 53 41 56... SAV...
    equb &cd, &02                                                     ; 82d0: cd 02       ..    
    equs "SGN"                                                        ; 82d2: 53 47 4e    SGN   
    equb &b4, &00                                                     ; 82d5: b4 00       ..    
    equs "SIN"                                                        ; 82d7: 53 49 4e    SIN   
    equb &b5, &00                                                     ; 82da: b5 00       ..    
    equs "SQR"                                                        ; 82dc: 53 51 52    SQR   
; &82df referenced 1 time by &8bb2
.l82df
    equb &b6, &00                                                     ; 82df: b6 00       ..    
    equs "SPC"                                                        ; 82e1: 53 50 43    SPC   
    equb &89, &00                                                     ; 82e4: 89 00       ..    
    equs "STR$"                                                       ; 82e6: 53 54 52... STR...
    equb &c3, &00                                                     ; 82ea: c3 00       ..    
    equs "STRING$("                                                   ; 82ec: 53 54 52... STR...
    equb &c4, &00                                                     ; 82f4: c4 00       ..    
    equs "SOUND"                                                      ; 82f6: 53 4f 55... SOU...
    equb &d4, &02                                                     ; 82fb: d4 02       ..    
    equs "STOP"                                                       ; 82fd: 53 54 4f... STO...
    equb &fa, &01                                                     ; 8301: fa 01       ..    
    equs "TAN"                                                        ; 8303: 54 41 4e    TAN   
    equb &b7, &00                                                     ; 8306: b7 00       ..    
    equs "THEN"                                                       ; 8308: 54 48 45... THE...
    equb &8c, &14, &54, &4f, &b8, &00                                 ; 830c: 8c 14 54... ..T...
    equs "TAB("                                                       ; 8312: 54 41 42... TAB...
    equb &8a, &00                                                     ; 8316: 8a 00       ..    
    equs "TRACE"                                                      ; 8318: 54 52 41... TRA...
    equb &fc, &12                                                     ; 831d: fc 12       ..    
    equs "TIME"                                                       ; 831f: 54 49 4d... TIM...
    equb &91                                                          ; 8323: 91          .     
    equs "CTRUE"                                                      ; 8324: 43 54 52... CTR...
    equb &b9, &01                                                     ; 8329: b9 01       ..    
    equs "UNTIL"                                                      ; 832b: 55 4e 54... UNT...
    equb &fd, &02                                                     ; 8330: fd 02       ..    
    equs "USR"                                                        ; 8332: 55 53 52    USR   
    equb &ba, &00                                                     ; 8335: ba 00       ..    
    equs "VDU"                                                        ; 8337: 56 44 55    VDU   
    equb &ef, &02                                                     ; 833a: ef 02       ..    
    equs "VAL"                                                        ; 833c: 56 41 4c    VAL   
    equb &bb, &00                                                     ; 833f: bb 00       ..    
    equs "VPOS"                                                       ; 8341: 56 50 4f... VPO...
    equb &bc, &01                                                     ; 8345: bc 01       ..    
    equs "WIDTH"                                                      ; 8347: 57 49 44... WID...
    equb &fe, &02                                                     ; 834c: fe 02       ..    
.sub_c834e
; &8351 referenced 1 time by &8bb7
l8351 = sub_c834e+3
    equs "PAGE"                                                       ; 834e: 50 41 47... PAG...
    equb &d0, &00                                                     ; 8352: d0 00       ..    
    equs "PTR"                                                        ; 8354: 50 54 52    PTR   
    equb &cf, &00                                                     ; 8357: cf 00       ..    
    equs "TIME"                                                       ; 8359: 54 49 4d... TIM...
    equb &d1, &00                                                     ; 835d: d1 00       ..    
    equs "LOMEM"                                                      ; 835f: 4c 4f 4d... LOM...
    equb &d2, &00                                                     ; 8364: d2 00       ..    
    equs "HIMEM"                                                      ; 8366: 48 49 4d... HIM...
    equb &d3, &00, &78, &47, &c0, &b4, &fc, &03, &6a, &d4, &33, &9e   ; 836b: d3 00 78... ..x...
    equb &da, &07, &6f, &8d, &f7, &c2, &9f, &a6, &e9, &91, &46, &ca   ; 8377: da 07 6f... ..o...
    equb &95, &b9, &ad, &e2, &78, &d1, &fe, &a8, &d1, &80, &7c, &cb   ; 8383: 95 b9 ad... ......
    equb &41, &6d, &b1, &49, &88, &98, &b4, &be, &dc, &c4, &d2, &2f   ; 838f: 41 6d b1... Am....
    equb &76, &bd, &bf, &26, &cc, &39, &ee, &94, &c2, &b8, &ac, &31   ; 839b: 76 bd bf... v.....
    equb &24, &9c, &da, &b6, &a3, &f3, &2a, &30, &83, &c9             ; 83a7: 24 9c da... $.....
    equs "o]LX"                                                       ; 83b1: 6f 5d 4c... o]L...
    equb &d2, &2a, &8d, &99, &bd, &c4                                 ; 83b5: d2 2a 8d... .*....
    equs "}}/"                                                        ; 83bb: 7d 7d 2f    }}/   
.sub_c83be
; &8450 referenced 1 time by &85f5
l8450 = sub_c83be+146
    equb &e8, &c8, &56, &72, &c4, &88, &cc, &7a, &c2, &44, &e4, &23   ; 83be: e8 c8 56... ..V...
    equb &9a, &e4, &95, &15, &2f, &f1, &9a, &04, &1f, &7d, &e4, &e4   ; 83ca: 9a e4 95... ......
    equb &e6, &b6, &11, &d0, &8e, &95, &b1, &a0, &c2, &bf, &bf, &ae   ; 83d6: e6 b6 11... ......
    equb &ae, &ae, &af, &ad, &a8, &ab, &ac, &a8, &a9, &bf, &a9, &ae   ; 83e2: ae ae af... ......
    equb &ab, &af, &af, &ab, &aa, &bf, &ae, &b1, &af, &ac, &ac, &ac   ; 83ee: ab af af... ......
    equb &ae, &a7, &ab, &ac, &bf, &bf, &ab, &ab, &ab, &ab, &af, &ab   ; 83fa: ae a7 ab... ......
    equb &a9, &a7, &a6, &ae, &ac, &ab, &ac, &ab, &b3, &af, &b0, &af   ; 8406: a9 a7 a6... ......
    equb &b0, &af, &b0, &b0, &ac, &90, &8f, &bf, &b5, &8a, &8a, &8f   ; 8412: b0 af b0... ......
    equb &be, &98, &bf, &92, &92, &92, &92, &b4, &bf, &8e, &bf, &92   ; 841e: be 98 bf... ......
    equb &bf, &8e, &8e, &8b, &8b, &91, &93, &8a, &93, &b4, &b7, &b8   ; 842a: bf 8e 8e... ......
    equb &b8, &93, &98, &ba, &8b, &93, &93, &93, &b6, &b9, &94, &93   ; 8436: b8 93 98... ......
    equb &8d, &93, &bb, &8b, &bb, &bf, &ba, &b8, &bd, &8a, &93, &92   ; 8442: 8d 93 bb... ......
    equb &bb, &b4, &be, &4b, &83, &84, &89, &96, &b8, &b9, &d8, &d9   ; 844e: bb b4 be... ......
    equb &f0, &01, &10, &81, &90, &89, &93, &a3, &a4, &a9             ; 845a: f0 01 10... ......
    equs "89x"                                                        ; 8464: 38 39 78    89x   
    equb &01, &13                                                     ; 8467: 01 13       ..    
    equs "!cs"                                                        ; 8469: 21 63 73    !cs   
    equb &b1, &a9, &c5, &0c, &c3, &d3, &c4, &f2, &41, &83, &b0, &81   ; 846c: b1 a9 c5... ......
    equs "Clr"                                                        ; 8478: 43 6c 72    Clr   
.sub_c847b
; &848a referenced 1 time by &85fa
l848a = sub_c847b+15
    equb &ec, &f2, &a3, &c3, &18, &19, &34, &b0, &72, &98, &99, &81   ; 847b: ec f2 a3... ......
    equb &98, &99, &14, &35, &0a, &0d, &0d, &0d, &0d, &10, &10        ; 8487: 98 99 14... ......
    equs "%%9AAAAJJLLLPPRSSS"                                         ; 8492: 25 25 39... %%9...
    equb &08, &08, &08, &09, &09, &0a, &0a, &0a, &05, &15, &3e, &04   ; 84a4: 08 08 08... ......
    equb &0d, &30, &4c, &06                                           ; 84b0: 0d 30 4c... .0L...
    equs "2II"                                                        ; 84b4: 32 49 49    2II   
    equb &10, &25, &0e, &0e, &09                                      ; 84b7: 10 25 0e... .%....
    equs ")*00NNN>"                                                   ; 84bc: 29 2a 30... )*0...
; &84c4 referenced 1 time by &8620
.l84c4
    equb &16, &00, &18, &d8, &58, &b8, &ca, &88, &e8, &c8, &ea, &48   ; 84c4: 16 00 18... ......
    equb &08                                                          ; 84d0: 08          .     
    equs "h(@`8"                                                      ; 84d1: 68 28 40... h(@...
    equb &f8, &78, &aa, &a8, &ba, &8a, &9a, &98, &90, &b0, &f0, &30   ; 84d6: f8 78 aa... .x....
    equb &d0, &10                                                     ; 84e2: d0 10       ..    
    equs "Pp!A"                                                       ; 84e4: 50 70 21... Pp!...
    equb &01, &61, &c1, &a1, &e1, &06                                 ; 84e8: 01 61 c1... .a....
    equs "F&f"                                                        ; 84ee: 46 26 66    F&f   
    equb &c6, &e6, &e0, &c0                                           ; 84f1: c6 e6 e0... ......
    equs " L "                                                        ; 84f5: 20 4c 20     L    
    equb &a2, &a0, &81, &86, &84                                      ; 84f8: a2 a0 81... ......
; &84fd referenced 1 time by &850d
.loop_c84fd
    lda #&ff                                                          ; 84fd: a9 ff       ..    
    sta l0028                                                         ; 84ff: 85 28       .(    
    jmp c8ba3                                                         ; 8501: 4c a3 8b    L..   
; &8504 referenced 1 time by &8b44
.c8504
    lda #3                                                            ; 8504: a9 03       ..    
    sta l0028                                                         ; 8506: 85 28       .(    
; &8508 referenced 1 time by &85a2
.c8508
    jsr c8a97                                                         ; 8508: 20 97 8a     ..   
    cmp #&5d ; ']'                                                    ; 850b: c9 5d       .]    
    beq loop_c84fd                                                    ; 850d: f0 ee       ..    
    jsr c986d                                                         ; 850f: 20 6d 98     m.   
    dec l000a                                                         ; 8512: c6 0a       ..    
    jsr sub_c85ba                                                     ; 8514: 20 ba 85     ..   
    dec l000a                                                         ; 8517: c6 0a       ..    
    lda l0028                                                         ; 8519: a5 28       .(    
    lsr a                                                             ; 851b: 4a          J     
    bcc c857e                                                         ; 851c: 90 60       .`    
    lda l001e                                                         ; 851e: a5 1e       ..    
    adc #4                                                            ; 8520: 69 04       i.    
    sta l003f                                                         ; 8522: 85 3f       .?    
    lda l0038                                                         ; 8524: a5 38       .8    
    jsr sub_cb545                                                     ; 8526: 20 45 b5     E.   
    lda l0037                                                         ; 8529: a5 37       .7    
    jsr sub_cb562                                                     ; 852b: 20 62 b5     b.   
    ldx #&fc                                                          ; 852e: a2 fc       ..    
    ldy l0039                                                         ; 8530: a4 39       .9    
    bpl c8536                                                         ; 8532: 10 02       ..    
    ldy l0036                                                         ; 8534: a4 36       .6    
; &8536 referenced 1 time by &8532
.c8536
    sty l0038                                                         ; 8536: 84 38       .8    
    beq c8556                                                         ; 8538: f0 1c       ..    
    ldy #0                                                            ; 853a: a0 00       ..    
; &853c referenced 1 time by &8554
.loop_c853c
    inx                                                               ; 853c: e8          .     
    bne c854c                                                         ; 853d: d0 0d       ..    
    jsr sub_cbc25                                                     ; 853f: 20 25 bc     %.   
    ldx l003f                                                         ; 8542: a6 3f       .?    
; &8544 referenced 1 time by &8548
.loop_c8544
    jsr cb565                                                         ; 8544: 20 65 b5     e.   
    dex                                                               ; 8547: ca          .     
    bne loop_c8544                                                    ; 8548: d0 fa       ..    
    ldx #&fd                                                          ; 854a: a2 fd       ..    
; &854c referenced 1 time by &853d
.c854c
    lda (l003a),y                                                     ; 854c: b1 3a       .:    
    jsr sub_cb562                                                     ; 854e: 20 62 b5     b.   
    iny                                                               ; 8551: c8          .     
    dec l0038                                                         ; 8552: c6 38       .8    
    bne loop_c853c                                                    ; 8554: d0 e6       ..    
; &8556 referenced 2 times by &8538, &8562
.c8556
    inx                                                               ; 8556: e8          .     
    bpl c8565                                                         ; 8557: 10 0c       ..    
    jsr cb565                                                         ; 8559: 20 65 b5     e.   
    jsr cb558                                                         ; 855c: 20 58 b5     X.   
    jsr cb558                                                         ; 855f: 20 58 b5     X.   
    jmp c8556                                                         ; 8562: 4c 56 85    LV.   
; &8565 referenced 1 time by &8557
.c8565
    ldy #0                                                            ; 8565: a0 00       ..    
; &8567 referenced 1 time by &8575
.loop_c8567
    lda (l000b),y                                                     ; 8567: b1 0b       ..    
    cmp #&3a ; ':'                                                    ; 8569: c9 3a       .:    
    beq c8577                                                         ; 856b: f0 0a       ..    
    cmp #&0d                                                          ; 856d: c9 0d       ..    
    beq c857b                                                         ; 856f: f0 0a       ..    
; &8571 referenced 1 time by &8579
.loop_c8571
    jsr sub_cb50e                                                     ; 8571: 20 0e b5     ..   
    iny                                                               ; 8574: c8          .     
    bne loop_c8567                                                    ; 8575: d0 f0       ..    
; &8577 referenced 1 time by &856b
.c8577
    cpy l000a                                                         ; 8577: c4 0a       ..    
    bcc loop_c8571                                                    ; 8579: 90 f6       ..    
; &857b referenced 1 time by &856f
.c857b
    jsr sub_cbc25                                                     ; 857b: 20 25 bc     %.   
; &857e referenced 1 time by &851c
.c857e
    ldy l000a                                                         ; 857e: a4 0a       ..    
    dey                                                               ; 8580: 88          .     
; &8581 referenced 1 time by &858a
.loop_c8581
    iny                                                               ; 8581: c8          .     
    lda (l000b),y                                                     ; 8582: b1 0b       ..    
    cmp #&3a ; ':'                                                    ; 8584: c9 3a       .:    
    beq c858c                                                         ; 8586: f0 04       ..    
    cmp #&0d                                                          ; 8588: c9 0d       ..    
    bne loop_c8581                                                    ; 858a: d0 f5       ..    
; &858c referenced 1 time by &8586
.c858c
    jsr sub_c9859                                                     ; 858c: 20 59 98     Y.   
    dey                                                               ; 858f: 88          .     
    lda (l000b),y                                                     ; 8590: b1 0b       ..    
    cmp #&3a ; ':'                                                    ; 8592: c9 3a       .:    
    beq c85a2                                                         ; 8594: f0 0c       ..    
    lda l000c                                                         ; 8596: a5 0c       ..    
    cmp #7                                                            ; 8598: c9 07       ..    
    bne c859f                                                         ; 859a: d0 03       ..    
    jmp c8af6                                                         ; 859c: 4c f6 8a    L..   
; &859f referenced 1 time by &859a
.c859f
    jsr sub_c9890                                                     ; 859f: 20 90 98     ..   
; &85a2 referenced 1 time by &8594
.c85a2
    jmp c8508                                                         ; 85a2: 4c 08 85    L..   
; &85a5 referenced 1 time by &85d1
.loop_c85a5
    jsr sub_c9582                                                     ; 85a5: 20 82 95     ..   
    beq c8604                                                         ; 85a8: f0 5a       .Z    
    bcs c8604                                                         ; 85aa: b0 58       .X    
    jsr sub_cbd94                                                     ; 85ac: 20 94 bd     ..   
    jsr sub_cae3a                                                     ; 85af: 20 3a ae     :.   
    sta l0027                                                         ; 85b2: 85 27       .'    
    jsr sub_cb4b4                                                     ; 85b4: 20 b4 b4     ..   
    jsr sub_c8827                                                     ; 85b7: 20 27 88     '.   
; &85ba referenced 1 time by &8514
.sub_c85ba
    ldx #3                                                            ; 85ba: a2 03       ..    
    jsr c8a97                                                         ; 85bc: 20 97 8a     ..   
    ldy #0                                                            ; 85bf: a0 00       ..    
    sty l003d                                                         ; 85c1: 84 3d       .=    
    cmp #&3a ; ':'                                                    ; 85c3: c9 3a       .:    
    beq c862b                                                         ; 85c5: f0 64       .d    
    cmp #&0d                                                          ; 85c7: c9 0d       ..    
    beq c862b                                                         ; 85c9: f0 60       .`    
    cmp #&5c ; '\'                                                    ; 85cb: c9 5c       .\    
    beq c862b                                                         ; 85cd: f0 5c       .\    
    cmp #&2e ; '.'                                                    ; 85cf: c9 2e       ..    
    beq loop_c85a5                                                    ; 85d1: f0 d2       ..    
    dec l000a                                                         ; 85d3: c6 0a       ..    
; &85d5 referenced 1 time by &85ef
.loop_c85d5
    ldy l000a                                                         ; 85d5: a4 0a       ..    
    inc l000a                                                         ; 85d7: e6 0a       ..    
    lda (l000b),y                                                     ; 85d9: b1 0b       ..    
    bmi c8607                                                         ; 85db: 30 2a       0*    
    cmp #&20 ; ' '                                                    ; 85dd: c9 20       .     
    beq c85f1                                                         ; 85df: f0 10       ..    
    ldy #5                                                            ; 85e1: a0 05       ..    
    asl a                                                             ; 85e3: 0a          .     
    asl a                                                             ; 85e4: 0a          .     
    asl a                                                             ; 85e5: 0a          .     
; &85e6 referenced 1 time by &85ec
.loop_c85e6
    asl a                                                             ; 85e6: 0a          .     
    rol l003d                                                         ; 85e7: 26 3d       &=    
    rol l003e                                                         ; 85e9: 26 3e       &>    
    dey                                                               ; 85eb: 88          .     
    bne loop_c85e6                                                    ; 85ec: d0 f8       ..    
    dex                                                               ; 85ee: ca          .     
    bne loop_c85d5                                                    ; 85ef: d0 e4       ..    
; &85f1 referenced 1 time by &85df
.c85f1
    ldx #&3a ; ':'                                                    ; 85f1: a2 3a       .:    
    lda l003d                                                         ; 85f3: a5 3d       .=    
; &85f5 referenced 1 time by &8602
.loop_c85f5
    cmp l8450,x                                                       ; 85f5: dd 50 84    .P.   
    bne c8601                                                         ; 85f8: d0 07       ..    
    ldy l848a,x                                                       ; 85fa: bc 8a 84    ...   
    cpy l003e                                                         ; 85fd: c4 3e       .>    
    beq c8620                                                         ; 85ff: f0 1f       ..    
; &8601 referenced 1 time by &85f8
.c8601
    dex                                                               ; 8601: ca          .     
    bne loop_c85f5                                                    ; 8602: d0 f1       ..    
; &8604 referenced 4 times by &85a8, &85aa, &8615, &861e
.c8604
    jmp c982a                                                         ; 8604: 4c 2a 98    L*.   
; &8607 referenced 1 time by &85db
.c8607
    ldx #&22                                                          ; 8607: a2 22       ."    
    cmp #&80                                                          ; 8609: c9 80       ..    
    beq c8620                                                         ; 860b: f0 13       ..    
    inx                                                               ; 860d: e8          .     
    cmp #&82                                                          ; 860e: c9 82       ..    
    beq c8620                                                         ; 8610: f0 0e       ..    
    inx                                                               ; 8612: e8          .     
    cmp #&84                                                          ; 8613: c9 84       ..    
    bne c8604                                                         ; 8615: d0 ed       ..    
    inc l000a                                                         ; 8617: e6 0a       ..    
    iny                                                               ; 8619: c8          .     
    lda (l000b),y                                                     ; 861a: b1 0b       ..    
    cmp #&41 ; 'A'                                                    ; 861c: c9 41       .A    
    bne c8604                                                         ; 861e: d0 e4       ..    
; &8620 referenced 3 times by &85ff, &860b, &8610
.c8620
    lda l84c4,x                                                       ; 8620: bd c4 84    ...   
    sta l0029                                                         ; 8623: 85 29       .)    
    ldy #1                                                            ; 8625: a0 01       ..    
    cpx #&1a                                                          ; 8627: e0 1a       ..    
    bcs c8673                                                         ; 8629: b0 48       .H    
; &862b referenced 7 times by &85c5, &85c9, &85cd, &86aa, &879c, &881e, &8864
.c862b
    lda l0440                                                         ; 862b: ad 40 04    .@.   
    sta l0037                                                         ; 862e: 85 37       .7    
    sty l0039                                                         ; 8630: 84 39       .9    
    ldx l0028                                                         ; 8632: a6 28       .(    
    cpx #4                                                            ; 8634: e0 04       ..    
    ldx l0441                                                         ; 8636: ae 41 04    .A.   
    stx l0038                                                         ; 8639: 86 38       .8    
    bcc c8643                                                         ; 863b: 90 06       ..    
    lda l043c                                                         ; 863d: ad 3c 04    .<.   
    ldx l043d                                                         ; 8640: ae 3d 04    .=.   
; &8643 referenced 1 time by &863b
.c8643
    sta l003a                                                         ; 8643: 85 3a       .:    
    stx l003b                                                         ; 8645: 86 3b       .;    
    tya                                                               ; 8647: 98          .     
    beq return_1                                                      ; 8648: f0 28       .(    
    bpl c8650                                                         ; 864a: 10 04       ..    
    ldy l0036                                                         ; 864c: a4 36       .6    
    beq return_1                                                      ; 864e: f0 22       ."    
; &8650 referenced 2 times by &864a, &8670
.c8650
    dey                                                               ; 8650: 88          .     
    lda l0029,y                                                       ; 8651: b9 29 00    .).   
    bit l0039                                                         ; 8654: 24 39       $9    
    bpl c865b                                                         ; 8656: 10 03       ..    
    lda l0600,y                                                       ; 8658: b9 00 06    ...   
; &865b referenced 1 time by &8656
.c865b
    sta (l003a),y                                                     ; 865b: 91 3a       .:    
    inc l0440                                                         ; 865d: ee 40 04    .@.   
    bne c8665                                                         ; 8660: d0 03       ..    
    inc l0441                                                         ; 8662: ee 41 04    .A.   
; &8665 referenced 1 time by &8660
.c8665
    bcc c866f                                                         ; 8665: 90 08       ..    
    inc l043c                                                         ; 8667: ee 3c 04    .<.   
    bne c866f                                                         ; 866a: d0 03       ..    
    inc l043d                                                         ; 866c: ee 3d 04    .=.   
; &866f referenced 2 times by &8665, &866a
.c866f
    tya                                                               ; 866f: 98          .     
    bne c8650                                                         ; 8670: d0 de       ..    
; &8672 referenced 2 times by &8648, &864e
.return_1
    rts                                                               ; 8672: 60          `     
; &8673 referenced 1 time by &8629
.c8673
    cpx #&22                                                          ; 8673: e0 22       ."    
    bcs c86b7                                                         ; 8675: b0 40       .@    
    jsr sub_c8821                                                     ; 8677: 20 21 88     !.   
    clc                                                               ; 867a: 18          .     
    lda l002a                                                         ; 867b: a5 2a       .*    
    sbc l0440                                                         ; 867d: ed 40 04    .@.   
    tay                                                               ; 8680: a8          .     
    lda l002b                                                         ; 8681: a5 2b       .+    
    sbc l0441                                                         ; 8683: ed 41 04    .A.   
    cpy #1                                                            ; 8686: c0 01       ..    
    dey                                                               ; 8688: 88          .     
    sbc #0                                                            ; 8689: e9 00       ..    
    beq c86b2                                                         ; 868b: f0 25       .%    
    cmp #&ff                                                          ; 868d: c9 ff       ..    
    beq c86ad                                                         ; 868f: f0 1c       ..    
; &8691 referenced 2 times by &86b0, &86b5
.c8691
    lda l0028                                                         ; 8691: a5 28       .(    
    lsr a                                                             ; 8693: 4a          J     
    beq c86a5                                                         ; 8694: f0 0f       ..    
    brk                                                               ; 8696: 00          .     
    equb &01                                                          ; 8697: 01          .     
    equs "Out of range"                                               ; 8698: 4f 75 74... Out...
    equb &00                                                          ; 86a4: 00          .     
; &86a5 referenced 1 time by &8694
.c86a5
    tay                                                               ; 86a5: a8          .     
; &86a6 referenced 2 times by &86ae, &86b3
.c86a6
    sty l002a                                                         ; 86a6: 84 2a       .*    
; &86a8 referenced 2 times by &86ca, &873c
.c86a8
    ldy #2                                                            ; 86a8: a0 02       ..    
    jmp c862b                                                         ; 86aa: 4c 2b 86    L+.   
; &86ad referenced 1 time by &868f
.c86ad
    tya                                                               ; 86ad: 98          .     
    bmi c86a6                                                         ; 86ae: 30 f6       0.    
    bpl c8691                                                         ; 86b0: 10 df       ..    
; &86b2 referenced 1 time by &868b
.c86b2
    tya                                                               ; 86b2: 98          .     
    bpl c86a6                                                         ; 86b3: 10 f1       ..    
    bmi c8691                                                         ; 86b5: 30 da       0.    
; &86b7 referenced 1 time by &8675
.c86b7
    cpx #&29 ; ')'                                                    ; 86b7: e0 29       .)    
    bcs c86d3                                                         ; 86b9: b0 18       ..    
    jsr c8a97                                                         ; 86bb: 20 97 8a     ..   
    cmp #&23 ; '#'                                                    ; 86be: c9 23       .#    
    bne c86da                                                         ; 86c0: d0 18       ..    
    jsr sub_c882f                                                     ; 86c2: 20 2f 88     /.   
; &86c5 referenced 2 times by &877d, &87c9
.c86c5
    jsr sub_c8821                                                     ; 86c5: 20 21 88     !.   
; &86c8 referenced 2 times by &86f9, &870b
.c86c8
    lda l002b                                                         ; 86c8: a5 2b       .+    
    beq c86a8                                                         ; 86ca: f0 dc       ..    
; &86cc referenced 1 time by &880d
.c86cc
    brk                                                               ; 86cc: 00          .     
    equb &02                                                          ; 86cd: 02          .     
    equs "Byte"                                                       ; 86ce: 42 79 74... Byt...
    equb &00                                                          ; 86d2: 00          .     
; &86d3 referenced 1 time by &86b9
.c86d3
    cpx #&36 ; '6'                                                    ; 86d3: e0 36       .6    
    bne c873f                                                         ; 86d5: d0 68       .h    
    jsr c8a97                                                         ; 86d7: 20 97 8a     ..   
; &86da referenced 1 time by &86c0
.c86da
    cmp #&28 ; '('                                                    ; 86da: c9 28       .(    
    bne c8715                                                         ; 86dc: d0 37       .7    
    jsr sub_c8821                                                     ; 86de: 20 21 88     !.   
    jsr c8a97                                                         ; 86e1: 20 97 8a     ..   
    cmp #&29 ; ')'                                                    ; 86e4: c9 29       .)    
    bne c86fb                                                         ; 86e6: d0 13       ..    
    jsr c8a97                                                         ; 86e8: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 86eb: c9 2c       .,    
    bne c870d                                                         ; 86ed: d0 1e       ..    
    jsr sub_c882c                                                     ; 86ef: 20 2c 88     ,.   
    jsr c8a97                                                         ; 86f2: 20 97 8a     ..   
    cmp #&59 ; 'Y'                                                    ; 86f5: c9 59       .Y    
    bne c870d                                                         ; 86f7: d0 14       ..    
    beq c86c8                                                         ; 86f9: f0 cd       ..    
; &86fb referenced 1 time by &86e6
.c86fb
    cmp #&2c ; ','                                                    ; 86fb: c9 2c       .,    
    bne c870d                                                         ; 86fd: d0 0e       ..    
    jsr c8a97                                                         ; 86ff: 20 97 8a     ..   
    cmp #&58 ; 'X'                                                    ; 8702: c9 58       .X    
    bne c870d                                                         ; 8704: d0 07       ..    
    jsr c8a97                                                         ; 8706: 20 97 8a     ..   
    cmp #&29 ; ')'                                                    ; 8709: c9 29       .)    
    beq c86c8                                                         ; 870b: f0 bb       ..    
; &870d referenced 8 times by &86ed, &86f7, &86fd, &8704, &872d, &8764, &87af, &87ed
.c870d
    brk                                                               ; 870d: 00          .     
    equb &03                                                          ; 870e: 03          .     
    equs "Index"                                                      ; 870f: 49 6e 64... Ind...
    equb &00                                                          ; 8714: 00          .     
; &8715 referenced 1 time by &86dc
.c8715
    dec l000a                                                         ; 8715: c6 0a       ..    
    jsr sub_c8821                                                     ; 8717: 20 21 88     !.   
    jsr c8a97                                                         ; 871a: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 871d: c9 2c       .,    
    bne c8735                                                         ; 871f: d0 14       ..    
    jsr sub_c882c                                                     ; 8721: 20 2c 88     ,.   
    jsr c8a97                                                         ; 8724: 20 97 8a     ..   
    cmp #&58 ; 'X'                                                    ; 8727: c9 58       .X    
    beq c8735                                                         ; 8729: f0 0a       ..    
    cmp #&59 ; 'Y'                                                    ; 872b: c9 59       .Y    
    bne c870d                                                         ; 872d: d0 de       ..    
; &872f referenced 1 time by &873a
.loop_c872f
    jsr sub_c882f                                                     ; 872f: 20 2f 88     /.   
    jmp c879a                                                         ; 8732: 4c 9a 87    L..   
; &8735 referenced 5 times by &871f, &8729, &8785, &87db, &87ea
.c8735
    jsr sub_c8832                                                     ; 8735: 20 32 88     2.   
; &8738 referenced 3 times by &8758, &8762, &8810
.c8738
    lda l002b                                                         ; 8738: a5 2b       .+    
    bne loop_c872f                                                    ; 873a: d0 f3       ..    
    jmp c86a8                                                         ; 873c: 4c a8 86    L..   
; &873f referenced 1 time by &86d5
.c873f
    cpx #&2f ; '/'                                                    ; 873f: e0 2f       ./    
    bcs c876e                                                         ; 8741: b0 2b       .+    
    cpx #&2d ; '-'                                                    ; 8743: e0 2d       .-    
    bcs c8750                                                         ; 8745: b0 09       ..    
    jsr c8a97                                                         ; 8747: 20 97 8a     ..   
    cmp #&41 ; 'A'                                                    ; 874a: c9 41       .A    
    beq c8767                                                         ; 874c: f0 19       ..    
    dec l000a                                                         ; 874e: c6 0a       ..    
; &8750 referenced 1 time by &8745
.c8750
    jsr sub_c8821                                                     ; 8750: 20 21 88     !.   
    jsr c8a97                                                         ; 8753: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 8756: c9 2c       .,    
    bne c8738                                                         ; 8758: d0 de       ..    
    jsr sub_c882c                                                     ; 875a: 20 2c 88     ,.   
    jsr c8a97                                                         ; 875d: 20 97 8a     ..   
    cmp #&58 ; 'X'                                                    ; 8760: c9 58       .X    
    beq c8738                                                         ; 8762: f0 d4       ..    
    jmp c870d                                                         ; 8764: 4c 0d 87    L..   
; &8767 referenced 1 time by &874c
.c8767
    jsr sub_c8832                                                     ; 8767: 20 32 88     2.   
    ldy #1                                                            ; 876a: a0 01       ..    
    bne c879c                                                         ; 876c: d0 2e       ..    
; &876e referenced 1 time by &8741
.c876e
    cpx #&32 ; '2'                                                    ; 876e: e0 32       .2    
    bcs c8788                                                         ; 8770: b0 16       ..    
    cpx #&31 ; '1'                                                    ; 8772: e0 31       .1    
    beq c8782                                                         ; 8774: f0 0c       ..    
    jsr c8a97                                                         ; 8776: 20 97 8a     ..   
    cmp #&23 ; '#'                                                    ; 8779: c9 23       .#    
    bne c8780                                                         ; 877b: d0 03       ..    
    jmp c86c5                                                         ; 877d: 4c c5 86    L..   
; &8780 referenced 1 time by &877b
.c8780
    dec l000a                                                         ; 8780: c6 0a       ..    
; &8782 referenced 1 time by &8774
.c8782
    jsr sub_c8821                                                     ; 8782: 20 21 88     !.   
    jmp c8735                                                         ; 8785: 4c 35 87    L5.   
; &8788 referenced 1 time by &8770
.c8788
    cpx #&33 ; '3'                                                    ; 8788: e0 33       .3    
    beq c8797                                                         ; 878a: f0 0b       ..    
    bcs c87b2                                                         ; 878c: b0 24       .$    
    jsr c8a97                                                         ; 878e: 20 97 8a     ..   
    cmp #&28 ; '('                                                    ; 8791: c9 28       .(    
    beq c879f                                                         ; 8793: f0 0a       ..    
    dec l000a                                                         ; 8795: c6 0a       ..    
; &8797 referenced 1 time by &878a
.c8797
    jsr sub_c8821                                                     ; 8797: 20 21 88     !.   
; &879a referenced 2 times by &8732, &87ad
.c879a
    ldy #3                                                            ; 879a: a0 03       ..    
; &879c referenced 1 time by &876c
.c879c
    jmp c862b                                                         ; 879c: 4c 2b 86    L+.   
; &879f referenced 1 time by &8793
.c879f
    jsr sub_c882c                                                     ; 879f: 20 2c 88     ,.   
    jsr sub_c882c                                                     ; 87a2: 20 2c 88     ,.   
    jsr sub_c8821                                                     ; 87a5: 20 21 88     !.   
    jsr c8a97                                                         ; 87a8: 20 97 8a     ..   
    cmp #&29 ; ')'                                                    ; 87ab: c9 29       .)    
    beq c879a                                                         ; 87ad: f0 eb       ..    
    jmp c870d                                                         ; 87af: 4c 0d 87    L..   
; &87b2 referenced 1 time by &878c
.c87b2
    cpx #&39 ; '9'                                                    ; 87b2: e0 39       .9    
    bcs c8813                                                         ; 87b4: b0 5d       .]    
    lda l003d                                                         ; 87b6: a5 3d       .=    
    eor #1                                                            ; 87b8: 49 01       I.    
    and #&1f                                                          ; 87ba: 29 1f       ).    
    pha                                                               ; 87bc: 48          H     
    cpx #&37 ; '7'                                                    ; 87bd: e0 37       .7    
    bcs c87f0                                                         ; 87bf: b0 2f       ./    
    jsr c8a97                                                         ; 87c1: 20 97 8a     ..   
    cmp #&23 ; '#'                                                    ; 87c4: c9 23       .#    
    bne c87cc                                                         ; 87c6: d0 04       ..    
    pla                                                               ; 87c8: 68          h     
    jmp c86c5                                                         ; 87c9: 4c c5 86    L..   
; &87cc referenced 1 time by &87c6
.c87cc
    dec l000a                                                         ; 87cc: c6 0a       ..    
    jsr sub_c8821                                                     ; 87ce: 20 21 88     !.   
    pla                                                               ; 87d1: 68          h     
    sta l0037                                                         ; 87d2: 85 37       .7    
    jsr c8a97                                                         ; 87d4: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 87d7: c9 2c       .,    
    beq c87de                                                         ; 87d9: f0 03       ..    
    jmp c8735                                                         ; 87db: 4c 35 87    L5.   
; &87de referenced 1 time by &87d9
.c87de
    jsr c8a97                                                         ; 87de: 20 97 8a     ..   
    and #&1f                                                          ; 87e1: 29 1f       ).    
    cmp l0037                                                         ; 87e3: c5 37       .7    
    bne c87ed                                                         ; 87e5: d0 06       ..    
    jsr sub_c882c                                                     ; 87e7: 20 2c 88     ,.   
    jmp c8735                                                         ; 87ea: 4c 35 87    L5.   
; &87ed referenced 2 times by &87e5, &8804
.c87ed
    jmp c870d                                                         ; 87ed: 4c 0d 87    L..   
; &87f0 referenced 1 time by &87bf
.c87f0
    jsr sub_c8821                                                     ; 87f0: 20 21 88     !.   
    pla                                                               ; 87f3: 68          h     
    sta l0037                                                         ; 87f4: 85 37       .7    
    jsr c8a97                                                         ; 87f6: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 87f9: c9 2c       .,    
    bne c8810                                                         ; 87fb: d0 13       ..    
    jsr c8a97                                                         ; 87fd: 20 97 8a     ..   
    and #&1f                                                          ; 8800: 29 1f       ).    
    cmp l0037                                                         ; 8802: c5 37       .7    
    bne c87ed                                                         ; 8804: d0 e7       ..    
    jsr sub_c882c                                                     ; 8806: 20 2c 88     ,.   
    lda l002b                                                         ; 8809: a5 2b       .+    
    beq c8810                                                         ; 880b: f0 03       ..    
    jmp c86cc                                                         ; 880d: 4c cc 86    L..   
; &8810 referenced 2 times by &87fb, &880b
.c8810
    jmp c8738                                                         ; 8810: 4c 38 87    L8.   
; &8813 referenced 1 time by &87b4
.c8813
    bne c883a                                                         ; 8813: d0 25       .%    
    jsr sub_c8821                                                     ; 8815: 20 21 88     !.   
    lda l002a                                                         ; 8818: a5 2a       .*    
    sta l0028                                                         ; 881a: 85 28       .(    
    ldy #0                                                            ; 881c: a0 00       ..    
    jmp c862b                                                         ; 881e: 4c 2b 86    L+.   
; &8821 referenced 12 times by &8677, &86c5, &86de, &8717, &8750, &8782, &8797, &87a5, &87ce, &87f0, &8815, &885a
.sub_c8821
    jsr sub_c9b1d                                                     ; 8821: 20 1d 9b     ..   
    jsr c92f0                                                         ; 8824: 20 f0 92     ..   
; &8827 referenced 2 times by &85b7, &8875
.sub_c8827
    ldy l001b                                                         ; 8827: a4 1b       ..    
    sty l000a                                                         ; 8829: 84 0a       ..    
    rts                                                               ; 882b: 60          `     
; &882c referenced 7 times by &86ef, &8721, &875a, &879f, &87a2, &87e7, &8806
.sub_c882c
    jsr sub_c882f                                                     ; 882c: 20 2f 88     /.   
; &882f referenced 3 times by &86c2, &872f, &882c
.sub_c882f
    jsr sub_c8832                                                     ; 882f: 20 32 88     2.   
; &8832 referenced 3 times by &8735, &8767, &882f
.sub_c8832
    lda l0029                                                         ; 8832: a5 29       .)    
    clc                                                               ; 8834: 18          .     
    adc #4                                                            ; 8835: 69 04       i.    
    sta l0029                                                         ; 8837: 85 29       .)    
    rts                                                               ; 8839: 60          `     
; &883a referenced 1 time by &8813
.c883a
    ldx #1                                                            ; 883a: a2 01       ..    
    ldy l000a                                                         ; 883c: a4 0a       ..    
    inc l000a                                                         ; 883e: e6 0a       ..    
    lda (l000b),y                                                     ; 8840: b1 0b       ..    
    cmp #&42 ; 'B'                                                    ; 8842: c9 42       .B    
    beq c8858                                                         ; 8844: f0 12       ..    
    inx                                                               ; 8846: e8          .     
    cmp #&57 ; 'W'                                                    ; 8847: c9 57       .W    
    beq c8858                                                         ; 8849: f0 0d       ..    
    ldx #4                                                            ; 884b: a2 04       ..    
    cmp #&44 ; 'D'                                                    ; 884d: c9 44       .D    
    beq c8858                                                         ; 884f: f0 07       ..    
    cmp #&53 ; 'S'                                                    ; 8851: c9 53       .S    
    beq c886a                                                         ; 8853: f0 15       ..    
    jmp c982a                                                         ; 8855: 4c 2a 98    L*.   
; &8858 referenced 3 times by &8844, &8849, &884f
.c8858
    txa                                                               ; 8858: 8a          .     
    pha                                                               ; 8859: 48          H     
    jsr sub_c8821                                                     ; 885a: 20 21 88     !.   
    ldx #&29 ; ')'                                                    ; 885d: a2 29       .)    
    jsr sub_cbe44                                                     ; 885f: 20 44 be     D.   
    pla                                                               ; 8862: 68          h     
    tay                                                               ; 8863: a8          .     
; &8864 referenced 1 time by &887a
.loop_c8864
    jmp c862b                                                         ; 8864: 4c 2b 86    L+.   
; &8867 referenced 1 time by &8870
.loop_c8867
    jmp c8c0e                                                         ; 8867: 4c 0e 8c    L..   
; &886a referenced 1 time by &8853
.c886a
    lda l0028                                                         ; 886a: a5 28       .(    
    pha                                                               ; 886c: 48          H     
    jsr sub_c9b1d                                                     ; 886d: 20 1d 9b     ..   
    bne loop_c8867                                                    ; 8870: d0 f5       ..    
    pla                                                               ; 8872: 68          h     
    sta l0028                                                         ; 8873: 85 28       .(    
    jsr sub_c8827                                                     ; 8875: 20 27 88     '.   
    ldy #&ff                                                          ; 8878: a0 ff       ..    
    bne loop_c8864                                                    ; 887a: d0 e8       ..    
; &887c referenced 2 times by &88dd, &8a55
.sub_c887c
    pha                                                               ; 887c: 48          H     
    clc                                                               ; 887d: 18          .     
    tya                                                               ; 887e: 98          .     
    adc l0037                                                         ; 887f: 65 37       e7    
    sta l0039                                                         ; 8881: 85 39       .9    
    ldy #0                                                            ; 8883: a0 00       ..    
    tya                                                               ; 8885: 98          .     
    adc l0038                                                         ; 8886: 65 38       e8    
    sta l003a                                                         ; 8888: 85 3a       .:    
    pla                                                               ; 888a: 68          h     
    sta (l0037),y                                                     ; 888b: 91 37       .7    
; &888d referenced 1 time by &8894
.loop_c888d
    iny                                                               ; 888d: c8          .     
    lda (l0039),y                                                     ; 888e: b1 39       .9    
    sta (l0037),y                                                     ; 8890: 91 37       .7    
    cmp #&0d                                                          ; 8892: c9 0d       ..    
    bne loop_c888d                                                    ; 8894: d0 f7       ..    
    rts                                                               ; 8896: 60          `     
; &8897 referenced 1 time by &89b0
.sub_c8897
    and #&0f                                                          ; 8897: 29 0f       ).    
    sta l003d                                                         ; 8899: 85 3d       .=    
    sty l003e                                                         ; 889b: 84 3e       .>    
; &889d referenced 2 times by &88ce, &88d2
.c889d
    iny                                                               ; 889d: c8          .     
    lda (l0037),y                                                     ; 889e: b1 37       .7    
    cmp #&3a ; ':'                                                    ; 88a0: c9 3a       .:    
    bcs c88da                                                         ; 88a2: b0 36       .6    
    cmp #&30 ; '0'                                                    ; 88a4: c9 30       .0    
    bcc c88da                                                         ; 88a6: 90 32       .2    
    and #&0f                                                          ; 88a8: 29 0f       ).    
    pha                                                               ; 88aa: 48          H     
    ldx l003e                                                         ; 88ab: a6 3e       .>    
    lda l003d                                                         ; 88ad: a5 3d       .=    
    asl a                                                             ; 88af: 0a          .     
    rol l003e                                                         ; 88b0: 26 3e       &>    
    bmi c88d5                                                         ; 88b2: 30 21       0!    
    asl a                                                             ; 88b4: 0a          .     
    rol l003e                                                         ; 88b5: 26 3e       &>    
    bmi c88d5                                                         ; 88b7: 30 1c       0.    
    adc l003d                                                         ; 88b9: 65 3d       e=    
    sta l003d                                                         ; 88bb: 85 3d       .=    
    txa                                                               ; 88bd: 8a          .     
    adc l003e                                                         ; 88be: 65 3e       e>    
    asl l003d                                                         ; 88c0: 06 3d       .=    
    rol a                                                             ; 88c2: 2a          *     
    bmi c88d5                                                         ; 88c3: 30 10       0.    
    bcs c88d5                                                         ; 88c5: b0 0e       ..    
    sta l003e                                                         ; 88c7: 85 3e       .>    
    pla                                                               ; 88c9: 68          h     
    adc l003d                                                         ; 88ca: 65 3d       e=    
    sta l003d                                                         ; 88cc: 85 3d       .=    
    bcc c889d                                                         ; 88ce: 90 cd       ..    
    inc l003e                                                         ; 88d0: e6 3e       .>    
    bpl c889d                                                         ; 88d2: 10 c9       ..    
    pha                                                               ; 88d4: 48          H     
; &88d5 referenced 4 times by &88b2, &88b7, &88c3, &88c5
.c88d5
    pla                                                               ; 88d5: 68          h     
    ldy #0                                                            ; 88d6: a0 00       ..    
    sec                                                               ; 88d8: 38          8     
    rts                                                               ; 88d9: 60          `     
; &88da referenced 2 times by &88a2, &88a6
.c88da
    dey                                                               ; 88da: 88          .     
    lda #&8d                                                          ; 88db: a9 8d       ..    
    jsr sub_c887c                                                     ; 88dd: 20 7c 88     |.   
    lda l0037                                                         ; 88e0: a5 37       .7    
    adc #2                                                            ; 88e2: 69 02       i.    
    sta l0039                                                         ; 88e4: 85 39       .9    
    lda l0038                                                         ; 88e6: a5 38       .8    
    adc #0                                                            ; 88e8: 69 00       i.    
    sta l003a                                                         ; 88ea: 85 3a       .:    
; &88ec referenced 1 time by &88f1
.loop_c88ec
    lda (l0037),y                                                     ; 88ec: b1 37       .7    
    sta (l0039),y                                                     ; 88ee: 91 39       .9    
    dey                                                               ; 88f0: 88          .     
    bne loop_c88ec                                                    ; 88f1: d0 f9       ..    
    ldy #3                                                            ; 88f3: a0 03       ..    
    lda l003e                                                         ; 88f5: a5 3e       .>    
    ora #&40 ; '@'                                                    ; 88f7: 09 40       .@    
    sta (l0037),y                                                     ; 88f9: 91 37       .7    
    dey                                                               ; 88fb: 88          .     
    lda l003d                                                         ; 88fc: a5 3d       .=    
    and #&3f ; '?'                                                    ; 88fe: 29 3f       )?    
    ora #&40 ; '@'                                                    ; 8900: 09 40       .@    
    sta (l0037),y                                                     ; 8902: 91 37       .7    
    dey                                                               ; 8904: 88          .     
    lda l003d                                                         ; 8905: a5 3d       .=    
    and #&c0                                                          ; 8907: 29 c0       ).    
    sta l003d                                                         ; 8909: 85 3d       .=    
    lda l003e                                                         ; 890b: a5 3e       .>    
    and #&c0                                                          ; 890d: 29 c0       ).    
    lsr a                                                             ; 890f: 4a          J     
    lsr a                                                             ; 8910: 4a          J     
    ora l003d                                                         ; 8911: 05 3d       .=    
    lsr a                                                             ; 8913: 4a          J     
    lsr a                                                             ; 8914: 4a          J     
    eor #&54 ; 'T'                                                    ; 8915: 49 54       IT    
    sta (l0037),y                                                     ; 8917: 91 37       .7    
    jsr sub_c8944                                                     ; 8919: 20 44 89     D.   
    jsr sub_c8944                                                     ; 891c: 20 44 89     D.   
    jsr sub_c8944                                                     ; 891f: 20 44 89     D.   
    ldy #0                                                            ; 8922: a0 00       ..    
; &8924 referenced 3 times by &8928, &8930, &8938
.c8924
    clc                                                               ; 8924: 18          .     
    rts                                                               ; 8925: 60          `     
; &8926 referenced 4 times by &89cb, &89d4, &8a43, &8a74
.sub_c8926
    cmp #&7b ; '{'                                                    ; 8926: c9 7b       .{    
    bcs c8924                                                         ; 8928: b0 fa       ..    
    cmp #&5f ; '_'                                                    ; 892a: c9 5f       ._    
    bcs return_2                                                      ; 892c: b0 0e       ..    
    cmp #&5b ; '['                                                    ; 892e: c9 5b       .[    
    bcs c8924                                                         ; 8930: b0 f2       ..    
    cmp #&41 ; 'A'                                                    ; 8932: c9 41       .A    
    bcs return_2                                                      ; 8934: b0 06       ..    
; &8936 referenced 3 times by &893f, &896d, &89a7
.c8936
    cmp #&3a ; ':'                                                    ; 8936: c9 3a       .:    
    bcs c8924                                                         ; 8938: b0 ea       ..    
    cmp #&30 ; '0'                                                    ; 893a: c9 30       .0    
; &893c referenced 2 times by &892c, &8934
.return_2
    rts                                                               ; 893c: 60          `     
; &893d referenced 1 time by &89b7
.sub_c893d
    cmp #&2e ; '.'                                                    ; 893d: c9 2e       ..    
    bne c8936                                                         ; 893f: d0 f5       ..    
    rts                                                               ; 8941: 60          `     
    equb &b1, &37                                                     ; 8942: b1 37       .7    
; &8944 referenced 8 times by &8919, &891c, &891f, &894b, &8961, &89bc, &89d9, &8a79
.sub_c8944
    inc l0037                                                         ; 8944: e6 37       .7    
    bne return_3                                                      ; 8946: d0 02       ..    
    inc l0038                                                         ; 8948: e6 38       .8    
; &894a referenced 2 times by &8946, &895b
.return_3
    rts                                                               ; 894a: 60          `     
; &894b referenced 3 times by &896a, &8980, &bfdc
.sub_c894b
    jsr sub_c8944                                                     ; 894b: 20 44 89     D.   
    lda (l0037),y                                                     ; 894e: b1 37       .7    
    rts                                                               ; 8950: 60          `     
    equb &a0, &00, &84, &3b, &84, &3c                                 ; 8951: a0 00 84... ......
; &8957 referenced 5 times by &8964, &8974, &897a, &89c8, &8b2a
.c8957
    lda (l0037),y                                                     ; 8957: b1 37       .7    
    cmp #&0d                                                          ; 8959: c9 0d       ..    
    beq return_3                                                      ; 895b: f0 ed       ..    
    cmp #&20 ; ' '                                                    ; 895d: c9 20       .     
    bne c8966                                                         ; 895f: d0 05       ..    
; &8961 referenced 5 times by &8985, &8994, &8998, &89e9, &8a89
.c8961
    jsr sub_c8944                                                     ; 8961: 20 44 89     D.   
    bne c8957                                                         ; 8964: d0 f1       ..    
; &8966 referenced 1 time by &895f
.c8966
    cmp #&26 ; '&'                                                    ; 8966: c9 26       .&    
    bne c897c                                                         ; 8968: d0 12       ..    
; &896a referenced 2 times by &8970, &8978
.c896a
    jsr sub_c894b                                                     ; 896a: 20 4b 89     K.   
    jsr c8936                                                         ; 896d: 20 36 89     6.   
    bcs c896a                                                         ; 8970: b0 f8       ..    
    cmp #&41 ; 'A'                                                    ; 8972: c9 41       .A    
    bcc c8957                                                         ; 8974: 90 e1       ..    
    cmp #&47 ; 'G'                                                    ; 8976: c9 47       .G    
    bcc c896a                                                         ; 8978: 90 f0       ..    
    bcs c8957                                                         ; 897a: b0 db       ..    
; &897c referenced 1 time by &8968
.c897c
    cmp #&22                                                          ; 897c: c9 22       ."    
    bne c898c                                                         ; 897e: d0 0c       ..    
; &8980 referenced 1 time by &8989
.loop_c8980
    jsr sub_c894b                                                     ; 8980: 20 4b 89     K.   
    cmp #&22                                                          ; 8983: c9 22       ."    
    beq c8961                                                         ; 8985: f0 da       ..    
    cmp #&0d                                                          ; 8987: c9 0d       ..    
    bne loop_c8980                                                    ; 8989: d0 f5       ..    
    rts                                                               ; 898b: 60          `     
; &898c referenced 1 time by &897e
.c898c
    cmp #&3a ; ':'                                                    ; 898c: c9 3a       .:    
    bne c8996                                                         ; 898e: d0 06       ..    
    sty l003b                                                         ; 8990: 84 3b       .;    
    sty l003c                                                         ; 8992: 84 3c       .<    
    beq c8961                                                         ; 8994: f0 cb       ..    
; &8996 referenced 1 time by &898e
.c8996
    cmp #&2c ; ','                                                    ; 8996: c9 2c       .,    
    beq c8961                                                         ; 8998: f0 c7       ..    
    cmp #&2a ; '*'                                                    ; 899a: c9 2a       .*    
    bne c89a3                                                         ; 899c: d0 05       ..    
    lda l003b                                                         ; 899e: a5 3b       .;    
    bne c89e3                                                         ; 89a0: d0 41       .A    
    rts                                                               ; 89a2: 60          `     
; &89a3 referenced 1 time by &899c
.c89a3
    cmp #&2e ; '.'                                                    ; 89a3: c9 2e       ..    
    beq c89b5                                                         ; 89a5: f0 0e       ..    
    jsr c8936                                                         ; 89a7: 20 36 89     6.   
    bcc c89df                                                         ; 89aa: 90 33       .3    
    ldx l003c                                                         ; 89ac: a6 3c       .<    
    beq c89b5                                                         ; 89ae: f0 05       ..    
    jsr sub_c8897                                                     ; 89b0: 20 97 88     ..   
    bcc c89e9                                                         ; 89b3: 90 34       .4    
; &89b5 referenced 3 times by &89a5, &89ae, &89bf
.c89b5
    lda (l0037),y                                                     ; 89b5: b1 37       .7    
    jsr sub_c893d                                                     ; 89b7: 20 3d 89     =.   
    bcc c89c2                                                         ; 89ba: 90 06       ..    
    jsr sub_c8944                                                     ; 89bc: 20 44 89     D.   
    jmp c89b5                                                         ; 89bf: 4c b5 89    L..   
; &89c2 referenced 2 times by &89ba, &89d7
.c89c2
    ldx #&ff                                                          ; 89c2: a2 ff       ..    
    stx l003b                                                         ; 89c4: 86 3b       .;    
    sty l003c                                                         ; 89c6: 84 3c       .<    
    jmp c8957                                                         ; 89c8: 4c 57 89    LW.   
; &89cb referenced 1 time by &89ee
.loop_c89cb
    jsr sub_c8926                                                     ; 89cb: 20 26 89     &.   
    bcc c89e3                                                         ; 89ce: 90 13       ..    
; &89d0 referenced 2 times by &8a16, &8a46
.c89d0
    ldy #0                                                            ; 89d0: a0 00       ..    
; &89d2 referenced 2 times by &89dc, &89fa
.c89d2
    lda (l0037),y                                                     ; 89d2: b1 37       .7    
    jsr sub_c8926                                                     ; 89d4: 20 26 89     &.   
    bcc c89c2                                                         ; 89d7: 90 e9       ..    
    jsr sub_c8944                                                     ; 89d9: 20 44 89     D.   
    jmp c89d2                                                         ; 89dc: 4c d2 89    L..   
; &89df referenced 1 time by &89aa
.c89df
    cmp #&41 ; 'A'                                                    ; 89df: c9 41       .A    
    bcs c89ec                                                         ; 89e1: b0 09       ..    
; &89e3 referenced 2 times by &89a0, &89ce
.c89e3
    ldx #&ff                                                          ; 89e3: a2 ff       ..    
    stx l003b                                                         ; 89e5: 86 3b       .;    
    sty l003c                                                         ; 89e7: 84 3c       .<    
; &89e9 referenced 1 time by &89b3
.c89e9
    jmp c8961                                                         ; 89e9: 4c 61 89    La.   
; &89ec referenced 1 time by &89e1
.c89ec
    cmp #&58 ; 'X'                                                    ; 89ec: c9 58       .X    
    bcs loop_c89cb                                                    ; 89ee: b0 db       ..    
    ldx #&71 ; 'q'                                                    ; 89f0: a2 71       .q    
    stx l0039                                                         ; 89f2: 86 39       .9    
    ldx #&80                                                          ; 89f4: a2 80       ..    
    stx l003a                                                         ; 89f6: 86 3a       .:    
; &89f8 referenced 1 time by &8a34
.c89f8
    cmp (l0039),y                                                     ; 89f8: d1 39       .9    
    bcc c89d2                                                         ; 89fa: 90 d6       ..    
    bne c8a0d                                                         ; 89fc: d0 0f       ..    
; &89fe referenced 1 time by &8a05
.loop_c89fe
    iny                                                               ; 89fe: c8          .     
    lda (l0039),y                                                     ; 89ff: b1 39       .9    
    bmi c8a37                                                         ; 8a01: 30 34       04    
    cmp (l0037),y                                                     ; 8a03: d1 37       .7    
    beq loop_c89fe                                                    ; 8a05: f0 f7       ..    
    lda (l0037),y                                                     ; 8a07: b1 37       .7    
    cmp #&2e ; '.'                                                    ; 8a09: c9 2e       ..    
    beq c8a18                                                         ; 8a0b: f0 0b       ..    
; &8a0d referenced 2 times by &89fc, &8a10
.c8a0d
    iny                                                               ; 8a0d: c8          .     
    lda (l0039),y                                                     ; 8a0e: b1 39       .9    
    bpl c8a0d                                                         ; 8a10: 10 fb       ..    
    cmp #&fe                                                          ; 8a12: c9 fe       ..    
    bne c8a25                                                         ; 8a14: d0 0f       ..    
    bcs c89d0                                                         ; 8a16: b0 b8       ..    
; &8a18 referenced 1 time by &8a0b
.c8a18
    iny                                                               ; 8a18: c8          .     
; &8a19 referenced 2 times by &8a1f, &8a23
.c8a19
    lda (l0039),y                                                     ; 8a19: b1 39       .9    
    bmi c8a37                                                         ; 8a1b: 30 1a       0.    
    inc l0039                                                         ; 8a1d: e6 39       .9    
    bne c8a19                                                         ; 8a1f: d0 f8       ..    
    inc l003a                                                         ; 8a21: e6 3a       .:    
    bne c8a19                                                         ; 8a23: d0 f4       ..    
; &8a25 referenced 1 time by &8a14
.c8a25
    sec                                                               ; 8a25: 38          8     
    iny                                                               ; 8a26: c8          .     
    tya                                                               ; 8a27: 98          .     
    adc l0039                                                         ; 8a28: 65 39       e9    
    sta l0039                                                         ; 8a2a: 85 39       .9    
    bcc c8a30                                                         ; 8a2c: 90 02       ..    
    inc l003a                                                         ; 8a2e: e6 3a       .:    
; &8a30 referenced 1 time by &8a2c
.c8a30
    ldy #0                                                            ; 8a30: a0 00       ..    
    lda (l0037),y                                                     ; 8a32: b1 37       .7    
    jmp c89f8                                                         ; 8a34: 4c f8 89    L..   
; &8a37 referenced 2 times by &8a01, &8a1b
.c8a37
    tax                                                               ; 8a37: aa          .     
    iny                                                               ; 8a38: c8          .     
    lda (l0039),y                                                     ; 8a39: b1 39       .9    
    sta l003d                                                         ; 8a3b: 85 3d       .=    
    dey                                                               ; 8a3d: 88          .     
    lsr a                                                             ; 8a3e: 4a          J     
    bcc c8a48                                                         ; 8a3f: 90 07       ..    
    lda (l0037),y                                                     ; 8a41: b1 37       .7    
    jsr sub_c8926                                                     ; 8a43: 20 26 89     &.   
    bcs c89d0                                                         ; 8a46: b0 88       ..    
; &8a48 referenced 1 time by &8a3f
.c8a48
    txa                                                               ; 8a48: 8a          .     
    bit l003d                                                         ; 8a49: 24 3d       $=    
    bvc c8a54                                                         ; 8a4b: 50 07       P.    
    ldx l003b                                                         ; 8a4d: a6 3b       .;    
    bne c8a54                                                         ; 8a4f: d0 03       ..    
    clc                                                               ; 8a51: 18          .     
    adc #&40 ; '@'                                                    ; 8a52: 69 40       i@    
; &8a54 referenced 2 times by &8a4b, &8a4f
.c8a54
    dey                                                               ; 8a54: 88          .     
    jsr sub_c887c                                                     ; 8a55: 20 7c 88     |.   
    ldy #0                                                            ; 8a58: a0 00       ..    
    ldx #&ff                                                          ; 8a5a: a2 ff       ..    
    lda l003d                                                         ; 8a5c: a5 3d       .=    
    lsr a                                                             ; 8a5e: 4a          J     
    lsr a                                                             ; 8a5f: 4a          J     
    bcc c8a66                                                         ; 8a60: 90 04       ..    
    stx l003b                                                         ; 8a62: 86 3b       .;    
    sty l003c                                                         ; 8a64: 84 3c       .<    
; &8a66 referenced 1 time by &8a60
.c8a66
    lsr a                                                             ; 8a66: 4a          J     
    bcc c8a6d                                                         ; 8a67: 90 04       ..    
    sty l003b                                                         ; 8a69: 84 3b       .;    
    sty l003c                                                         ; 8a6b: 84 3c       .<    
; &8a6d referenced 1 time by &8a67
.c8a6d
    lsr a                                                             ; 8a6d: 4a          J     
    bcc c8a81                                                         ; 8a6e: 90 11       ..    
    pha                                                               ; 8a70: 48          H     
    iny                                                               ; 8a71: c8          .     
; &8a72 referenced 1 time by &8a7c
.c8a72
    lda (l0037),y                                                     ; 8a72: b1 37       .7    
    jsr sub_c8926                                                     ; 8a74: 20 26 89     &.   
    bcc c8a7f                                                         ; 8a77: 90 06       ..    
    jsr sub_c8944                                                     ; 8a79: 20 44 89     D.   
    jmp c8a72                                                         ; 8a7c: 4c 72 8a    Lr.   
; &8a7f referenced 1 time by &8a77
.c8a7f
    dey                                                               ; 8a7f: 88          .     
    pla                                                               ; 8a80: 68          h     
; &8a81 referenced 1 time by &8a6e
.c8a81
    lsr a                                                             ; 8a81: 4a          J     
    bcc c8a86                                                         ; 8a82: 90 02       ..    
    stx l003c                                                         ; 8a84: 86 3c       .<    
; &8a86 referenced 1 time by &8a82
.c8a86
    lsr a                                                             ; 8a86: 4a          J     
    bcs return_4                                                      ; 8a87: b0 0d       ..    
    jmp c8961                                                         ; 8a89: 4c 61 89    La.   
; &8a8c referenced 3 times by &8a94, &9841, &ae02
.c8a8c
    ldy l001b                                                         ; 8a8c: a4 1b       ..    
    inc l001b                                                         ; 8a8e: e6 1b       ..    
    lda (l0019),y                                                     ; 8a90: b1 19       ..    
    cmp #&20 ; ' '                                                    ; 8a92: c9 20       .     
    beq c8a8c                                                         ; 8a94: f0 f6       ..    
; &8a96 referenced 1 time by &8a87
.return_4
    rts                                                               ; 8a96: 60          `     
; &8a97 referenced 24 times by &8508, &85bc, &86bb, &86d7, &86e1, &86e8, &86f2, &86ff, &8706, &871a, &8724, &8747, &8753, &875d, &8776, &878e, &87a8, &87c1, &87d4, &87de, &87f6, &87fd, &8a9f, &8b38
.c8a97
    ldy l000a                                                         ; 8a97: a4 0a       ..    
    inc l000a                                                         ; 8a99: e6 0a       ..    
    lda (l000b),y                                                     ; 8a9b: b1 0b       ..    
    cmp #&20 ; ' '                                                    ; 8a9d: c9 20       .     
    beq c8a97                                                         ; 8a9f: f0 f6       ..    
    rts                                                               ; 8aa1: 60          `     
    equb &00, &05                                                     ; 8aa2: 00 05       ..    
    equs "Missing ,"                                                  ; 8aa4: 4d 69 73... Mis...
    equb &00, &20, &8c, &8a, &c9, &2c, &d0, &ed                       ; 8aad: 00 20 8c... . ....
    equs "` W"                                                        ; 8ab5: 60 20 57    ` W   
    equb &98, &a5, &18, &85, &38, &a9, &00, &85, &37, &91             ; 8ab8: 98 a5 18... ......
    equs "7 o"                                                        ; 8ac2: 37 20 6f    7 o   
    equb &be, &d0                                                     ; 8ac5: be d0       ..    
    equs "+ W"                                                        ; 8ac7: 2b 20 57    + W   
    equb &98, &20, &6f, &be, &d0                                      ; 8aca: 98 20 6f... . o...
    equs "& W"                                                        ; 8acf: 26 20 57    & W   
    equb &98, &00, &00                                                ; 8ad2: 98 00 00    ...   
    equs "STOP"                                                       ; 8ad5: 53 54 4f... STO...
    equb &00, &20, &57, &98                                           ; 8ad9: 00 20 57... . W...
; &8add referenced 1 time by &806e
.c8add
    lda #&0d                                                          ; 8add: a9 0d       ..    
    ldy l0018                                                         ; 8adf: a4 18       ..    
    sty l0013                                                         ; 8ae1: 84 13       ..    
    ldy #0                                                            ; 8ae3: a0 00       ..    
    sty l0012                                                         ; 8ae5: 84 12       ..    
    sty l0020                                                         ; 8ae7: 84 20       .     
    sta (l0012),y                                                     ; 8ae9: 91 12       ..    
    lda #&ff                                                          ; 8aeb: a9 ff       ..    
    iny                                                               ; 8aed: c8          .     
    sta (l0012),y                                                     ; 8aee: 91 12       ..    
    iny                                                               ; 8af0: c8          .     
    sty l0012                                                         ; 8af1: 84 12       ..    
; &8af3 referenced 1 time by &8b35
.c8af3
    jsr sub_cbd20                                                     ; 8af3: 20 20 bd      .   
; &8af6 referenced 3 times by &859c, &8b41, &98bc
.c8af6
    ldy #7                                                            ; 8af6: a0 07       ..    
    sty l000c                                                         ; 8af8: 84 0c       ..    
    ldy #0                                                            ; 8afa: a0 00       ..    
    sty l000b                                                         ; 8afc: 84 0b       ..    
    lda #&33 ; '3'                                                    ; 8afe: a9 33       .3    
    sta l0016                                                         ; 8b00: 85 16       ..    
    lda #&b4                                                          ; 8b02: a9 b4       ..    
    sta l0017                                                         ; 8b04: 85 17       ..    
    lda #&3e ; '>'                                                    ; 8b06: a9 3e       .>    
    jsr sub_cbc02                                                     ; 8b08: 20 02 bc     ..   
    lda #&33 ; '3'                                                    ; 8b0b: a9 33       .3    
    sta l0016                                                         ; 8b0d: 85 16       ..    
    lda #&b4                                                          ; 8b0f: a9 b4       ..    
    sta l0017                                                         ; 8b11: 85 17       ..    
    ldx #&ff                                                          ; 8b13: a2 ff       ..    
    stx l0028                                                         ; 8b15: 86 28       .(    
    stx l003c                                                         ; 8b17: 86 3c       .<    
    txs                                                               ; 8b19: 9a          .     
    jsr sub_cbd3a                                                     ; 8b1a: 20 3a bd     :.   
    tay                                                               ; 8b1d: a8          .     
    lda l000b                                                         ; 8b1e: a5 0b       ..    
    sta l0037                                                         ; 8b20: 85 37       .7    
    lda l000c                                                         ; 8b22: a5 0c       ..    
    sta l0038                                                         ; 8b24: 85 38       .8    
    sty l003b                                                         ; 8b26: 84 3b       .;    
    sty l000a                                                         ; 8b28: 84 0a       ..    
    jsr c8957                                                         ; 8b2a: 20 57 89     W.   
    jsr sub_c97df                                                     ; 8b2d: 20 df 97     ..   
    bcc c8b38                                                         ; 8b30: 90 06       ..    
    jsr sub_cbc8d                                                     ; 8b32: 20 8d bc     ..   
    jmp c8af3                                                         ; 8b35: 4c f3 8a    L..   
; &8b38 referenced 1 time by &8b30
.c8b38
    jsr c8a97                                                         ; 8b38: 20 97 8a     ..   
    cmp #&c6                                                          ; 8b3b: c9 c6       ..    
    bcs c8bb1                                                         ; 8b3d: b0 72       .r    
    bcc c8bbf                                                         ; 8b3f: 90 7e       .~    
; &8b41 referenced 1 time by &8b8f
.loop_c8b41
    jmp c8af6                                                         ; 8b41: 4c f6 8a    L..   
; &8b44 referenced 1 time by &8b6f
.loop_c8b44
    jmp c8504                                                         ; 8b44: 4c 04 85    L..   
; &8b47 referenced 1 time by &8b67
.loop_c8b47
    tsx                                                               ; 8b47: ba          .     
    cpx #&fc                                                          ; 8b48: e0 fc       ..    
    bcs c8b59                                                         ; 8b4a: b0 0d       ..    
    lda l01ff                                                         ; 8b4c: ad ff 01    ...   
    cmp #&a4                                                          ; 8b4f: c9 a4       ..    
    bne c8b59                                                         ; 8b51: d0 06       ..    
    jsr sub_c9b1d                                                     ; 8b53: 20 1d 9b     ..   
    jmp c984c                                                         ; 8b56: 4c 4c 98    LL.   
; &8b59 referenced 2 times by &8b4a, &8b51
.c8b59
    brk                                                               ; 8b59: 00          .     
    equb &07                                                          ; 8b5a: 07          .     
    equs "No "                                                        ; 8b5b: 4e 6f 20    No    
    equb &a4, &00                                                     ; 8b5e: a4 00       ..    
; &8b60 referenced 1 time by &8bce
.loop_c8b60
    ldy l000a                                                         ; 8b60: a4 0a       ..    
    dey                                                               ; 8b62: 88          .     
    lda (l000b),y                                                     ; 8b63: b1 0b       ..    
    cmp #&3d ; '='                                                    ; 8b65: c9 3d       .=    
    beq loop_c8b47                                                    ; 8b67: f0 de       ..    
    cmp #&2a ; '*'                                                    ; 8b69: c9 2a       .*    
    beq c8b73                                                         ; 8b6b: f0 06       ..    
    cmp #&5b ; '['                                                    ; 8b6d: c9 5b       .[    
    beq loop_c8b44                                                    ; 8b6f: f0 d3       ..    
    bne c8b96                                                         ; 8b71: d0 23       .#    
; &8b73 referenced 1 time by &8b6b
.c8b73
    jsr c986d                                                         ; 8b73: 20 6d 98     m.   
    ldx l000b                                                         ; 8b76: a6 0b       ..    
    ldy l000c                                                         ; 8b78: a4 0c       ..    
    jsr oscli                                                         ; 8b7a: 20 f7 ff     ..   
; &8b7d referenced 1 time by &8b89
.loop_c8b7d
    lda #&0d                                                          ; 8b7d: a9 0d       ..    
    ldy l000a                                                         ; 8b7f: a4 0a       ..    
    dey                                                               ; 8b81: 88          .     
; &8b82 referenced 1 time by &8b85
.loop_c8b82
    iny                                                               ; 8b82: c8          .     
    cmp (l000b),y                                                     ; 8b83: d1 0b       ..    
    bne loop_c8b82                                                    ; 8b85: d0 fb       ..    
; &8b87 referenced 1 time by &8ba1
.loop_c8b87
    cmp #&8b                                                          ; 8b87: c9 8b       ..    
    beq loop_c8b7d                                                    ; 8b89: f0 f2       ..    
    lda l000c                                                         ; 8b8b: a5 0c       ..    
    cmp #7                                                            ; 8b8d: c9 07       ..    
    beq loop_c8b41                                                    ; 8b8f: f0 b0       ..    
    jsr sub_c9890                                                     ; 8b91: 20 90 98     ..   
    bne c8ba3                                                         ; 8b94: d0 0d       ..    
; &8b96 referenced 1 time by &8b71
.c8b96
    dec l000a                                                         ; 8b96: c6 0a       ..    
    jsr sub_c9857                                                     ; 8b98: 20 57 98     W.   
; &8b9b referenced 2 times by &8bf8, &8c08
.c8b9b
    ldy #0                                                            ; 8b9b: a0 00       ..    
    lda (l000b),y                                                     ; 8b9d: b1 0b       ..    
    cmp #&3a ; ':'                                                    ; 8b9f: c9 3a       .:    
    bne loop_c8b87                                                    ; 8ba1: d0 e4       ..    
; &8ba3 referenced 3 times by &8501, &8b94, &8bab
.c8ba3
    ldy l000a                                                         ; 8ba3: a4 0a       ..    
    inc l000a                                                         ; 8ba5: e6 0a       ..    
    lda (l000b),y                                                     ; 8ba7: b1 0b       ..    
    cmp #&20 ; ' '                                                    ; 8ba9: c9 20       .     
    beq c8ba3                                                         ; 8bab: f0 f6       ..    
    cmp #&cf                                                          ; 8bad: c9 cf       ..    
    bcc c8bbf                                                         ; 8baf: 90 0e       ..    
; &8bb1 referenced 2 times by &8b3d, &ae0d
.c8bb1
    tax                                                               ; 8bb1: aa          .     
    lda l82df,x                                                       ; 8bb2: bd df 82    ...   
    sta l0037                                                         ; 8bb5: 85 37       .7    
    lda l8351,x                                                       ; 8bb7: bd 51 83    .Q.   
    sta l0038                                                         ; 8bba: 85 38       .8    
    jmp (l0037)                                                       ; 8bbc: 6c 37 00    l7.   
; &8bbf referenced 2 times by &8b3f, &8baf
.c8bbf
    ldx l000b                                                         ; 8bbf: a6 0b       ..    
    stx l0019                                                         ; 8bc1: 86 19       ..    
    ldx l000c                                                         ; 8bc3: a6 0c       ..    
    stx l001a                                                         ; 8bc5: 86 1a       ..    
    sty l001b                                                         ; 8bc7: 84 1b       ..    
    jsr sub_c95dd                                                     ; 8bc9: 20 dd 95     ..   
    bne c8be9                                                         ; 8bcc: d0 1b       ..    
    bcs loop_c8b60                                                    ; 8bce: b0 90       ..    
    stx l001b                                                         ; 8bd0: 86 1b       ..    
    jsr sub_c9841                                                     ; 8bd2: 20 41 98     A.   
    jsr sub_c94fc                                                     ; 8bd5: 20 fc 94     ..   
    ldx #5                                                            ; 8bd8: a2 05       ..    
    cpx l002c                                                         ; 8bda: e4 2c       .,    
    bne c8bdf                                                         ; 8bdc: d0 01       ..    
    inx                                                               ; 8bde: e8          .     
; &8bdf referenced 1 time by &8bdc
.c8bdf
    jsr sub_c9531                                                     ; 8bdf: 20 31 95     1.   
    dec l000a                                                         ; 8be2: c6 0a       ..    
    jsr sub_c9582                                                     ; 8be4: 20 82 95     ..   
    beq c8c0b                                                         ; 8be7: f0 22       ."    
; &8be9 referenced 1 time by &8bcc
.c8be9
    bcc c8bfb                                                         ; 8be9: 90 10       ..    
    jsr sub_cbd94                                                     ; 8beb: 20 94 bd     ..   
    jsr c9813                                                         ; 8bee: 20 13 98     ..   
    lda l0027                                                         ; 8bf1: a5 27       .'    
    bne c8c0e                                                         ; 8bf3: d0 19       ..    
    jsr sub_c8c1e                                                     ; 8bf5: 20 1e 8c     ..   
    jmp c8b9b                                                         ; 8bf8: 4c 9b 8b    L..   
; &8bfb referenced 1 time by &8be9
.c8bfb
    jsr sub_cbd94                                                     ; 8bfb: 20 94 bd     ..   
    jsr c9813                                                         ; 8bfe: 20 13 98     ..   
    lda l0027                                                         ; 8c01: a5 27       .'    
    beq c8c0e                                                         ; 8c03: f0 09       ..    
    jsr sub_cb4b4                                                     ; 8c05: 20 b4 b4     ..   
    jmp c8b9b                                                         ; 8c08: 4c 9b 8b    L..   
; &8c0b referenced 1 time by &8be7
.c8c0b
    jmp c982a                                                         ; 8c0b: 4c 2a 98    L*.   
; &8c0e referenced 9 times by &8867, &8bf3, &8c03, &92f7, &9a9a, &9c88, &9d39, &ad67, &b4ae
.c8c0e
    brk                                                               ; 8c0e: 00          .     
    equb &06                                                          ; 8c0f: 06          .     
    equs "Type mismatch"                                              ; 8c10: 54 79 70... Typ...
    equb &00                                                          ; 8c1d: 00          .     
; &8c1e referenced 1 time by &8bf5
.sub_c8c1e
    jsr sub_cbdea                                                     ; 8c1e: 20 ea bd     ..   
    lda l002c                                                         ; 8c21: a5 2c       .,    
    cmp #&80                                                          ; 8c23: c9 80       ..    
    beq c8ca2                                                         ; 8c25: f0 7b       .{    
    ldy #2                                                            ; 8c27: a0 02       ..    
    lda (l002a),y                                                     ; 8c29: b1 2a       .*    
    cmp l0036                                                         ; 8c2b: c5 36       .6    
    bcs c8c84                                                         ; 8c2d: b0 55       .U    
    lda l0002                                                         ; 8c2f: a5 02       ..    
    sta l002c                                                         ; 8c31: 85 2c       .,    
    lda l0003                                                         ; 8c33: a5 03       ..    
    sta l002d                                                         ; 8c35: 85 2d       .-    
    lda l0036                                                         ; 8c37: a5 36       .6    
    cmp #8                                                            ; 8c39: c9 08       ..    
    bcc c8c43                                                         ; 8c3b: 90 06       ..    
    adc #7                                                            ; 8c3d: 69 07       i.    
    bcc c8c43                                                         ; 8c3f: 90 02       ..    
    lda #&ff                                                          ; 8c41: a9 ff       ..    
; &8c43 referenced 2 times by &8c3b, &8c3f
.c8c43
    clc                                                               ; 8c43: 18          .     
    pha                                                               ; 8c44: 48          H     
    tax                                                               ; 8c45: aa          .     
    lda (l002a),y                                                     ; 8c46: b1 2a       .*    
    ldy #0                                                            ; 8c48: a0 00       ..    
    adc (l002a),y                                                     ; 8c4a: 71 2a       q*    
    eor l0002                                                         ; 8c4c: 45 02       E.    
    bne c8c5f                                                         ; 8c4e: d0 0f       ..    
    iny                                                               ; 8c50: c8          .     
    adc (l002a),y                                                     ; 8c51: 71 2a       q*    
    eor l0003                                                         ; 8c53: 45 03       E.    
    bne c8c5f                                                         ; 8c55: d0 08       ..    
    sta l002d                                                         ; 8c57: 85 2d       .-    
    txa                                                               ; 8c59: 8a          .     
    iny                                                               ; 8c5a: c8          .     
    sec                                                               ; 8c5b: 38          8     
    sbc (l002a),y                                                     ; 8c5c: f1 2a       .*    
    tax                                                               ; 8c5e: aa          .     
; &8c5f referenced 2 times by &8c4e, &8c55
.c8c5f
    txa                                                               ; 8c5f: 8a          .     
    clc                                                               ; 8c60: 18          .     
    adc l0002                                                         ; 8c61: 65 02       e.    
    tay                                                               ; 8c63: a8          .     
    lda l0003                                                         ; 8c64: a5 03       ..    
    adc #0                                                            ; 8c66: 69 00       i.    
    cpy l0004                                                         ; 8c68: c4 04       ..    
    tax                                                               ; 8c6a: aa          .     
    sbc l0005                                                         ; 8c6b: e5 05       ..    
    bcs c8cb7                                                         ; 8c6d: b0 48       .H    
    sty l0002                                                         ; 8c6f: 84 02       ..    
    stx l0003                                                         ; 8c71: 86 03       ..    
    pla                                                               ; 8c73: 68          h     
    ldy #2                                                            ; 8c74: a0 02       ..    
    sta (l002a),y                                                     ; 8c76: 91 2a       .*    
    dey                                                               ; 8c78: 88          .     
    lda l002d                                                         ; 8c79: a5 2d       .-    
    beq c8c84                                                         ; 8c7b: f0 07       ..    
    sta (l002a),y                                                     ; 8c7d: 91 2a       .*    
    dey                                                               ; 8c7f: 88          .     
    lda l002c                                                         ; 8c80: a5 2c       .,    
    sta (l002a),y                                                     ; 8c82: 91 2a       .*    
; &8c84 referenced 2 times by &8c2d, &8c7b
.c8c84
    ldy #3                                                            ; 8c84: a0 03       ..    
    lda l0036                                                         ; 8c86: a5 36       .6    
    sta (l002a),y                                                     ; 8c88: 91 2a       .*    
    beq return_5                                                      ; 8c8a: f0 15       ..    
    dey                                                               ; 8c8c: 88          .     
    dey                                                               ; 8c8d: 88          .     
    lda (l002a),y                                                     ; 8c8e: b1 2a       .*    
    sta l002d                                                         ; 8c90: 85 2d       .-    
    dey                                                               ; 8c92: 88          .     
    lda (l002a),y                                                     ; 8c93: b1 2a       .*    
    sta l002c                                                         ; 8c95: 85 2c       .,    
; &8c97 referenced 1 time by &8c9f
.loop_c8c97
    lda l0600,y                                                       ; 8c97: b9 00 06    ...   
    sta (l002c),y                                                     ; 8c9a: 91 2c       .,    
    iny                                                               ; 8c9c: c8          .     
    cpy l0036                                                         ; 8c9d: c4 36       .6    
    bne loop_c8c97                                                    ; 8c9f: d0 f6       ..    
; &8ca1 referenced 1 time by &8c8a
.return_5
    rts                                                               ; 8ca1: 60          `     
; &8ca2 referenced 1 time by &8c25
.c8ca2
    jsr sub_cbeba                                                     ; 8ca2: 20 ba be     ..   
    cpy #0                                                            ; 8ca5: c0 00       ..    
    beq c8cb4                                                         ; 8ca7: f0 0b       ..    
; &8ca9 referenced 1 time by &8caf
.loop_c8ca9
    lda l0600,y                                                       ; 8ca9: b9 00 06    ...   
    sta (l002a),y                                                     ; 8cac: 91 2a       .*    
    dey                                                               ; 8cae: 88          .     
    bne loop_c8ca9                                                    ; 8caf: d0 f8       ..    
    lda l0600                                                         ; 8cb1: ad 00 06    ...   
; &8cb4 referenced 1 time by &8ca7
.c8cb4
    sta (l002a),y                                                     ; 8cb4: 91 2a       .*    
    rts                                                               ; 8cb6: 60          `     
; &8cb7 referenced 3 times by &8c6d, &9553, &be41
.c8cb7
    brk                                                               ; 8cb7: 00          .     
    equb &00                                                          ; 8cb8: 00          .     
    equs "No room"                                                    ; 8cb9: 4e 6f 20... No ...
    equb &00, &a5, &39, &c9, &80, &f0, &27, &90, &3a, &a0, &00, &b1   ; 8cc0: 00 a5 39... ..9...
    equb &04, &aa, &f0, &15, &b1, &37, &e9, &01, &85, &39, &c8, &b1   ; 8ccc: 04 aa f0... ......
    equb &37, &e9, &00, &85, &3a, &b1, &04, &91, &39, &c8, &ca, &d0   ; 8cd8: 37 e9 00... 7.....
    equb &f8, &a1, &04, &a0, &03, &91, &37, &4c, &dc, &bd, &a0, &00   ; 8ce4: f8 a1 04... ......
    equb &b1, &04, &aa, &f0, &0a, &c8, &b1, &04, &88, &91, &37, &c8   ; 8cf0: b1 04 aa... ......
    equb &ca, &d0, &f6, &a9, &0d, &d0, &e6, &a0, &00, &b1, &04, &91   ; 8cfc: ca d0 f6... ......
    equb &37, &c8, &c4, &39, &b0, &18, &b1, &04, &91, &37, &c8, &b1   ; 8d08: 37 c8 c4... 7.....
    equb &04, &91, &37, &c8, &b1, &04, &91, &37, &c8, &c4, &39, &b0   ; 8d14: 04 91 37... ..7...
    equb &05, &b1, &04, &91, &37, &c8, &98, &18, &4c, &e1, &bd, &c6   ; 8d20: 05 b1 04... ......
    equb &0a, &20, &a9, &bf, &98, &48, &20, &8c, &8a, &c9, &2c, &d0   ; 8d2c: 0a 20 a9... . ....
    equs "> )"                                                        ; 8d38: 3e 20 29    > )   
    equb &9b, &20, &85, &a3, &68, &a8, &a5, &27, &20, &d4, &ff, &aa   ; 8d3b: 9b 20 85... . ....
    equb &f0, &1b, &30, &0c, &a2, &03, &b5, &2a, &20, &d4, &ff, &ca   ; 8d47: f0 1b 30... ..0...
    equb &10, &f8, &30, &d9, &a2, &04, &bd, &6c, &04, &20, &d4, &ff   ; 8d53: 10 f8 30... ..0...
    equb &ca, &10, &f7, &30, &cc, &a5, &36, &20, &d4, &ff, &aa, &f0   ; 8d5f: ca 10 f7... ......
    equb &c4, &bd, &ff, &05, &20, &d4, &ff, &ca, &d0, &f7, &f0, &b9   ; 8d6b: c4 bd ff... ......
    equb &68, &84, &0a, &4c, &98, &8b, &20, &25, &bc, &4c, &96, &8b   ; 8d77: 68 84 0a... h.....
    equb &a9, &00, &85, &14, &85, &15, &20, &97, &8a, &c9, &3a, &f0   ; 8d83: a9 00 85... ......
    equb &f0, &c9, &0d, &f0, &ec, &c9, &8b, &f0, &e8, &d0, &38, &20   ; 8d8f: f0 c9 0d... ......
    equb &97, &8a, &c9, &23, &f0, &8a, &c6, &0a, &4c, &bb, &8d, &ad   ; 8d9b: 97 8a c9... ......
    equb &00, &04, &f0, &10, &a5, &1e, &f0, &0c, &ed, &00, &04, &b0   ; 8da7: 00 04 f0... ......
    equb &f9, &a8, &20, &65, &b5, &c8, &d0, &fa, &18, &ad, &00, &04   ; 8db3: f9 a8 20... .. ...
    equb &85, &14, &66, &15, &20, &97, &8a, &c9, &3a, &f0, &b3, &c9   ; 8dbf: 85 14 66... ..f...
    equb &0d, &f0, &af, &c9, &8b, &f0, &ab, &c9, &7e, &f0, &eb, &c9   ; 8dcb: 0d f0 af... ......
    equb &2c, &f0, &cc, &c9, &3b, &f0, &a5, &20, &70, &8e, &90, &e0   ; 8dd7: 2c f0 cc... ,.....
    equb &a5, &14, &48, &a5, &15, &48, &c6, &1b, &20, &29, &9b, &68   ; 8de3: a5 14 48... ..H...
    equb &85, &15, &68, &85, &14, &a5, &1b, &85, &0a, &98, &f0, &13   ; 8def: 85 15 68... ..h...
    equb &20, &df, &9e, &a5, &14, &38, &e5, &36, &90, &09, &f0, &07   ; 8dfb: 20 df 9e...  .....
    equb &a8, &20, &65, &b5, &88, &d0, &fa, &a5, &36, &f0, &b1, &a0   ; 8e07: a8 20 65... . e...
    equb &00, &b9, &00, &06, &20, &58, &b5, &c8, &c4, &36, &d0, &f5   ; 8e13: 00 b9 00... ......
    equb &f0, &a2, &4c, &a2, &8a, &c9, &2c, &d0, &f9, &a5             ; 8e1f: f0 a2 4c... ..L...
    equs "*H V"                                                       ; 8e29: 2a 48 20... *H ...
    equb &ae, &20, &f0, &92, &a9, &1f, &20, &ee, &ff, &68, &20, &ee   ; 8e2d: ae 20 f0... . ....
    equb &ff, &20, &56, &94, &4c, &6a, &8e, &20, &dd, &92, &20, &8c   ; 8e39: ff 20 56... . V...
    equb &8a, &c9, &29, &d0, &da, &a5, &2a, &e5, &1e, &f0, &1a, &a8   ; 8e45: 8a c9 29... ..)...
    equb &b0, &0c, &20, &25, &bc, &f0, &03, &20, &e3, &92, &a4, &2a   ; 8e51: b0 0c 20... .. ...
    equb &f0, &0b, &20, &65, &b5, &88, &d0, &fa, &f0, &03, &20, &25   ; 8e5d: f0 0b 20... .. ...
    equb &bc, &18, &a4, &1b, &84, &0a, &60, &a6, &0b, &86, &19, &a6   ; 8e69: bc 18 a4... ......
    equb &0c, &86, &1a, &a6, &0a, &86, &1b, &c9, &27, &f0, &e7, &c9   ; 8e75: 0c 86 1a... ......
    equb &8a, &f0, &bc, &c9, &89, &f0, &d0                            ; 8e81: 8a f0 bc... ......
    equs "8` "                                                        ; 8e88: 38 60 20    8`    
    equb &97, &8a, &20, &70, &8e, &90, &f7, &c9, &22, &f0, &11, &38   ; 8e8b: 97 8a 20... .. ...
    equb &60                                                          ; 8e97: 60          `     
; &8e98 referenced 1 time by &ade9
.c8e98
    brk                                                               ; 8e98: 00          .     
    equb &09                                                          ; 8e99: 09          .     
    equs "Missing ", &22                                              ; 8e9a: 4d 69 73... Mis...
    equb &00, &20, &58, &b5, &c8, &b1, &19, &c9, &0d, &f0, &ea, &c9   ; 8ea3: 00 20 58... . X...
    equb &22, &d0, &f2, &c8, &84, &1b, &b1, &19, &c9, &22, &d0, &af   ; 8eaf: 22 d0 f2... ".....
    equb &f0, &e7, &20, &57, &98, &a9, &10, &d0, &08, &20, &57, &98   ; 8ebb: f0 e7 20... .. ...
    equb &20, &28, &bc, &a9, &0c, &20, &ee, &ff, &4c, &9b, &8b, &20   ; 8ec7: 20 28 bc...  (....
    equb &1d, &9b, &20, &ee, &92, &20, &94, &bd, &a0, &00, &8c, &00   ; 8ed3: 1d 9b 20... .. ...
    equb &06, &8c, &ff, &06, &20, &8c, &8a, &c9, &2c, &d0, &22, &a4   ; 8edf: 06 8c ff... ......
    equb &1b, &20, &d5, &95, &f0, &2a, &ac, &ff, &06, &c8, &a5, &2a   ; 8eeb: 1b 20 d5... . ....
    equb &99, &00, &06, &c8, &a5, &2b, &99, &00, &06, &c8, &a5, &2c   ; 8ef7: 99 00 06... ......
    equb &99, &00, &06, &ee, &00, &06, &4c, &e0, &8e, &c6, &1b, &20   ; 8f03: 99 00 06... ......
    equb &52, &98, &20, &ea, &bd, &20, &1e, &8f, &d8, &4c, &9b, &8b   ; 8f0f: 52 98 20... R. ...
    equb &4c, &43, &ae, &ad, &0c, &04, &4a, &ad, &04, &04, &ae, &60   ; 8f1b: 4c 43 ae... LC....
    equb &04, &ac, &64, &04, &6c, &2a, &00, &4c, &2a, &98, &20, &df   ; 8f27: 04 ac 64... ..d...
    equb &97, &90, &f8, &20, &94, &bd, &20, &97, &8a, &c9, &2c, &d0   ; 8f33: 97 90 f8... ......
    equb &ee, &20, &df, &97, &90, &e9, &20, &57, &98, &a5, &2a, &85   ; 8f3f: ee 20 df... . ....
    equb &39, &a5, &2b, &85, &3a, &20, &ea, &bd, &20, &2d, &bc, &20   ; 8f4b: 39 a5 2b... 9.+...
    equb &7b, &98, &20, &22, &92, &a5, &39, &c5, &2a, &a5, &3a, &e5   ; 8f57: 7b 98 20... {. ...
    equb &2b, &b0, &ed, &4c, &f3, &8a, &a9, &0a, &20, &d8, &ae, &20   ; 8f63: 2b b0 ed... +.....
    equb &df, &97, &20, &94, &bd, &a9, &0a, &20, &d8, &ae, &20, &97   ; 8f6f: df 97 20... .. ...
    equb &8a, &c9, &2c, &d0, &0d, &20, &df, &97, &a5, &2b, &d0, &58   ; 8f7b: 8a c9 2c... ..,...
    equb &a5, &2a, &f0, &54, &e6, &0a, &c6, &0a, &4c, &57, &98, &a5   ; 8f87: a5 2a f0... .*....
    equb &12, &85, &3b, &a5, &13, &85, &3c, &a5, &18, &85, &38, &a9   ; 8f93: 12 85 3b... ..;...
    equb &01, &85                                                     ; 8f9f: 01 85       ..    
    equs "7` i"                                                       ; 8fa1: 37 60 20... 7` ...
    equb &8f, &a2, &39, &20, &0d, &be, &20, &6f, &be, &20, &92, &8f   ; 8fa5: 8f a2 39... ..9...
    equb &a0, &00, &b1                                                ; 8fb1: a0 00 b1    ...   
    equs "700"                                                        ; 8fb4: 37 30 30    700   
    equb &91, &3b, &c8, &b1, &37, &91, &3b, &38, &98, &65, &3b, &85   ; 8fb7: 91 3b c8... .;....
    equb &3b, &aa, &a5, &3c, &69, &00, &85, &3c, &e4, &06, &e5, &07   ; 8fc3: 3b aa a5... ;.....
    equb &b0, &05, &20, &9f, &90, &90, &db, &00, &00, &cc             ; 8fcf: b0 05 20... .. ...
    equs " space"                                                     ; 8fd9: 20 73 70...  sp...
    equb &00, &00                                                     ; 8fdf: 00 00       ..    
    equs "Silly"                                                      ; 8fe1: 53 69 6c... Sil...
    equb &00, &20, &9a, &8f, &a0, &00, &b1, &37, &30, &1d, &a5, &3a   ; 8fe6: 00 20 9a... . ....
    equb &91, &37, &a5, &39, &c8, &91, &37, &18, &a5                  ; 8ff2: 91 37 a5... .7....
    equs "*e9"                                                        ; 8ffb: 2a 65 39    *e9   
    equb &85, &39, &a9, &00                                           ; 8ffe: 85 39 a9... .9....
    equs "e:)"                                                        ; 9002: 65 3a 29    e:)   
    equb &7f, &85, &3a, &20, &9f, &90, &90, &dd, &a5, &18, &85, &0c   ; 9005: 7f 85 3a... ..:...
    equb &a0, &00, &84, &0b, &c8, &b1, &0b, &30, &20, &a0, &04, &b1   ; 9011: a0 00 84... ......
    equb &0b, &c9, &8d, &f0, &1b, &c8, &c9, &0d, &d0, &f5, &b1, &0b   ; 901d: 0b c9 8d... ......
    equb &30, &0f, &a0, &03, &b1, &0b, &18, &65, &0b, &85, &0b, &90   ; 9029: 30 0f a0... 0.....
    equb &e4, &e6, &0c, &b0, &e0, &4c, &f3, &8a, &20, &eb, &97, &20   ; 9035: e4 e6 0c... ......
    equb &92, &8f, &a0, &00, &b1                                      ; 9041: 92 8f a0... ......
    equs "707"                                                        ; 9046: 37 30 37    707   
    equb &b1, &3b, &c8, &c5, &2b, &d0, &21, &b1, &3b, &c5, &2a, &d0   ; 9049: b1 3b c8... .;....
    equb &1b, &b1, &37, &85, &3d, &88, &b1, &37, &85, &3e, &a4, &0a   ; 9055: 1b b1 37... ..7...
    equb &88, &a5, &0b, &85, &37, &a5, &0c, &85, &38, &20, &f5, &88   ; 9061: 88 a5 0b... ......
    equb &a4, &0a, &d0, &ab, &20, &9f, &90, &a5, &3b, &69, &02, &85   ; 906d: a4 0a d0... ......
    equb &3b, &90, &c7, &e6, &3c, &b0, &c3, &20, &cf, &bf             ; 9079: 3b 90 c7... ;.....
    equs "Failed at "                                                 ; 9083: 46 61 69... Fai...
    equb &c8, &b1, &0b, &85, &2b, &c8, &b1, &0b, &85, &2a, &20, &1f   ; 908d: c8 b1 0b... ......
    equb &99, &20, &25, &bc, &f0, &ce, &c8, &b1                       ; 9099: 99 20 25... . %...
    equs "7e7"                                                        ; 90a1: 37 65 37    7e7   
    equb &85, &37, &90, &03, &e6, &38, &18                            ; 90a4: 85 37 90... .7....
    equs "` i"                                                        ; 90ab: 60 20 69    ` i   
    equb &8f, &a5                                                     ; 90ae: 8f a5       ..    
    equs "*H "                                                        ; 90b0: 2a 48 20    *H    
    equb &ea, &bd, &20, &94, &bd, &20, &23, &99, &a9, &20, &20, &02   ; 90b3: ea bd 20... .. ...
    equb &bc, &20, &ea, &bd, &20, &51, &89, &20, &8d, &bc, &20, &20   ; 90bf: bc 20 ea... . ....
    equb &bd, &68, &48, &18, &65, &2a, &85, &2a, &90, &e0, &e6, &2b   ; 90cb: bd 68 48... .hH...
    equb &10, &dc, &4c, &f3, &8a, &4c, &18, &92, &c6, &0a, &20, &82   ; 90d7: 10 dc 4c... ..L...
    equb &95, &f0, &41, &b0, &3f, &20, &94, &bd, &20, &dd, &92, &20   ; 90e3: 95 f0 41... ..A...
    equb &22, &92, &a5, &2d, &05, &2c, &d0, &30, &18, &a5, &2a, &65   ; 90ef: 22 92 a5... ".....
    equb &02, &a8, &a5, &2b, &65, &03, &aa, &c4, &04, &e5, &05, &b0   ; 90fb: 02 a8 a5... ......
    equb &d4, &a5, &02, &85, &2a, &a5, &03, &85, &2b, &84, &02, &86   ; 9107: d4 a5 02... ......
    equb &03, &a9, &00, &85, &2c, &85, &2d, &a9, &40, &85, &27, &20   ; 9113: 03 a9 00... ......
    equb &b4, &b4, &20, &27, &88, &4c, &0b, &92                       ; 911f: b4 b4 20... .. ...
; &9127 referenced 1 time by &925a
.c9127
    brk                                                               ; 9127: 00          .     
    equb &0a                                                          ; 9128: 0a          .     
    equs "Bad "                                                       ; 9129: 42 61 64... Bad...
    equb &de, &00, &20, &97, &8a, &98, &18, &65, &0b, &a6, &0c, &90   ; 912d: de 00 20... .. ...
    equb &02, &e8, &18, &e9, &00, &85, &37, &8a, &e9, &00, &85, &38   ; 9139: 02 e8 18... ......
    equb &a2, &05, &86, &3f, &a6, &0a, &20, &59, &95, &c0, &01, &f0   ; 9145: a2 05 86... ......
    equb &d5, &c9, &28, &f0, &15, &c9, &24, &f0, &04, &c9, &25, &d0   ; 9151: d5 c9 28... ..(...
    equb &0a, &c6, &3f, &c8, &e8, &b1, &37, &c9, &28, &f0, &03, &4c   ; 915d: 0a c6 3f... ..?...
    equb &df, &90, &84, &39, &86, &0a, &20, &69, &94, &d0, &b3, &20   ; 9169: df 90 84... ......
    equb &fc, &94, &a2, &01, &20, &31, &95, &a5, &3f, &48, &a9, &01   ; 9175: fc 94 a2... ......
    equb &48, &20, &d8, &ae, &20, &94, &bd, &20, &21, &88, &a5, &2b   ; 9181: 48 20 d8... H ....
    equb &29, &c0, &05, &2c, &05, &2d, &d0, &92, &20, &22, &92, &68   ; 918d: 29 c0 05... ).....
    equb &a8, &a5, &2a, &91, &02, &c8, &a5, &2b, &91, &02, &c8, &98   ; 9199: a8 a5 2a... ..*...
    equs "H 1"                                                        ; 91a5: 48 20 31    H 1   
    equb &92, &20, &97, &8a, &c9, &2c, &f0, &d5, &c9, &29, &f0, &03   ; 91a8: 92 20 97... . ....
    equb &4c, &27, &91, &68, &85, &15, &68, &85, &3f, &a9, &00, &85   ; 91b4: 4c 27 91... L'....
    equs "@ 6"                                                        ; 91c0: 40 20 36    @ 6   
    equb &92, &a0, &00, &a5, &15, &91, &02, &65, &2a, &85, &2a, &90   ; 91c3: 92 a0 00... ......
    equb &02, &e6, &2b, &a5, &03, &85, &38, &a5, &02, &85, &37, &18   ; 91cf: 02 e6 2b... ..+...
    equb &65, &2a, &a8, &a5, &2b, &65, &03, &b0, &34, &aa, &c4, &04   ; 91db: 65 2a a8... e*....
    equb &e5, &05, &b0, &2d, &84, &02, &86, &03, &a5, &37, &65, &15   ; 91e7: e5 05 b0... ......
    equb &a8, &a9, &00, &85, &37, &90, &02, &e6, &38, &91, &37, &c8   ; 91f3: a8 a9 00... ......
    equb &d0, &02, &e6, &38, &c4, &02, &d0, &f5, &e4, &38, &d0, &f1   ; 91ff: d0 02 e6... ......
    equb &20, &97, &8a, &c9, &2c, &f0, &03, &4c, &96, &8b, &4c, &2f   ; 920b: 20 97 8a...  .....
    equb &91, &00, &0b, &de                                           ; 9217: 91 00 0b... ......
    equs " space"                                                     ; 921b: 20 73 70...  sp...
    equb &00, &e6, &2a, &d0, &0a, &e6, &2b, &d0, &06, &e6, &2c, &d0   ; 9221: 00 e6 2a... ..*...
    equb &02, &e6, &2d, &60, &a2, &3f, &20, &0d, &be                  ; 922d: 02 e6 2d... ..-...
; &9236 referenced 1 time by &9736
.sub_c9236
    ldx #0                                                            ; 9236: a2 00       ..    
    ldy #0                                                            ; 9238: a0 00       ..    
; &923a referenced 1 time by &9253
.loop_c923a
    lsr l0040                                                         ; 923a: 46 40       F@    
    ror l003f                                                         ; 923c: 66 3f       f?    
    bcc c924b                                                         ; 923e: 90 0b       ..    
    clc                                                               ; 9240: 18          .     
    tya                                                               ; 9241: 98          .     
    adc l002a                                                         ; 9242: 65 2a       e*    
    tay                                                               ; 9244: a8          .     
    txa                                                               ; 9245: 8a          .     
    adc l002b                                                         ; 9246: 65 2b       e+    
    tax                                                               ; 9248: aa          .     
    bcs c925a                                                         ; 9249: b0 0f       ..    
; &924b referenced 1 time by &923e
.c924b
    asl l002a                                                         ; 924b: 06 2a       .*    
    rol l002b                                                         ; 924d: 26 2b       &+    
    lda l003f                                                         ; 924f: a5 3f       .?    
    ora l0040                                                         ; 9251: 05 40       .@    
    bne loop_c923a                                                    ; 9253: d0 e5       ..    
    sty l002a                                                         ; 9255: 84 2a       .*    
    stx l002b                                                         ; 9257: 86 2b       .+    
    rts                                                               ; 9259: 60          `     
; &925a referenced 1 time by &9249
.c925a
    jmp c9127                                                         ; 925a: 4c 27 91    L'.   
    equb &20, &eb, &92, &a5, &2a, &85, &06, &85, &04, &a5, &2b, &85   ; 925d: 20 eb 92...  .....
    equb &07, &85, &05, &4c, &9b, &8b, &20, &eb, &92, &a5, &2a, &85   ; 9269: 07 85 05... ......
    equb &00, &85, &02, &a5, &2b, &85, &01, &85, &03, &20, &2f, &bd   ; 9275: 00 85 02... ......
    equb &f0, &07, &20, &eb, &92, &a5, &2b, &85, &18, &4c, &9b, &8b   ; 9281: f0 07 20... .. ...
    equb &20, &57, &98, &20, &20, &bd, &f0, &f5, &20, &df, &97, &b0   ; 928d: 20 57 98...  W....
    equb &0b, &c9, &ee, &f0, &19, &c9, &87, &f0, &1e, &20, &21, &88   ; 9299: 0b c9 ee... ......
    equb &20, &57, &98, &a5, &2a, &85, &21, &a5, &2b, &85, &22, &a9   ; 92a5: 20 57 98...  W....
    equb &ff, &85, &20, &4c, &9b, &8b, &e6, &0a, &20, &57, &98, &a9   ; 92b1: ff 85 20... .. ...
    equb &ff, &d0, &ee, &e6, &0a, &20, &57, &98, &a9, &00, &f0, &e9   ; 92bd: ff d0 ee... ......
    equb &20, &eb, &92, &a2, &2a, &a0, &00, &84, &2e, &a9, &02, &20   ; 92c9: 20 eb 92...  .....
    equb &f1, &ff, &4c, &9b, &8b, &20, &ae, &8a                       ; 92d5: f1 ff 4c... ..L...
; &92dd referenced 1 time by &9702
.sub_c92dd
    jsr sub_c9b29                                                     ; 92dd: 20 29 9b     ).   
    jmp c92f0                                                         ; 92e0: 4c f0 92    L..   
; &92e3 referenced 3 times by &95aa, &95b2, &9691
.sub_c92e3
    jsr cadec                                                         ; 92e3: 20 ec ad     ..   
    beq c92f7                                                         ; 92e6: f0 0f       ..    
    bmi c92f4                                                         ; 92e8: 30 0a       0.    
; &92ea referenced 2 times by &92f2, &92ff
.return_6
    rts                                                               ; 92ea: 60          `     
    equb &20, &07, &98, &a5, &27                                      ; 92eb: 20 07 98...  .....
; &92f0 referenced 12 times by &8824, &92e0, &9688, &974a, &976f, &99bf, &99ce, &9b3e, &9b59, &9b6c, &9b7b, &9b85
.c92f0
    beq c92f7                                                         ; 92f0: f0 05       ..    
    bpl return_6                                                      ; 92f2: 10 f6       ..    
; &92f4 referenced 1 time by &92e8
.c92f4
    jmp ca3e4                                                         ; 92f4: 4c e4 a3    L..   
; &92f7 referenced 3 times by &92e6, &92f0, &92fd
.c92f7
    jmp c8c0e                                                         ; 92f7: 4c 0e 8c    L..   
; &92fa referenced 1 time by &9e3c
.sub_c92fa
    jsr cadec                                                         ; 92fa: 20 ec ad     ..   
; &92fd referenced 5 times by &9a59, &9d29, &9de6, &9df2, &9e36
.sub_c92fd
    beq c92f7                                                         ; 92fd: f0 f8       ..    
    bmi return_6                                                      ; 92ff: 30 e9       0.    
    jmp ca2be                                                         ; 9301: 4c be a2    L..   
    equb &a5, &0b, &85, &19, &a5, &0c, &85, &1a, &a5, &0a, &85, &1b   ; 9304: a5 0b 85... ......
    equb &a9, &f2, &20, &97, &b1, &20, &52, &98, &4c, &9b, &8b, &a0   ; 9310: a9 f2 20... .. ...
    equb &03, &a9, &00, &91, &2a, &f0, &1e, &ba, &e0, &fc, &b0, &43   ; 931c: 03 a9 00... ......
    equb &20, &82, &95, &f0, &26, &20, &0d, &b3, &a4, &2c, &30, &e7   ; 9328: 20 82 95...  .....
    equb &20, &94, &bd, &a9, &00, &20, &d8, &ae, &85, &27, &20, &b4   ; 9334: 20 94 bd...  .....
    equb &b4, &ba, &fe, &06, &01, &a4, &1b, &84, &0a, &20, &97, &8a   ; 9340: b4 ba fe... ......
    equb &c9, &2c, &f0, &d3, &4c, &96, &8b, &4c, &98, &8b, &ba, &e0   ; 934c: c9 2c f0... .,....
    equb &fc, &b0, &0a, &ad, &ff, &01, &c9, &f2, &d0, &03, &4c, &57   ; 9358: fc b0 0a... ......
    equb &98, &00, &0d                                                ; 9364: 98 00 0d    ...   
    equs "No "                                                        ; 9367: 4e 6f 20    No    
    equb &f2, &00, &0c                                                ; 936a: f2 00 0c    ...   
    equs "Not "                                                       ; 936d: 4e 6f 74... Not...
    equb &ea, &00, &19                                                ; 9371: ea 00 19    ...   
    equs "Bad "                                                       ; 9374: 42 61 64... Bad...
    equb &eb, &00, &20, &21, &88, &a5                                 ; 9378: eb 00 20... .. ...
    equs "*H "                                                        ; 937e: 2a 48 20    *H    
    equb &da, &92, &20, &52, &98, &a9, &12, &20, &ee, &ff, &4c, &da   ; 9381: da 92 20... .. ...
    equb &93, &a9, &11                                                ; 938d: 93 a9 11    ...   
    equs "H !"                                                        ; 9390: 48 20 21    H !   
    equb &88, &20, &57, &98, &4c, &da, &93, &a9, &16                  ; 9393: 88 20 57... . W...
    equs "H !"                                                        ; 939c: 48 20 21    H !   
    equb &88, &20, &57, &98, &20, &e7, &be, &e0, &ff, &d0, &2d, &c0   ; 939f: 88 20 57... . W...
    equb &ff, &d0, &29, &a5, &04, &c5, &06, &d0, &be, &a5, &05, &c5   ; 93ab: ff d0 29... ..)...
    equb &07, &d0, &b8, &a6, &2a, &a9, &85, &20, &f4, &ff, &e4, &02   ; 93b7: 07 d0 b8... ......
    equb &98, &e5, &03, &90, &aa, &e4, &12, &98, &e5, &13, &90, &a3   ; 93c3: 98 e5 03... ......
    equb &86, &06, &86, &04, &84, &07, &84, &05, &20, &28, &bc, &68   ; 93cf: 86 06 86... ......
    equb &20, &ee, &ff, &20, &56, &94, &4c, &9b, &8b, &a9, &04, &d0   ; 93db: 20 ee ff...  .....
    equb &02, &a9, &05, &48, &20, &1d, &9b, &4c, &fd, &93, &20, &21   ; 93e7: 02 a9 05... ......
    equb &88, &a5                                                     ; 93f3: 88 a5       ..    
    equs "*H "                                                        ; 93f5: 2a 48 20    *H    
    equb &ae, &8a, &20, &29, &9b, &20, &ee, &92, &20, &94, &bd, &20   ; 93f8: ae 8a 20... .. ...
    equb &da, &92, &20, &52, &98, &a9, &19, &20, &ee, &ff, &68, &20   ; 9404: da 92 20... .. ...
    equb &ee, &ff, &20, &0b, &be, &a5, &37, &20, &ee, &ff, &a5, &38   ; 9410: ee ff 20... .. ...
    equb &20, &ee, &ff, &20, &56, &94, &a5, &2b, &20, &ee, &ff, &4c   ; 941c: 20 ee ff...  .....
    equb &9b, &8b, &a5, &2b, &20, &ee, &ff, &20, &97, &8a, &c9, &3a   ; 9428: 9b 8b a5... ......
    equb &f0, &1d, &c9, &0d, &f0, &19, &c9, &8b, &f0, &15, &c6, &0a   ; 9434: f0 1d c9... ......
    equb &20, &21, &88, &20, &56, &94, &20, &97, &8a, &c9, &2c, &f0   ; 9440: 20 21 88...  !....
    equb &e2, &c9, &3b, &d0, &e1, &f0, &d7, &4c, &96, &8b, &a5, &2a   ; 944c: e2 c9 3b... ..;...
    equb &6c, &0e, &02, &a0, &01, &b1, &37, &a0, &f6, &c9, &f2, &f0   ; 9458: 6c 0e 02... l.....
    equb &0a, &a0, &f8, &d0, &06                                      ; 9464: 0a a0 f8... ......
; &9469 referenced 3 times by &965a, &96bc, &96df
.sub_c9469
    ldy #1                                                            ; 9469: a0 01       ..    
    lda (l0037),y                                                     ; 946b: b1 37       .7    
    asl a                                                             ; 946d: 0a          .     
    tay                                                               ; 946e: a8          .     
    lda l0400,y                                                       ; 946f: b9 00 04    ...   
    sta l003a                                                         ; 9472: 85 3a       .:    
    lda l0401,y                                                       ; 9474: b9 01 04    ...   
    sta l003b                                                         ; 9477: 85 3b       .;    
; &9479 referenced 4 times by &94ca, &94d2, &94d6, &94df
.c9479
    lda l003b                                                         ; 9479: a5 3b       .;    
    beq return_7                                                      ; 947b: f0 35       .5    
    ldy #0                                                            ; 947d: a0 00       ..    
    lda (l003a),y                                                     ; 947f: b1 3a       .:    
    sta l003c                                                         ; 9481: 85 3c       .<    
    iny                                                               ; 9483: c8          .     
    lda (l003a),y                                                     ; 9484: b1 3a       .:    
    sta l003d                                                         ; 9486: 85 3d       .=    
    iny                                                               ; 9488: c8          .     
    lda (l003a),y                                                     ; 9489: b1 3a       .:    
    bne c949a                                                         ; 948b: d0 0d       ..    
    dey                                                               ; 948d: 88          .     
    cpy l0039                                                         ; 948e: c4 39       .9    
    bne c94b3                                                         ; 9490: d0 21       .!    
    iny                                                               ; 9492: c8          .     
    bcs c94a7                                                         ; 9493: b0 12       ..    
; &9495 referenced 1 time by &94a0
.loop_c9495
    iny                                                               ; 9495: c8          .     
    lda (l003a),y                                                     ; 9496: b1 3a       .:    
    beq c94b3                                                         ; 9498: f0 19       ..    
; &949a referenced 1 time by &948b
.c949a
    cmp (l0037),y                                                     ; 949a: d1 37       .7    
    bne c94b3                                                         ; 949c: d0 15       ..    
    cpy l0039                                                         ; 949e: c4 39       .9    
    bne loop_c9495                                                    ; 94a0: d0 f3       ..    
    iny                                                               ; 94a2: c8          .     
    lda (l003a),y                                                     ; 94a3: b1 3a       .:    
    bne c94b3                                                         ; 94a5: d0 0c       ..    
; &94a7 referenced 1 time by &9493
.c94a7
    tya                                                               ; 94a7: 98          .     
    adc l003a                                                         ; 94a8: 65 3a       e:    
    sta l002a                                                         ; 94aa: 85 2a       .*    
    lda l003b                                                         ; 94ac: a5 3b       .;    
    adc #0                                                            ; 94ae: 69 00       i.    
    sta l002b                                                         ; 94b0: 85 2b       .+    
; &94b2 referenced 2 times by &947b, &94b5
.return_7
    rts                                                               ; 94b2: 60          `     
; &94b3 referenced 4 times by &9490, &9498, &949c, &94a5
.c94b3
    lda l003d                                                         ; 94b3: a5 3d       .=    
    beq return_7                                                      ; 94b5: f0 fb       ..    
    ldy #0                                                            ; 94b7: a0 00       ..    
    lda (l003c),y                                                     ; 94b9: b1 3c       .<    
    sta l003a                                                         ; 94bb: 85 3a       .:    
    iny                                                               ; 94bd: c8          .     
    lda (l003c),y                                                     ; 94be: b1 3c       .<    
    sta l003b                                                         ; 94c0: 85 3b       .;    
    iny                                                               ; 94c2: c8          .     
    lda (l003c),y                                                     ; 94c3: b1 3c       .<    
    bne c94d4                                                         ; 94c5: d0 0d       ..    
    dey                                                               ; 94c7: 88          .     
    cpy l0039                                                         ; 94c8: c4 39       .9    
    bne c9479                                                         ; 94ca: d0 ad       ..    
    iny                                                               ; 94cc: c8          .     
    bcs c94e1                                                         ; 94cd: b0 12       ..    
; &94cf referenced 1 time by &94da
.loop_c94cf
    iny                                                               ; 94cf: c8          .     
    lda (l003c),y                                                     ; 94d0: b1 3c       .<    
    beq c9479                                                         ; 94d2: f0 a5       ..    
; &94d4 referenced 1 time by &94c5
.c94d4
    cmp (l0037),y                                                     ; 94d4: d1 37       .7    
    bne c9479                                                         ; 94d6: d0 a1       ..    
    cpy l0039                                                         ; 94d8: c4 39       .9    
    bne loop_c94cf                                                    ; 94da: d0 f3       ..    
    iny                                                               ; 94dc: c8          .     
    lda (l003c),y                                                     ; 94dd: b1 3c       .<    
    bne c9479                                                         ; 94df: d0 98       ..    
; &94e1 referenced 1 time by &94cd
.c94e1
    tya                                                               ; 94e1: 98          .     
    adc l003c                                                         ; 94e2: 65 3c       e<    
    sta l002a                                                         ; 94e4: 85 2a       .*    
    lda l003d                                                         ; 94e6: a5 3d       .=    
    adc #0                                                            ; 94e8: 69 00       i.    
    sta l002b                                                         ; 94ea: 85 2b       .+    
    rts                                                               ; 94ec: 60          `     
    equb &a0, &01, &b1, &37, &aa, &a9, &f6, &e0, &f2, &f0, &09, &a9   ; 94ed: a0 01 b1... ......
    equb &f8, &d0, &05                                                ; 94f9: f8 d0 05    ...   
; &94fc referenced 2 times by &8bd5, &9589
.sub_c94fc
    ldy #1                                                            ; 94fc: a0 01       ..    
    lda (l0037),y                                                     ; 94fe: b1 37       .7    
    asl a                                                             ; 9500: 0a          .     
    sta l003a                                                         ; 9501: 85 3a       .:    
    lda #4                                                            ; 9503: a9 04       ..    
    sta l003b                                                         ; 9505: 85 3b       .;    
; &9507 referenced 1 time by &9514
.loop_c9507
    lda (l003a),y                                                     ; 9507: b1 3a       .:    
    beq c9516                                                         ; 9509: f0 0b       ..    
    tax                                                               ; 950b: aa          .     
    dey                                                               ; 950c: 88          .     
    lda (l003a),y                                                     ; 950d: b1 3a       .:    
    sta l003a                                                         ; 950f: 85 3a       .:    
    stx l003b                                                         ; 9511: 86 3b       .;    
    iny                                                               ; 9513: c8          .     
    bpl loop_c9507                                                    ; 9514: 10 f1       ..    
; &9516 referenced 1 time by &9509
.c9516
    lda l0003                                                         ; 9516: a5 03       ..    
    sta (l003a),y                                                     ; 9518: 91 3a       .:    
    lda l0002                                                         ; 951a: a5 02       ..    
    dey                                                               ; 951c: 88          .     
    sta (l003a),y                                                     ; 951d: 91 3a       .:    
    tya                                                               ; 951f: 98          .     
    iny                                                               ; 9520: c8          .     
    sta (l0002),y                                                     ; 9521: 91 02       ..    
    cpy l0039                                                         ; 9523: c4 39       .9    
    beq return_8                                                      ; 9525: f0 31       .1    
; &9527 referenced 1 time by &952e
.loop_c9527
    iny                                                               ; 9527: c8          .     
    lda (l0037),y                                                     ; 9528: b1 37       .7    
    sta (l0002),y                                                     ; 952a: 91 02       ..    
    cpy l0039                                                         ; 952c: c4 39       .9    
    bne loop_c9527                                                    ; 952e: d0 f7       ..    
    rts                                                               ; 9530: 60          `     
; &9531 referenced 2 times by &8bdf, &957f
.sub_c9531
    lda #0                                                            ; 9531: a9 00       ..    
; &9533 referenced 1 time by &9537
.loop_c9533
    iny                                                               ; 9533: c8          .     
    sta (l0002),y                                                     ; 9534: 91 02       ..    
    dex                                                               ; 9536: ca          .     
    bne loop_c9533                                                    ; 9537: d0 fa       ..    
    sec                                                               ; 9539: 38          8     
    tya                                                               ; 953a: 98          .     
    adc l0002                                                         ; 953b: 65 02       e.    
    bcc c9541                                                         ; 953d: 90 02       ..    
    inc l0003                                                         ; 953f: e6 03       ..    
; &9541 referenced 1 time by &953d
.c9541
    ldy l0003                                                         ; 9541: a4 03       ..    
    cpy l0005                                                         ; 9543: c4 05       ..    
    bcc c9556                                                         ; 9545: 90 0f       ..    
    bne c954d                                                         ; 9547: d0 04       ..    
    cmp l0004                                                         ; 9549: c5 04       ..    
    bcc c9556                                                         ; 954b: 90 09       ..    
; &954d referenced 1 time by &9547
.c954d
    lda #0                                                            ; 954d: a9 00       ..    
    ldy #1                                                            ; 954f: a0 01       ..    
    sta (l003a),y                                                     ; 9551: 91 3a       .:    
    jmp c8cb7                                                         ; 9553: 4c b7 8c    L..   
; &9556 referenced 2 times by &9545, &954b
.c9556
    sta l0002                                                         ; 9556: 85 02       ..    
; &9558 referenced 1 time by &9525
.return_8
    rts                                                               ; 9558: 60          `     
    equb &a0, &01, &b1, &37, &c9, &30, &90, &18, &c9, &40, &b0, &0c   ; 9559: a0 01 b1... ......
    equb &c9, &3a, &b0, &10, &c0, &01, &f0, &0c, &e8, &c8, &d0, &ea   ; 9565: c9 3a b0... .:....
    equb &c9, &5f, &b0, &05, &c9, &5b, &90, &f4, &60, &c9, &7b, &90   ; 9571: c9 5f b0... ._....
    equb &ef, &60                                                     ; 957d: ef 60       .`    
; &957f referenced 2 times by &9590, &9593
.c957f
    jsr sub_c9531                                                     ; 957f: 20 31 95     1.   
; &9582 referenced 2 times by &85a5, &8be4
.sub_c9582
    jsr sub_c95c9                                                     ; 9582: 20 c9 95     ..   
    bne return_9                                                      ; 9585: d0 1d       ..    
    bcs return_9                                                      ; 9587: b0 1b       ..    
    jsr sub_c94fc                                                     ; 9589: 20 fc 94     ..   
    ldx #5                                                            ; 958c: a2 05       ..    
    cpx l002c                                                         ; 958e: e4 2c       .,    
    bne c957f                                                         ; 9590: d0 ed       ..    
    inx                                                               ; 9592: e8          .     
    bne c957f                                                         ; 9593: d0 ea       ..    
; &9595 referenced 1 time by &95df
.loop_c9595
    cmp #&21 ; '!'                                                    ; 9595: c9 21       .!    
    beq c95a5                                                         ; 9597: f0 0c       ..    
    cmp #&24 ; '$'                                                    ; 9599: c9 24       .$    
    beq c95b0                                                         ; 959b: f0 13       ..    
    eor #&3f ; '?'                                                    ; 959d: 49 3f       I?    
    beq c95a7                                                         ; 959f: f0 06       ..    
    lda #0                                                            ; 95a1: a9 00       ..    
    sec                                                               ; 95a3: 38          8     
; &95a4 referenced 2 times by &9585, &9587
.return_9
    rts                                                               ; 95a4: 60          `     
; &95a5 referenced 1 time by &9597
.c95a5
    lda #4                                                            ; 95a5: a9 04       ..    
; &95a7 referenced 1 time by &959f
.c95a7
    pha                                                               ; 95a7: 48          H     
    inc l001b                                                         ; 95a8: e6 1b       ..    
    jsr sub_c92e3                                                     ; 95aa: 20 e3 92     ..   
    jmp c969f                                                         ; 95ad: 4c 9f 96    L..   
; &95b0 referenced 1 time by &959b
.c95b0
    inc l001b                                                         ; 95b0: e6 1b       ..    
    jsr sub_c92e3                                                     ; 95b2: 20 e3 92     ..   
    lda l002b                                                         ; 95b5: a5 2b       .+    
    beq c95bf                                                         ; 95b7: f0 06       ..    
    lda #&80                                                          ; 95b9: a9 80       ..    
    sta l002c                                                         ; 95bb: 85 2c       .,    
    sec                                                               ; 95bd: 38          8     
    rts                                                               ; 95be: 60          `     
; &95bf referenced 1 time by &95b7
.c95bf
    brk                                                               ; 95bf: 00          .     
    equb &08                                                          ; 95c0: 08          .     
    equs "$ range"                                                    ; 95c1: 24 20 72... $ r...
    equb &00                                                          ; 95c8: 00          .     
; &95c9 referenced 1 time by &9582
.sub_c95c9
    lda l000b                                                         ; 95c9: a5 0b       ..    
    sta l0019                                                         ; 95cb: 85 19       ..    
    lda l000c                                                         ; 95cd: a5 0c       ..    
    sta l001a                                                         ; 95cf: 85 1a       ..    
    ldy l000a                                                         ; 95d1: a4 0a       ..    
    dey                                                               ; 95d3: 88          .     
; &95d4 referenced 1 time by &95db
.loop_c95d4
    iny                                                               ; 95d4: c8          .     
    sty l001b                                                         ; 95d5: 84 1b       ..    
    lda (l0019),y                                                     ; 95d7: b1 19       ..    
    cmp #&20 ; ' '                                                    ; 95d9: c9 20       .     
    beq loop_c95d4                                                    ; 95db: f0 f7       ..    
; &95dd referenced 2 times by &8bc9, &ae22
.sub_c95dd
    cmp #&40 ; '@'                                                    ; 95dd: c9 40       .@    
    bcc loop_c9595                                                    ; 95df: 90 b4       ..    
    cmp #&5b ; '['                                                    ; 95e1: c9 5b       .[    
    bcs c95ff                                                         ; 95e3: b0 1a       ..    
    asl a                                                             ; 95e5: 0a          .     
    asl a                                                             ; 95e6: 0a          .     
    sta l002a                                                         ; 95e7: 85 2a       .*    
    lda #4                                                            ; 95e9: a9 04       ..    
    sta l002b                                                         ; 95eb: 85 2b       .+    
    iny                                                               ; 95ed: c8          .     
    lda (l0019),y                                                     ; 95ee: b1 19       ..    
    iny                                                               ; 95f0: c8          .     
    cmp #&25 ; '%'                                                    ; 95f1: c9 25       .%    
    bne c95ff                                                         ; 95f3: d0 0a       ..    
    ldx #4                                                            ; 95f5: a2 04       ..    
    stx l002c                                                         ; 95f7: 86 2c       .,    
    lda (l0019),y                                                     ; 95f9: b1 19       ..    
    cmp #&28 ; '('                                                    ; 95fb: c9 28       .(    
    bne c9665                                                         ; 95fd: d0 66       .f    
; &95ff referenced 2 times by &95e3, &95f3
.c95ff
    ldx #5                                                            ; 95ff: a2 05       ..    
    stx l002c                                                         ; 9601: 86 2c       .,    
    lda l001b                                                         ; 9603: a5 1b       ..    
    clc                                                               ; 9605: 18          .     
    adc l0019                                                         ; 9606: 65 19       e.    
    ldx l001a                                                         ; 9608: a6 1a       ..    
    bcc c960e                                                         ; 960a: 90 02       ..    
    inx                                                               ; 960c: e8          .     
    clc                                                               ; 960d: 18          .     
; &960e referenced 1 time by &960a
.c960e
    sbc #0                                                            ; 960e: e9 00       ..    
    sta l0037                                                         ; 9610: 85 37       .7    
    bcs c9615                                                         ; 9612: b0 01       ..    
    dex                                                               ; 9614: ca          .     
; &9615 referenced 1 time by &9612
.c9615
    stx l0038                                                         ; 9615: 86 38       .8    
    ldx l001b                                                         ; 9617: a6 1b       ..    
    ldy #1                                                            ; 9619: a0 01       ..    
; &961b referenced 3 times by &962b, &9633, &963f
.c961b
    lda (l0037),y                                                     ; 961b: b1 37       .7    
    cmp #&41 ; 'A'                                                    ; 961d: c9 41       .A    
    bcs c962d                                                         ; 961f: b0 0c       ..    
    cmp #&30 ; '0'                                                    ; 9621: c9 30       .0    
    bcc c9641                                                         ; 9623: 90 1c       ..    
    cmp #&3a ; ':'                                                    ; 9625: c9 3a       .:    
    bcs c9641                                                         ; 9627: b0 18       ..    
    inx                                                               ; 9629: e8          .     
    iny                                                               ; 962a: c8          .     
    bne c961b                                                         ; 962b: d0 ee       ..    
; &962d referenced 1 time by &961f
.c962d
    cmp #&5b ; '['                                                    ; 962d: c9 5b       .[    
    bcs c9635                                                         ; 962f: b0 04       ..    
    inx                                                               ; 9631: e8          .     
    iny                                                               ; 9632: c8          .     
    bne c961b                                                         ; 9633: d0 e6       ..    
; &9635 referenced 1 time by &962f
.c9635
    cmp #&5f ; '_'                                                    ; 9635: c9 5f       ._    
    bcc c9641                                                         ; 9637: 90 08       ..    
    cmp #&7b ; '{'                                                    ; 9639: c9 7b       .{    
    bcs c9641                                                         ; 963b: b0 04       ..    
    inx                                                               ; 963d: e8          .     
    iny                                                               ; 963e: c8          .     
    bne c961b                                                         ; 963f: d0 da       ..    
; &9641 referenced 4 times by &9623, &9627, &9637, &963b
.c9641
    dey                                                               ; 9641: 88          .     
    beq c9673                                                         ; 9642: f0 2f       ./    
    cmp #&24 ; '$'                                                    ; 9644: c9 24       .$    
    beq c96af                                                         ; 9646: f0 67       .g    
    cmp #&25 ; '%'                                                    ; 9648: c9 25       .%    
    bne c9654                                                         ; 964a: d0 08       ..    
    dec l002c                                                         ; 964c: c6 2c       .,    
    iny                                                               ; 964e: c8          .     
    inx                                                               ; 964f: e8          .     
    iny                                                               ; 9650: c8          .     
    lda (l0037),y                                                     ; 9651: b1 37       .7    
    dey                                                               ; 9653: 88          .     
; &9654 referenced 1 time by &964a
.c9654
    sty l0039                                                         ; 9654: 84 39       .9    
    cmp #&28 ; '('                                                    ; 9656: c9 28       .(    
    beq c96a6                                                         ; 9658: f0 4c       .L    
    jsr sub_c9469                                                     ; 965a: 20 69 94     i.   
    beq c9677                                                         ; 965d: f0 18       ..    
    stx l001b                                                         ; 965f: 86 1b       ..    
; &9661 referenced 1 time by &96ac
.c9661
    ldy l001b                                                         ; 9661: a4 1b       ..    
    lda (l0019),y                                                     ; 9663: b1 19       ..    
; &9665 referenced 1 time by &95fd
.c9665
    cmp #&21 ; '!'                                                    ; 9665: c9 21       .!    
    beq c967f                                                         ; 9667: f0 16       ..    
    cmp #&3f ; '?'                                                    ; 9669: c9 3f       .?    
    beq c967b                                                         ; 966b: f0 0e       ..    
    clc                                                               ; 966d: 18          .     
    sty l001b                                                         ; 966e: 84 1b       ..    
    lda #&ff                                                          ; 9670: a9 ff       ..    
    rts                                                               ; 9672: 60          `     
; &9673 referenced 1 time by &9642
.c9673
    lda #0                                                            ; 9673: a9 00       ..    
    sec                                                               ; 9675: 38          8     
    rts                                                               ; 9676: 60          `     
; &9677 referenced 2 times by &965d, &96bf
.c9677
    lda #0                                                            ; 9677: a9 00       ..    
    clc                                                               ; 9679: 18          .     
    rts                                                               ; 967a: 60          `     
; &967b referenced 1 time by &966b
.c967b
    lda #0                                                            ; 967b: a9 00       ..    
    beq c9681                                                         ; 967d: f0 02       ..    
; &967f referenced 1 time by &9667
.c967f
    lda #4                                                            ; 967f: a9 04       ..    
; &9681 referenced 1 time by &967d
.c9681
    pha                                                               ; 9681: 48          H     
    iny                                                               ; 9682: c8          .     
    sty l001b                                                         ; 9683: 84 1b       ..    
    jsr cb32c                                                         ; 9685: 20 2c b3     ,.   
    jsr c92f0                                                         ; 9688: 20 f0 92     ..   
    lda l002b                                                         ; 968b: a5 2b       .+    
    pha                                                               ; 968d: 48          H     
    lda l002a                                                         ; 968e: a5 2a       .*    
    pha                                                               ; 9690: 48          H     
    jsr sub_c92e3                                                     ; 9691: 20 e3 92     ..   
    clc                                                               ; 9694: 18          .     
    pla                                                               ; 9695: 68          h     
    adc l002a                                                         ; 9696: 65 2a       e*    
    sta l002a                                                         ; 9698: 85 2a       .*    
    pla                                                               ; 969a: 68          h     
    adc l002b                                                         ; 969b: 65 2b       e+    
    sta l002b                                                         ; 969d: 85 2b       .+    
; &969f referenced 1 time by &95ad
.c969f
    pla                                                               ; 969f: 68          h     
    sta l002c                                                         ; 96a0: 85 2c       .,    
    clc                                                               ; 96a2: 18          .     
    lda #&ff                                                          ; 96a3: a9 ff       ..    
    rts                                                               ; 96a5: 60          `     
; &96a6 referenced 1 time by &9658
.c96a6
    inx                                                               ; 96a6: e8          .     
    inc l0039                                                         ; 96a7: e6 39       .9    
    jsr sub_c96df                                                     ; 96a9: 20 df 96     ..   
    jmp c9661                                                         ; 96ac: 4c 61 96    La.   
; &96af referenced 1 time by &9646
.c96af
    inx                                                               ; 96af: e8          .     
    iny                                                               ; 96b0: c8          .     
    sty l0039                                                         ; 96b1: 84 39       .9    
    iny                                                               ; 96b3: c8          .     
    dec l002c                                                         ; 96b4: c6 2c       .,    
    lda (l0037),y                                                     ; 96b6: b1 37       .7    
    cmp #&28 ; '('                                                    ; 96b8: c9 28       .(    
    beq c96c9                                                         ; 96ba: f0 0d       ..    
    jsr sub_c9469                                                     ; 96bc: 20 69 94     i.   
    beq c9677                                                         ; 96bf: f0 b6       ..    
    stx l001b                                                         ; 96c1: 86 1b       ..    
    lda #&81                                                          ; 96c3: a9 81       ..    
    sta l002c                                                         ; 96c5: 85 2c       .,    
    sec                                                               ; 96c7: 38          8     
    rts                                                               ; 96c8: 60          `     
; &96c9 referenced 1 time by &96ba
.c96c9
    inx                                                               ; 96c9: e8          .     
    sty l0039                                                         ; 96ca: 84 39       .9    
    dec l002c                                                         ; 96cc: c6 2c       .,    
    jsr sub_c96df                                                     ; 96ce: 20 df 96     ..   
    lda #&81                                                          ; 96d1: a9 81       ..    
    sta l002c                                                         ; 96d3: 85 2c       .,    
    sec                                                               ; 96d5: 38          8     
    rts                                                               ; 96d6: 60          `     
; &96d7 referenced 2 times by &96e2, &9709
.c96d7
    brk                                                               ; 96d7: 00          .     
    equb &0e                                                          ; 96d8: 0e          .     
    equs "Array"                                                      ; 96d9: 41 72 72... Arr...
    equb &00                                                          ; 96de: 00          .     
; &96df referenced 2 times by &96a9, &96ce
.sub_c96df
    jsr sub_c9469                                                     ; 96df: 20 69 94     i.   
    beq c96d7                                                         ; 96e2: f0 f3       ..    
    stx l001b                                                         ; 96e4: 86 1b       ..    
    lda l002c                                                         ; 96e6: a5 2c       .,    
    pha                                                               ; 96e8: 48          H     
    lda l002a                                                         ; 96e9: a5 2a       .*    
    pha                                                               ; 96eb: 48          H     
    lda l002b                                                         ; 96ec: a5 2b       .+    
    pha                                                               ; 96ee: 48          H     
    ldy #0                                                            ; 96ef: a0 00       ..    
    lda (l002a),y                                                     ; 96f1: b1 2a       .*    
    cmp #4                                                            ; 96f3: c9 04       ..    
    bcc c976c                                                         ; 96f5: 90 75       .u    
    tya                                                               ; 96f7: 98          .     
    jsr sub_caed8                                                     ; 96f8: 20 d8 ae     ..   
    lda #1                                                            ; 96fb: a9 01       ..    
    sta l002d                                                         ; 96fd: 85 2d       .-    
; &96ff referenced 1 time by &9742
.loop_c96ff
    jsr sub_cbd94                                                     ; 96ff: 20 94 bd     ..   
    jsr sub_c92dd                                                     ; 9702: 20 dd 92     ..   
    inc l001b                                                         ; 9705: e6 1b       ..    
    cpx #&2c ; ','                                                    ; 9707: e0 2c       .,    
    bne c96d7                                                         ; 9709: d0 cc       ..    
    ldx #&39 ; '9'                                                    ; 970b: a2 39       .9    
    jsr sub_cbe0d                                                     ; 970d: 20 0d be     ..   
    ldy l003c                                                         ; 9710: a4 3c       .<    
    pla                                                               ; 9712: 68          h     
    sta l0038                                                         ; 9713: 85 38       .8    
    pla                                                               ; 9715: 68          h     
    sta l0037                                                         ; 9716: 85 37       .7    
    pha                                                               ; 9718: 48          H     
    lda l0038                                                         ; 9719: a5 38       .8    
    pha                                                               ; 971b: 48          H     
    jsr sub_c97ba                                                     ; 971c: 20 ba 97     ..   
    sty l002d                                                         ; 971f: 84 2d       .-    
    lda (l0037),y                                                     ; 9721: b1 37       .7    
    sta l003f                                                         ; 9723: 85 3f       .?    
    iny                                                               ; 9725: c8          .     
    lda (l0037),y                                                     ; 9726: b1 37       .7    
    sta l0040                                                         ; 9728: 85 40       .@    
    lda l002a                                                         ; 972a: a5 2a       .*    
    adc l0039                                                         ; 972c: 65 39       e9    
    sta l002a                                                         ; 972e: 85 2a       .*    
    lda l002b                                                         ; 9730: a5 2b       .+    
    adc l003a                                                         ; 9732: 65 3a       e:    
    sta l002b                                                         ; 9734: 85 2b       .+    
    jsr sub_c9236                                                     ; 9736: 20 36 92     6.   
    ldy #0                                                            ; 9739: a0 00       ..    
    sec                                                               ; 973b: 38          8     
    lda (l0037),y                                                     ; 973c: b1 37       .7    
    sbc l002d                                                         ; 973e: e5 2d       .-    
    cmp #3                                                            ; 9740: c9 03       ..    
    bcs loop_c96ff                                                    ; 9742: b0 bb       ..    
    jsr sub_cbd94                                                     ; 9744: 20 94 bd     ..   
    jsr cae56                                                         ; 9747: 20 56 ae     V.   
    jsr c92f0                                                         ; 974a: 20 f0 92     ..   
    pla                                                               ; 974d: 68          h     
    sta l0038                                                         ; 974e: 85 38       .8    
    pla                                                               ; 9750: 68          h     
    sta l0037                                                         ; 9751: 85 37       .7    
    ldx #&39 ; '9'                                                    ; 9753: a2 39       .9    
    jsr sub_cbe0d                                                     ; 9755: 20 0d be     ..   
    ldy l003c                                                         ; 9758: a4 3c       .<    
    jsr sub_c97ba                                                     ; 975a: 20 ba 97     ..   
    clc                                                               ; 975d: 18          .     
    lda l0039                                                         ; 975e: a5 39       .9    
    adc l002a                                                         ; 9760: 65 2a       e*    
    sta l002a                                                         ; 9762: 85 2a       .*    
    lda l003a                                                         ; 9764: a5 3a       .:    
    adc l002b                                                         ; 9766: 65 2b       e+    
    sta l002b                                                         ; 9768: 85 2b       .+    
    bcc c977d                                                         ; 976a: 90 11       ..    
; &976c referenced 1 time by &96f5
.c976c
    jsr cae56                                                         ; 976c: 20 56 ae     V.   
    jsr c92f0                                                         ; 976f: 20 f0 92     ..   
    pla                                                               ; 9772: 68          h     
    sta l0038                                                         ; 9773: 85 38       .8    
    pla                                                               ; 9775: 68          h     
    sta l0037                                                         ; 9776: 85 37       .7    
    ldy #1                                                            ; 9778: a0 01       ..    
    jsr sub_c97ba                                                     ; 977a: 20 ba 97     ..   
; &977d referenced 1 time by &976a
.c977d
    pla                                                               ; 977d: 68          h     
    sta l002c                                                         ; 977e: 85 2c       .,    
    cmp #5                                                            ; 9780: c9 05       ..    
    bne c979b                                                         ; 9782: d0 17       ..    
    ldx l002b                                                         ; 9784: a6 2b       .+    
    lda l002a                                                         ; 9786: a5 2a       .*    
    asl l002a                                                         ; 9788: 06 2a       .*    
    rol l002b                                                         ; 978a: 26 2b       &+    
    asl l002a                                                         ; 978c: 06 2a       .*    
    rol l002b                                                         ; 978e: 26 2b       &+    
    adc l002a                                                         ; 9790: 65 2a       e*    
    sta l002a                                                         ; 9792: 85 2a       .*    
    txa                                                               ; 9794: 8a          .     
    adc l002b                                                         ; 9795: 65 2b       e+    
    sta l002b                                                         ; 9797: 85 2b       .+    
    bcc c97a3                                                         ; 9799: 90 08       ..    
; &979b referenced 1 time by &9782
.c979b
    asl l002a                                                         ; 979b: 06 2a       .*    
    rol l002b                                                         ; 979d: 26 2b       &+    
    asl l002a                                                         ; 979f: 06 2a       .*    
    rol l002b                                                         ; 97a1: 26 2b       &+    
; &97a3 referenced 1 time by &9799
.c97a3
    tya                                                               ; 97a3: 98          .     
    adc l002a                                                         ; 97a4: 65 2a       e*    
    sta l002a                                                         ; 97a6: 85 2a       .*    
    bcc c97ad                                                         ; 97a8: 90 03       ..    
    inc l002b                                                         ; 97aa: e6 2b       .+    
    clc                                                               ; 97ac: 18          .     
; &97ad referenced 1 time by &97a8
.c97ad
    lda l0037                                                         ; 97ad: a5 37       .7    
    adc l002a                                                         ; 97af: 65 2a       e*    
    sta l002a                                                         ; 97b1: 85 2a       .*    
    lda l0038                                                         ; 97b3: a5 38       .8    
    adc l002b                                                         ; 97b5: 65 2b       e+    
    sta l002b                                                         ; 97b7: 85 2b       .+    
    rts                                                               ; 97b9: 60          `     
; &97ba referenced 3 times by &971c, &975a, &977a
.sub_c97ba
    lda l002b                                                         ; 97ba: a5 2b       .+    
    and #&c0                                                          ; 97bc: 29 c0       ).    
    ora l002c                                                         ; 97be: 05 2c       .,    
    ora l002d                                                         ; 97c0: 05 2d       .-    
    bne c97d1                                                         ; 97c2: d0 0d       ..    
    lda l002a                                                         ; 97c4: a5 2a       .*    
    cmp (l0037),y                                                     ; 97c6: d1 37       .7    
    iny                                                               ; 97c8: c8          .     
    lda l002b                                                         ; 97c9: a5 2b       .+    
    sbc (l0037),y                                                     ; 97cb: f1 37       .7    
    bcs c97d1                                                         ; 97cd: b0 02       ..    
    iny                                                               ; 97cf: c8          .     
    rts                                                               ; 97d0: 60          `     
; &97d1 referenced 2 times by &97c2, &97cd
.c97d1
    brk                                                               ; 97d1: 00          .     
    equb &0f                                                          ; 97d2: 0f          .     
    equs "Subscript"                                                  ; 97d3: 53 75 62... Sub...
    equb &00                                                          ; 97dc: 00          .     
; &97dd referenced 1 time by &97e5
.loop_c97dd
    inc l000a                                                         ; 97dd: e6 0a       ..    
; &97df referenced 1 time by &8b2d
.sub_c97df
    ldy l000a                                                         ; 97df: a4 0a       ..    
    lda (l000b),y                                                     ; 97e1: b1 0b       ..    
    cmp #&20 ; ' '                                                    ; 97e3: c9 20       .     
    beq loop_c97dd                                                    ; 97e5: f0 f6       ..    
    cmp #&8d                                                          ; 97e7: c9 8d       ..    
    bne c9805                                                         ; 97e9: d0 1a       ..    
    iny                                                               ; 97eb: c8          .     
    lda (l000b),y                                                     ; 97ec: b1 0b       ..    
    asl a                                                             ; 97ee: 0a          .     
    asl a                                                             ; 97ef: 0a          .     
    tax                                                               ; 97f0: aa          .     
    and #&c0                                                          ; 97f1: 29 c0       ).    
    iny                                                               ; 97f3: c8          .     
    eor (l000b),y                                                     ; 97f4: 51 0b       Q.    
    sta l002a                                                         ; 97f6: 85 2a       .*    
    txa                                                               ; 97f8: 8a          .     
    asl a                                                             ; 97f9: 0a          .     
    asl a                                                             ; 97fa: 0a          .     
    iny                                                               ; 97fb: c8          .     
    eor (l000b),y                                                     ; 97fc: 51 0b       Q.    
    sta l002b                                                         ; 97fe: 85 2b       .+    
    iny                                                               ; 9800: c8          .     
    sty l000a                                                         ; 9801: 84 0a       ..    
    sec                                                               ; 9803: 38          8     
    rts                                                               ; 9804: 60          `     
; &9805 referenced 1 time by &97e9
.c9805
    clc                                                               ; 9805: 18          .     
    rts                                                               ; 9806: 60          `     
    equb &a5, &0b, &85, &19, &a5, &0c, &85, &1a, &a5, &0a, &85, &1b   ; 9807: a5 0b 85... ......
; &9813 referenced 3 times by &8bee, &8bfe, &981b
.c9813
    ldy l001b                                                         ; 9813: a4 1b       ..    
    inc l001b                                                         ; 9815: e6 1b       ..    
    lda (l0019),y                                                     ; 9817: b1 19       ..    
    cmp #&20 ; ' '                                                    ; 9819: c9 20       .     
    beq c9813                                                         ; 981b: f0 f6       ..    
    cmp #&3d ; '='                                                    ; 981d: c9 3d       .=    
    beq c9849                                                         ; 981f: f0 28       .(    
; &9821 referenced 1 time by &9846
.loop_c9821
    brk                                                               ; 9821: 00          .     
    equb &04                                                          ; 9822: 04          .     
    equs "Mistake"                                                    ; 9823: 4d 69 73... Mis...
; &982a referenced 4 times by &8604, &8855, &8c0b, &986b
.c982a
    brk                                                               ; 982a: 00          .     
    equb &10                                                          ; 982b: 10          .     
    equs "Syntax error"                                               ; 982c: 53 79 6e... Syn...
; &9838 referenced 2 times by &987d, &bc22
.c9838
    brk                                                               ; 9838: 00          .     
    equb &11                                                          ; 9839: 11          .     
    equs "Escape"                                                     ; 983a: 45 73 63... Esc...
    equb &00                                                          ; 9840: 00          .     
; &9841 referenced 1 time by &8bd2
.sub_c9841
    jsr c8a8c                                                         ; 9841: 20 8c 8a     ..   
    cmp #&3d ; '='                                                    ; 9844: c9 3d       .=    
    bne loop_c9821                                                    ; 9846: d0 d9       ..    
    rts                                                               ; 9848: 60          `     
; &9849 referenced 1 time by &981f
.c9849
    jsr sub_c9b29                                                     ; 9849: 20 29 9b     ).   
; &984c referenced 1 time by &8b56
.c984c
    txa                                                               ; 984c: 8a          .     
    ldy l001b                                                         ; 984d: a4 1b       ..    
    jmp c9861                                                         ; 984f: 4c 61 98    La.   
    equb &a4, &1b, &4c, &59, &98                                      ; 9852: a4 1b 4c... ..L...
; &9857 referenced 1 time by &8b98
.sub_c9857
    ldy l000a                                                         ; 9857: a4 0a       ..    
; &9859 referenced 1 time by &858c
.sub_c9859
    dey                                                               ; 9859: 88          .     
; &985a referenced 1 time by &985f
.loop_c985a
    iny                                                               ; 985a: c8          .     
    lda (l000b),y                                                     ; 985b: b1 0b       ..    
    cmp #&20 ; ' '                                                    ; 985d: c9 20       .     
    beq loop_c985a                                                    ; 985f: f0 f9       ..    
; &9861 referenced 1 time by &984f
.c9861
    cmp #&3a ; ':'                                                    ; 9861: c9 3a       .:    
    beq c986d                                                         ; 9863: f0 08       ..    
    cmp #&0d                                                          ; 9865: c9 0d       ..    
    beq c986d                                                         ; 9867: f0 04       ..    
    cmp #&8b                                                          ; 9869: c9 8b       ..    
    bne c982a                                                         ; 986b: d0 bd       ..    
; &986d referenced 4 times by &850f, &8b73, &9863, &9867
.c986d
    clc                                                               ; 986d: 18          .     
    tya                                                               ; 986e: 98          .     
    adc l000b                                                         ; 986f: 65 0b       e.    
    sta l000b                                                         ; 9871: 85 0b       ..    
    bcc c9877                                                         ; 9873: 90 02       ..    
    inc l000c                                                         ; 9875: e6 0c       ..    
; &9877 referenced 1 time by &9873
.c9877
    ldy #1                                                            ; 9877: a0 01       ..    
    sty l000a                                                         ; 9879: 84 0a       ..    
    bit l00ff                                                         ; 987b: 24 ff       $.    
    bmi c9838                                                         ; 987d: 30 b9       0.    
    rts                                                               ; 987f: 60          `     
    equb &20, &57, &98, &88, &b1, &0b, &c9, &3a, &f0, &f5, &a5, &0c   ; 9880: 20 57 98...  W....
    equb &c9, &07, &f0, &2c                                           ; 988c: c9 07 f0... ......
; &9890 referenced 2 times by &859f, &8b91
.sub_c9890
    iny                                                               ; 9890: c8          .     
    lda (l000b),y                                                     ; 9891: b1 0b       ..    
    bmi c98bc                                                         ; 9893: 30 27       0'    
    lda l0020                                                         ; 9895: a5 20       .     
    beq c98ac                                                         ; 9897: f0 13       ..    
    tya                                                               ; 9899: 98          .     
    pha                                                               ; 989a: 48          H     
    iny                                                               ; 989b: c8          .     
    lda (l000b),y                                                     ; 989c: b1 0b       ..    
    pha                                                               ; 989e: 48          H     
    dey                                                               ; 989f: 88          .     
    lda (l000b),y                                                     ; 98a0: b1 0b       ..    
    tay                                                               ; 98a2: a8          .     
    pla                                                               ; 98a3: 68          h     
    jsr caeea                                                         ; 98a4: 20 ea ae     ..   
    jsr sub_c9905                                                     ; 98a7: 20 05 99     ..   
    pla                                                               ; 98aa: 68          h     
    tay                                                               ; 98ab: a8          .     
; &98ac referenced 1 time by &9897
.c98ac
    iny                                                               ; 98ac: c8          .     
    sec                                                               ; 98ad: 38          8     
    tya                                                               ; 98ae: 98          .     
    adc l000b                                                         ; 98af: 65 0b       e.    
    sta l000b                                                         ; 98b1: 85 0b       ..    
    bcc c98b7                                                         ; 98b3: 90 02       ..    
    inc l000c                                                         ; 98b5: e6 0c       ..    
; &98b7 referenced 1 time by &98b3
.c98b7
    ldy #1                                                            ; 98b7: a0 01       ..    
    sty l000a                                                         ; 98b9: 84 0a       ..    
; &98bb referenced 1 time by &990d
.return_10
    rts                                                               ; 98bb: 60          `     
; &98bc referenced 1 time by &9893
.c98bc
    jmp c8af6                                                         ; 98bc: 4c f6 8a    L..   
    equb &4c, &0e, &8c, &20, &1d, &9b, &f0, &f8, &10, &03, &20, &e4   ; 98bf: 4c 0e 8c... L.....
    equb &a3, &a4, &1b, &84, &0a, &a5, &2a, &05, &2b, &05, &2c, &05   ; 98cb: a3 a4 1b... ......
    equb &2d, &f0, &17, &e0, &8c, &f0, &03, &4c, &a3, &8b, &e6, &0a   ; 98d7: 2d f0 17... -.....
    equb &20, &df, &97, &90, &f6, &20, &af, &b9, &20, &77, &98, &4c   ; 98e3: 20 df 97...  .....
    equb &d2, &b8, &a4, &0a, &b1, &0b, &c9, &0d, &f0, &09, &c8, &c9   ; 98ef: d2 b8 a4... ......
    equb &8b, &d0, &f5, &84, &0a, &f0, &e1, &4c, &87, &8b             ; 98fb: 8b d0 f5... ......
; &9905 referenced 1 time by &98a7
.sub_c9905
    lda l002a                                                         ; 9905: a5 2a       .*    
    cmp l0021                                                         ; 9907: c5 21       .!    
    lda l002b                                                         ; 9909: a5 2b       .+    
    sbc l0022                                                         ; 990b: e5 22       ."    
    bcs return_10                                                     ; 990d: b0 ac       ..    
    lda #&5b ; '['                                                    ; 990f: a9 5b       .[    
    jsr cb558                                                         ; 9911: 20 58 b5     X.   
    jsr sub_c991f                                                     ; 9914: 20 1f 99     ..   
    lda #&5d ; ']'                                                    ; 9917: a9 5d       .]    
    jsr cb558                                                         ; 9919: 20 58 b5     X.   
    jmp cb565                                                         ; 991c: 4c 65 b5    Le.   
; &991f referenced 1 time by &9914
.sub_c991f
    lda #0                                                            ; 991f: a9 00       ..    
    beq c9925                                                         ; 9921: f0 02       ..    
    lda #5                                                            ; 9923: a9 05       ..    
; &9925 referenced 1 time by &9921
.c9925
    sta l0014                                                         ; 9925: 85 14       ..    
    ldx #4                                                            ; 9927: a2 04       ..    
; &9929 referenced 1 time by &9944
.loop_c9929
    lda #0                                                            ; 9929: a9 00       ..    
    sta l003f,x                                                       ; 992b: 95 3f       .?    
    sec                                                               ; 992d: 38          8     
; &992e referenced 1 time by &9941
.loop_c992e
    lda l002a                                                         ; 992e: a5 2a       .*    
    sbc l996b,x                                                       ; 9930: fd 6b 99    .k.   
    tay                                                               ; 9933: a8          .     
    lda l002b                                                         ; 9934: a5 2b       .+    
    sbc l99b9,x                                                       ; 9936: fd b9 99    ...   
    bcc c9943                                                         ; 9939: 90 08       ..    
    sta l002b                                                         ; 993b: 85 2b       .+    
    sty l002a                                                         ; 993d: 84 2a       .*    
    inc l003f,x                                                       ; 993f: f6 3f       .?    
    bne loop_c992e                                                    ; 9941: d0 eb       ..    
; &9943 referenced 1 time by &9939
.c9943
    dex                                                               ; 9943: ca          .     
    bpl loop_c9929                                                    ; 9944: 10 e3       ..    
    ldx #5                                                            ; 9946: a2 05       ..    
; &9948 referenced 1 time by &994d
.loop_c9948
    dex                                                               ; 9948: ca          .     
    beq c994f                                                         ; 9949: f0 04       ..    
    lda l003f,x                                                       ; 994b: b5 3f       .?    
    beq loop_c9948                                                    ; 994d: f0 f9       ..    
; &994f referenced 1 time by &9949
.c994f
    stx l0037                                                         ; 994f: 86 37       .7    
    lda l0014                                                         ; 9951: a5 14       ..    
    beq c9960                                                         ; 9953: f0 0b       ..    
    sbc l0037                                                         ; 9955: e5 37       .7    
    beq c9960                                                         ; 9957: f0 07       ..    
    tay                                                               ; 9959: a8          .     
; &995a referenced 1 time by &995e
.loop_c995a
    jsr cb565                                                         ; 995a: 20 65 b5     e.   
    dey                                                               ; 995d: 88          .     
    bne loop_c995a                                                    ; 995e: d0 fa       ..    
; &9960 referenced 3 times by &9953, &9957, &9968
.c9960
    lda l003f,x                                                       ; 9960: b5 3f       .?    
    ora #&30 ; '0'                                                    ; 9962: 09 30       .0    
    jsr cb558                                                         ; 9964: 20 58 b5     X.   
    dex                                                               ; 9967: ca          .     
    bpl c9960                                                         ; 9968: 10 f6       ..    
    rts                                                               ; 996a: 60          `     
; &996b referenced 1 time by &9930
.l996b
    equb &01, &0a, &64, &e8, &10                                      ; 996b: 01 0a 64... ..d...
; &9970 referenced 1 time by &bc2d
.sub_c9970
    ldy #0                                                            ; 9970: a0 00       ..    
    sty l003d                                                         ; 9972: 84 3d       .=    
    lda l0018                                                         ; 9974: a5 18       ..    
    sta l003e                                                         ; 9976: 85 3e       .>    
; &9978 referenced 2 times by &9988, &998c
.c9978
    ldy #1                                                            ; 9978: a0 01       ..    
    lda (l003d),y                                                     ; 997a: b1 3d       .=    
    cmp l002b                                                         ; 997c: c5 2b       .+    
    bcs c998e                                                         ; 997e: b0 0e       ..    
; &9980 referenced 1 time by &9996
.loop_c9980
    ldy #3                                                            ; 9980: a0 03       ..    
    lda (l003d),y                                                     ; 9982: b1 3d       .=    
    adc l003d                                                         ; 9984: 65 3d       e=    
    sta l003d                                                         ; 9986: 85 3d       .=    
    bcc c9978                                                         ; 9988: 90 ee       ..    
    inc l003e                                                         ; 998a: e6 3e       .>    
    bcs c9978                                                         ; 998c: b0 ea       ..    
; &998e referenced 1 time by &997e
.c998e
    bne c99a4                                                         ; 998e: d0 14       ..    
    ldy #2                                                            ; 9990: a0 02       ..    
    lda (l003d),y                                                     ; 9992: b1 3d       .=    
    cmp l002a                                                         ; 9994: c5 2a       .*    
    bcc loop_c9980                                                    ; 9996: 90 e8       ..    
    bne c99a4                                                         ; 9998: d0 0a       ..    
    tya                                                               ; 999a: 98          .     
    adc l003d                                                         ; 999b: 65 3d       e=    
    sta l003d                                                         ; 999d: 85 3d       .=    
    bcc c99a4                                                         ; 999f: 90 03       ..    
    inc l003e                                                         ; 99a1: e6 3e       .>    
    clc                                                               ; 99a3: 18          .     
; &99a4 referenced 3 times by &998e, &9998, &999f
.c99a4
    ldy #2                                                            ; 99a4: a0 02       ..    
    rts                                                               ; 99a6: 60          `     
; &99a7 referenced 2 times by &99f0, &a6bb
.c99a7
    brk                                                               ; 99a7: 00          .     
    equb &12                                                          ; 99a8: 12          .     
    equs "Division by zero"                                           ; 99a9: 44 69 76... Div...
; &99b9 referenced 1 time by &9936
.l99b9
    equb &00, &00, &00, &03, &27                                      ; 99b9: 00 00 00... ......
; &99be referenced 2 times by &9e01, &9e0a
.sub_c99be
    tay                                                               ; 99be: a8          .     
    jsr c92f0                                                         ; 99bf: 20 f0 92     ..   
    lda l002d                                                         ; 99c2: a5 2d       .-    
    pha                                                               ; 99c4: 48          H     
    jsr sub_cad71                                                     ; 99c5: 20 71 ad     q.   
    jsr sub_c9e1d                                                     ; 99c8: 20 1d 9e     ..   
    stx l0027                                                         ; 99cb: 86 27       .'    
    tay                                                               ; 99cd: a8          .     
    jsr c92f0                                                         ; 99ce: 20 f0 92     ..   
    pla                                                               ; 99d1: 68          h     
    sta l0038                                                         ; 99d2: 85 38       .8    
    eor l002d                                                         ; 99d4: 45 2d       E-    
    sta l0037                                                         ; 99d6: 85 37       .7    
    jsr sub_cad71                                                     ; 99d8: 20 71 ad     q.   
    ldx #&39 ; '9'                                                    ; 99db: a2 39       .9    
    jsr sub_cbe0d                                                     ; 99dd: 20 0d be     ..   
    sty l003d                                                         ; 99e0: 84 3d       .=    
    sty l003e                                                         ; 99e2: 84 3e       .>    
    sty l003f                                                         ; 99e4: 84 3f       .?    
    sty l0040                                                         ; 99e6: 84 40       .@    
    lda l002d                                                         ; 99e8: a5 2d       .-    
    ora l002a                                                         ; 99ea: 05 2a       .*    
    ora l002b                                                         ; 99ec: 05 2b       .+    
    ora l002c                                                         ; 99ee: 05 2c       .,    
    beq c99a7                                                         ; 99f0: f0 b5       ..    
    ldy #&20 ; ' '                                                    ; 99f2: a0 20       .     
; &99f4 referenced 1 time by &99ff
.loop_c99f4
    dey                                                               ; 99f4: 88          .     
    beq return_11                                                     ; 99f5: f0 41       .A    
    asl l0039                                                         ; 99f7: 06 39       .9    
    rol l003a                                                         ; 99f9: 26 3a       &:    
    rol l003b                                                         ; 99fb: 26 3b       &;    
    rol l003c                                                         ; 99fd: 26 3c       &<    
    bpl loop_c99f4                                                    ; 99ff: 10 f3       ..    
; &9a01 referenced 1 time by &9a36
.loop_c9a01
    rol l0039                                                         ; 9a01: 26 39       &9    
    rol l003a                                                         ; 9a03: 26 3a       &:    
    rol l003b                                                         ; 9a05: 26 3b       &;    
    rol l003c                                                         ; 9a07: 26 3c       &<    
    rol l003d                                                         ; 9a09: 26 3d       &=    
    rol l003e                                                         ; 9a0b: 26 3e       &>    
    rol l003f                                                         ; 9a0d: 26 3f       &?    
    rol l0040                                                         ; 9a0f: 26 40       &@    
    sec                                                               ; 9a11: 38          8     
    lda l003d                                                         ; 9a12: a5 3d       .=    
    sbc l002a                                                         ; 9a14: e5 2a       .*    
    pha                                                               ; 9a16: 48          H     
    lda l003e                                                         ; 9a17: a5 3e       .>    
    sbc l002b                                                         ; 9a19: e5 2b       .+    
    pha                                                               ; 9a1b: 48          H     
    lda l003f                                                         ; 9a1c: a5 3f       .?    
    sbc l002c                                                         ; 9a1e: e5 2c       .,    
    tax                                                               ; 9a20: aa          .     
    lda l0040                                                         ; 9a21: a5 40       .@    
    sbc l002d                                                         ; 9a23: e5 2d       .-    
    bcc c9a33                                                         ; 9a25: 90 0c       ..    
    sta l0040                                                         ; 9a27: 85 40       .@    
    stx l003f                                                         ; 9a29: 86 3f       .?    
    pla                                                               ; 9a2b: 68          h     
    sta l003e                                                         ; 9a2c: 85 3e       .>    
    pla                                                               ; 9a2e: 68          h     
    sta l003d                                                         ; 9a2f: 85 3d       .=    
    bcs c9a35                                                         ; 9a31: b0 02       ..    
; &9a33 referenced 1 time by &9a25
.c9a33
    pla                                                               ; 9a33: 68          h     
    pla                                                               ; 9a34: 68          h     
; &9a35 referenced 1 time by &9a31
.c9a35
    dey                                                               ; 9a35: 88          .     
    bne loop_c9a01                                                    ; 9a36: d0 c9       ..    
; &9a38 referenced 1 time by &99f5
.return_11
    rts                                                               ; 9a38: 60          `     
; &9a39 referenced 1 time by &9aab
.loop_c9a39
    stx l0027                                                         ; 9a39: 86 27       .'    
    jsr sub_cbdea                                                     ; 9a3b: 20 ea bd     ..   
    jsr sub_cbd51                                                     ; 9a3e: 20 51 bd     Q.   
    jsr ca2be                                                         ; 9a41: 20 be a2     ..   
    jsr sub_ca21e                                                     ; 9a44: 20 1e a2     ..   
    jsr sub_cbd7e                                                     ; 9a47: 20 7e bd     ~.   
    jsr sub_ca3b5                                                     ; 9a4a: 20 b5 a3     ..   
    jmp c9a62                                                         ; 9a4d: 4c 62 9a    Lb.   
; &9a50 referenced 1 time by &9aa0
.loop_c9a50
    jsr sub_cbd51                                                     ; 9a50: 20 51 bd     Q.   
    jsr sub_c9c42                                                     ; 9a53: 20 42 9c     B.   
    stx l0027                                                         ; 9a56: 86 27       .'    
    tay                                                               ; 9a58: a8          .     
    jsr sub_c92fd                                                     ; 9a59: 20 fd 92     ..   
    jsr sub_cbd7e                                                     ; 9a5c: 20 7e bd     ~.   
    jsr sub_ca34e                                                     ; 9a5f: 20 4e a3     N.   
; &9a62 referenced 1 time by &9a4d
.c9a62
    ldx l0027                                                         ; 9a62: a6 27       .'    
    ldy #0                                                            ; 9a64: a0 00       ..    
    lda l003b                                                         ; 9a66: a5 3b       .;    
    and #&80                                                          ; 9a68: 29 80       ).    
    sta l003b                                                         ; 9a6a: 85 3b       .;    
    lda l002e                                                         ; 9a6c: a5 2e       ..    
    and #&80                                                          ; 9a6e: 29 80       ).    
    cmp l003b                                                         ; 9a70: c5 3b       .;    
    bne return_12                                                     ; 9a72: d0 1e       ..    
    lda l003d                                                         ; 9a74: a5 3d       .=    
    cmp l0030                                                         ; 9a76: c5 30       .0    
    bne c9a93                                                         ; 9a78: d0 19       ..    
    lda l003e                                                         ; 9a7a: a5 3e       .>    
    cmp l0031                                                         ; 9a7c: c5 31       .1    
    bne c9a93                                                         ; 9a7e: d0 13       ..    
    lda l003f                                                         ; 9a80: a5 3f       .?    
    cmp l0032                                                         ; 9a82: c5 32       .2    
    bne c9a93                                                         ; 9a84: d0 0d       ..    
    lda l0040                                                         ; 9a86: a5 40       .@    
    cmp l0033                                                         ; 9a88: c5 33       .3    
    bne c9a93                                                         ; 9a8a: d0 07       ..    
    lda l0041                                                         ; 9a8c: a5 41       .A    
    cmp l0034                                                         ; 9a8e: c5 34       .4    
    bne c9a93                                                         ; 9a90: d0 01       ..    
; &9a92 referenced 1 time by &9a72
.return_12
    rts                                                               ; 9a92: 60          `     
; &9a93 referenced 5 times by &9a78, &9a7e, &9a84, &9a8a, &9a90
.c9a93
    ror a                                                             ; 9a93: 6a          j     
    eor l003b                                                         ; 9a94: 45 3b       E;    
    rol a                                                             ; 9a96: 2a          *     
    lda #1                                                            ; 9a97: a9 01       ..    
    rts                                                               ; 9a99: 60          `     
; &9a9a referenced 2 times by &9aa9, &9aee
.c9a9a
    jmp c8c0e                                                         ; 9a9a: 4c 0e 8c    L..   
; &9a9d referenced 5 times by &9bcd, &9bd6, &9be1, &9bf1, &9bfc
.sub_c9a9d
    txa                                                               ; 9a9d: 8a          .     
; &9a9e referenced 1 time by &9baf
.sub_c9a9e
    beq c9ae7                                                         ; 9a9e: f0 47       .G    
    bmi loop_c9a50                                                    ; 9aa0: 30 ae       0.    
    jsr sub_cbd94                                                     ; 9aa2: 20 94 bd     ..   
    jsr sub_c9c42                                                     ; 9aa5: 20 42 9c     B.   
    tay                                                               ; 9aa8: a8          .     
    beq c9a9a                                                         ; 9aa9: f0 ef       ..    
    bmi loop_c9a39                                                    ; 9aab: 30 8c       0.    
    lda l002d                                                         ; 9aad: a5 2d       .-    
    eor #&80                                                          ; 9aaf: 49 80       I.    
    sta l002d                                                         ; 9ab1: 85 2d       .-    
    sec                                                               ; 9ab3: 38          8     
    ldy #0                                                            ; 9ab4: a0 00       ..    
    lda (l0004),y                                                     ; 9ab6: b1 04       ..    
    sbc l002a                                                         ; 9ab8: e5 2a       .*    
    sta l002a                                                         ; 9aba: 85 2a       .*    
    iny                                                               ; 9abc: c8          .     
    lda (l0004),y                                                     ; 9abd: b1 04       ..    
    sbc l002b                                                         ; 9abf: e5 2b       .+    
    sta l002b                                                         ; 9ac1: 85 2b       .+    
    iny                                                               ; 9ac3: c8          .     
    lda (l0004),y                                                     ; 9ac4: b1 04       ..    
    sbc l002c                                                         ; 9ac6: e5 2c       .,    
    sta l002c                                                         ; 9ac8: 85 2c       .,    
    iny                                                               ; 9aca: c8          .     
    lda (l0004),y                                                     ; 9acb: b1 04       ..    
    ldy #0                                                            ; 9acd: a0 00       ..    
    eor #&80                                                          ; 9acf: 49 80       I.    
    sbc l002d                                                         ; 9ad1: e5 2d       .-    
    ora l002a                                                         ; 9ad3: 05 2a       .*    
    ora l002b                                                         ; 9ad5: 05 2b       .+    
    ora l002c                                                         ; 9ad7: 05 2c       .,    
    php                                                               ; 9ad9: 08          .     
    clc                                                               ; 9ada: 18          .     
    lda #4                                                            ; 9adb: a9 04       ..    
    adc l0004                                                         ; 9add: 65 04       e.    
    sta l0004                                                         ; 9adf: 85 04       ..    
    bcc c9ae5                                                         ; 9ae1: 90 02       ..    
    inc l0005                                                         ; 9ae3: e6 05       ..    
; &9ae5 referenced 1 time by &9ae1
.c9ae5
    plp                                                               ; 9ae5: 28          (     
    rts                                                               ; 9ae6: 60          `     
; &9ae7 referenced 1 time by &9a9e
.c9ae7
    jsr sub_cbdb2                                                     ; 9ae7: 20 b2 bd     ..   
    jsr sub_c9c42                                                     ; 9aea: 20 42 9c     B.   
    tay                                                               ; 9aed: a8          .     
    bne c9a9a                                                         ; 9aee: d0 aa       ..    
    stx l0037                                                         ; 9af0: 86 37       .7    
    ldx l0036                                                         ; 9af2: a6 36       .6    
    ldy #0                                                            ; 9af4: a0 00       ..    
    lda (l0004),y                                                     ; 9af6: b1 04       ..    
    sta l0039                                                         ; 9af8: 85 39       .9    
    cmp l0036                                                         ; 9afa: c5 36       .6    
    bcs c9aff                                                         ; 9afc: b0 01       ..    
    tax                                                               ; 9afe: aa          .     
; &9aff referenced 1 time by &9afc
.c9aff
    stx l003a                                                         ; 9aff: 86 3a       .:    
    ldy #0                                                            ; 9b01: a0 00       ..    
; &9b03 referenced 1 time by &9b0d
.loop_c9b03
    cpy l003a                                                         ; 9b03: c4 3a       .:    
    beq c9b11                                                         ; 9b05: f0 0a       ..    
    iny                                                               ; 9b07: c8          .     
    lda (l0004),y                                                     ; 9b08: b1 04       ..    
    cmp l05ff,y                                                       ; 9b0a: d9 ff 05    ...   
    beq loop_c9b03                                                    ; 9b0d: f0 f4       ..    
    bne c9b15                                                         ; 9b0f: d0 04       ..    
; &9b11 referenced 1 time by &9b05
.c9b11
    lda l0039                                                         ; 9b11: a5 39       .9    
    cmp l0036                                                         ; 9b13: c5 36       .6    
; &9b15 referenced 1 time by &9b0f
.c9b15
    php                                                               ; 9b15: 08          .     
    jsr cbddc                                                         ; 9b16: 20 dc bd     ..   
    ldx l0037                                                         ; 9b19: a6 37       .7    
    plp                                                               ; 9b1b: 28          (     
    rts                                                               ; 9b1c: 60          `     
; &9b1d referenced 3 times by &8821, &886d, &8b53
.sub_c9b1d
    lda l000b                                                         ; 9b1d: a5 0b       ..    
    sta l0019                                                         ; 9b1f: 85 19       ..    
    lda l000c                                                         ; 9b21: a5 0c       ..    
    sta l001a                                                         ; 9b23: 85 1a       ..    
    lda l000a                                                         ; 9b25: a5 0a       ..    
    sta l001b                                                         ; 9b27: 85 1b       ..    
; &9b29 referenced 3 times by &92dd, &9849, &ae56
.sub_c9b29
    jsr sub_c9b72                                                     ; 9b29: 20 72 9b     r.   
; &9b2c referenced 1 time by &9b53
.loop_c9b2c
    cpx #&84                                                          ; 9b2c: e0 84       ..    
    beq c9b3a                                                         ; 9b2e: f0 0a       ..    
    cpx #&82                                                          ; 9b30: e0 82       ..    
    beq c9b55                                                         ; 9b32: f0 21       .!    
    dec l001b                                                         ; 9b34: c6 1b       ..    
    tay                                                               ; 9b36: a8          .     
    sta l0027                                                         ; 9b37: 85 27       .'    
    rts                                                               ; 9b39: 60          `     
; &9b3a referenced 1 time by &9b2e
.c9b3a
    jsr sub_c9b6b                                                     ; 9b3a: 20 6b 9b     k.   
    tay                                                               ; 9b3d: a8          .     
    jsr c92f0                                                         ; 9b3e: 20 f0 92     ..   
    ldy #3                                                            ; 9b41: a0 03       ..    
; &9b43 referenced 1 time by &9b4c
.loop_c9b43
    lda (l0004),y                                                     ; 9b43: b1 04       ..    
    ora l002a,y                                                       ; 9b45: 19 2a 00    .*.   
    sta l002a,y                                                       ; 9b48: 99 2a 00    .*.   
    dey                                                               ; 9b4b: 88          .     
    bpl loop_c9b43                                                    ; 9b4c: 10 f5       ..    
; &9b4e referenced 1 time by &9b69
.loop_c9b4e
    jsr sub_cbdff                                                     ; 9b4e: 20 ff bd     ..   
    lda #&40 ; '@'                                                    ; 9b51: a9 40       .@    
    bne loop_c9b2c                                                    ; 9b53: d0 d7       ..    
; &9b55 referenced 1 time by &9b32
.c9b55
    jsr sub_c9b6b                                                     ; 9b55: 20 6b 9b     k.   
    tay                                                               ; 9b58: a8          .     
    jsr c92f0                                                         ; 9b59: 20 f0 92     ..   
    ldy #3                                                            ; 9b5c: a0 03       ..    
; &9b5e referenced 1 time by &9b67
.loop_c9b5e
    lda (l0004),y                                                     ; 9b5e: b1 04       ..    
    eor l002a,y                                                       ; 9b60: 59 2a 00    Y*.   
    sta l002a,y                                                       ; 9b63: 99 2a 00    .*.   
    dey                                                               ; 9b66: 88          .     
    bpl loop_c9b5e                                                    ; 9b67: 10 f5       ..    
    bmi loop_c9b4e                                                    ; 9b69: 30 e3       0.    
; &9b6b referenced 2 times by &9b3a, &9b55
.sub_c9b6b
    tay                                                               ; 9b6b: a8          .     
    jsr c92f0                                                         ; 9b6c: 20 f0 92     ..   
    jsr sub_cbd94                                                     ; 9b6f: 20 94 bd     ..   
; &9b72 referenced 1 time by &9b29
.sub_c9b72
    jsr sub_c9b9c                                                     ; 9b72: 20 9c 9b     ..   
; &9b75 referenced 1 time by &9b9a
.loop_c9b75
    cpx #&80                                                          ; 9b75: e0 80       ..    
    beq c9b7a                                                         ; 9b77: f0 01       ..    
    rts                                                               ; 9b79: 60          `     
; &9b7a referenced 1 time by &9b77
.c9b7a
    tay                                                               ; 9b7a: a8          .     
    jsr c92f0                                                         ; 9b7b: 20 f0 92     ..   
    jsr sub_cbd94                                                     ; 9b7e: 20 94 bd     ..   
    jsr sub_c9b9c                                                     ; 9b81: 20 9c 9b     ..   
    tay                                                               ; 9b84: a8          .     
    jsr c92f0                                                         ; 9b85: 20 f0 92     ..   
    ldy #3                                                            ; 9b88: a0 03       ..    
; &9b8a referenced 1 time by &9b93
.loop_c9b8a
    lda (l0004),y                                                     ; 9b8a: b1 04       ..    
    and l002a,y                                                       ; 9b8c: 39 2a 00    9*.   
    sta l002a,y                                                       ; 9b8f: 99 2a 00    .*.   
    dey                                                               ; 9b92: 88          .     
    bpl loop_c9b8a                                                    ; 9b93: 10 f5       ..    
    jsr sub_cbdff                                                     ; 9b95: 20 ff bd     ..   
    lda #&40 ; '@'                                                    ; 9b98: a9 40       .@    
    bne loop_c9b75                                                    ; 9b9a: d0 d9       ..    
; &9b9c referenced 2 times by &9b72, &9b81
.sub_c9b9c
    jsr sub_c9c42                                                     ; 9b9c: 20 42 9c     B.   
    cpx #&3f ; '?'                                                    ; 9b9f: e0 3f       .?    
    bcs return_13                                                     ; 9ba1: b0 04       ..    
    cpx #&3c ; '<'                                                    ; 9ba3: e0 3c       .<    
    bcs c9ba8                                                         ; 9ba5: b0 01       ..    
; &9ba7 referenced 1 time by &9ba1
.return_13
    rts                                                               ; 9ba7: 60          `     
; &9ba8 referenced 1 time by &9ba5
.c9ba8
    beq c9bc0                                                         ; 9ba8: f0 16       ..    
    cpx #&3e ; '>'                                                    ; 9baa: e0 3e       .>    
    beq c9be8                                                         ; 9bac: f0 3a       .:    
    tax                                                               ; 9bae: aa          .     
    jsr sub_c9a9e                                                     ; 9baf: 20 9e 9a     ..   
    bne c9bb5                                                         ; 9bb2: d0 01       ..    
; &9bb4 referenced 6 times by &9bd0, &9bd9, &9bdb, &9be4, &9bf6, &9bff
.c9bb4
    dey                                                               ; 9bb4: 88          .     
; &9bb5 referenced 7 times by &9bb2, &9bd2, &9bdd, &9be6, &9bf4, &9bf8, &9c01
.c9bb5
    sty l002a                                                         ; 9bb5: 84 2a       .*    
    sty l002b                                                         ; 9bb7: 84 2b       .+    
    sty l002c                                                         ; 9bb9: 84 2c       .,    
    sty l002d                                                         ; 9bbb: 84 2d       .-    
    lda #&40 ; '@'                                                    ; 9bbd: a9 40       .@    
    rts                                                               ; 9bbf: 60          `     
; &9bc0 referenced 1 time by &9ba8
.c9bc0
    tax                                                               ; 9bc0: aa          .     
    ldy l001b                                                         ; 9bc1: a4 1b       ..    
    lda (l0019),y                                                     ; 9bc3: b1 19       ..    
    cmp #&3d ; '='                                                    ; 9bc5: c9 3d       .=    
    beq c9bd4                                                         ; 9bc7: f0 0b       ..    
    cmp #&3e ; '>'                                                    ; 9bc9: c9 3e       .>    
    beq c9bdf                                                         ; 9bcb: f0 12       ..    
    jsr sub_c9a9d                                                     ; 9bcd: 20 9d 9a     ..   
    bcc c9bb4                                                         ; 9bd0: 90 e2       ..    
    bcs c9bb5                                                         ; 9bd2: b0 e1       ..    
; &9bd4 referenced 1 time by &9bc7
.c9bd4
    inc l001b                                                         ; 9bd4: e6 1b       ..    
    jsr sub_c9a9d                                                     ; 9bd6: 20 9d 9a     ..   
    beq c9bb4                                                         ; 9bd9: f0 d9       ..    
    bcc c9bb4                                                         ; 9bdb: 90 d7       ..    
    bcs c9bb5                                                         ; 9bdd: b0 d6       ..    
; &9bdf referenced 1 time by &9bcb
.c9bdf
    inc l001b                                                         ; 9bdf: e6 1b       ..    
    jsr sub_c9a9d                                                     ; 9be1: 20 9d 9a     ..   
    bne c9bb4                                                         ; 9be4: d0 ce       ..    
    beq c9bb5                                                         ; 9be6: f0 cd       ..    
; &9be8 referenced 1 time by &9bac
.c9be8
    tax                                                               ; 9be8: aa          .     
    ldy l001b                                                         ; 9be9: a4 1b       ..    
    lda (l0019),y                                                     ; 9beb: b1 19       ..    
    cmp #&3d ; '='                                                    ; 9bed: c9 3d       .=    
    beq c9bfa                                                         ; 9bef: f0 09       ..    
    jsr sub_c9a9d                                                     ; 9bf1: 20 9d 9a     ..   
    beq c9bb5                                                         ; 9bf4: f0 bf       ..    
    bcs c9bb4                                                         ; 9bf6: b0 bc       ..    
    bcc c9bb5                                                         ; 9bf8: 90 bb       ..    
; &9bfa referenced 1 time by &9bef
.c9bfa
    inc l001b                                                         ; 9bfa: e6 1b       ..    
    jsr sub_c9a9d                                                     ; 9bfc: 20 9d 9a     ..   
    bcs c9bb4                                                         ; 9bff: b0 b3       ..    
    bcc c9bb5                                                         ; 9c01: 90 b2       ..    
; &9c03 referenced 1 time by &9c27
.loop_c9c03
    brk                                                               ; 9c03: 00          .     
    equb &13                                                          ; 9c04: 13          .     
    equs "String too long"                                            ; 9c05: 53 74 72... Str...
    equb &00                                                          ; 9c14: 00          .     
; &9c15 referenced 1 time by &9c4f
.loop_c9c15
    jsr sub_cbdb2                                                     ; 9c15: 20 b2 bd     ..   
    jsr sub_c9e20                                                     ; 9c18: 20 20 9e      .   
    tay                                                               ; 9c1b: a8          .     
    bne c9c88                                                         ; 9c1c: d0 6a       .j    
    clc                                                               ; 9c1e: 18          .     
    stx l0037                                                         ; 9c1f: 86 37       .7    
    ldy #0                                                            ; 9c21: a0 00       ..    
    lda (l0004),y                                                     ; 9c23: b1 04       ..    
    adc l0036                                                         ; 9c25: 65 36       e6    
    bcs loop_c9c03                                                    ; 9c27: b0 da       ..    
    tax                                                               ; 9c29: aa          .     
    pha                                                               ; 9c2a: 48          H     
    ldy l0036                                                         ; 9c2b: a4 36       .6    
; &9c2d referenced 1 time by &9c35
.loop_c9c2d
    lda l05ff,y                                                       ; 9c2d: b9 ff 05    ...   
    sta l05ff,x                                                       ; 9c30: 9d ff 05    ...   
    dex                                                               ; 9c33: ca          .     
    dey                                                               ; 9c34: 88          .     
    bne loop_c9c2d                                                    ; 9c35: d0 f6       ..    
    jsr sub_cbdcb                                                     ; 9c37: 20 cb bd     ..   
    pla                                                               ; 9c3a: 68          h     
    sta l0036                                                         ; 9c3b: 85 36       .6    
    ldx l0037                                                         ; 9c3d: a6 37       .7    
    tya                                                               ; 9c3f: 98          .     
    beq c9c45                                                         ; 9c40: f0 03       ..    
; &9c42 referenced 4 times by &9a53, &9aa5, &9aea, &9b9c
.sub_c9c42
    jsr sub_c9dd1                                                     ; 9c42: 20 d1 9d     ..   
; &9c45 referenced 4 times by &9c40, &9c82, &9c86, &9ca5
.c9c45
    cpx #&2b ; '+'                                                    ; 9c45: e0 2b       .+    
    beq c9c4e                                                         ; 9c47: f0 05       ..    
    cpx #&2d ; '-'                                                    ; 9c49: e0 2d       .-    
    beq c9cb5                                                         ; 9c4b: f0 68       .h    
    rts                                                               ; 9c4d: 60          `     
; &9c4e referenced 1 time by &9c47
.c9c4e
    tay                                                               ; 9c4e: a8          .     
    beq loop_c9c15                                                    ; 9c4f: f0 c4       ..    
    bmi c9c8b                                                         ; 9c51: 30 38       08    
    jsr sub_c9dce                                                     ; 9c53: 20 ce 9d     ..   
    tay                                                               ; 9c56: a8          .     
    beq c9c88                                                         ; 9c57: f0 2f       ./    
    bmi c9ca7                                                         ; 9c59: 30 4c       0L    
    ldy #0                                                            ; 9c5b: a0 00       ..    
    clc                                                               ; 9c5d: 18          .     
    lda (l0004),y                                                     ; 9c5e: b1 04       ..    
    adc l002a                                                         ; 9c60: 65 2a       e*    
    sta l002a                                                         ; 9c62: 85 2a       .*    
    iny                                                               ; 9c64: c8          .     
    lda (l0004),y                                                     ; 9c65: b1 04       ..    
    adc l002b                                                         ; 9c67: 65 2b       e+    
    sta l002b                                                         ; 9c69: 85 2b       .+    
    iny                                                               ; 9c6b: c8          .     
    lda (l0004),y                                                     ; 9c6c: b1 04       ..    
    adc l002c                                                         ; 9c6e: 65 2c       e,    
    sta l002c                                                         ; 9c70: 85 2c       .,    
    iny                                                               ; 9c72: c8          .     
    lda (l0004),y                                                     ; 9c73: b1 04       ..    
    adc l002d                                                         ; 9c75: 65 2d       e-    
; &9c77 referenced 1 time by &9cde
.c9c77
    sta l002d                                                         ; 9c77: 85 2d       .-    
    clc                                                               ; 9c79: 18          .     
    lda l0004                                                         ; 9c7a: a5 04       ..    
    adc #4                                                            ; 9c7c: 69 04       i.    
    sta l0004                                                         ; 9c7e: 85 04       ..    
    lda #&40 ; '@'                                                    ; 9c80: a9 40       .@    
    bcc c9c45                                                         ; 9c82: 90 c1       ..    
    inc l0005                                                         ; 9c84: e6 05       ..    
    bcs c9c45                                                         ; 9c86: b0 bd       ..    
; &9c88 referenced 6 times by &9c1c, &9c57, &9c92, &9cb6, &9cbe, &9ce8
.c9c88
    jmp c8c0e                                                         ; 9c88: 4c 0e 8c    L..   
; &9c8b referenced 1 time by &9c51
.c9c8b
    jsr sub_cbd51                                                     ; 9c8b: 20 51 bd     Q.   
    jsr sub_c9dd1                                                     ; 9c8e: 20 d1 9d     ..   
    tay                                                               ; 9c91: a8          .     
    beq c9c88                                                         ; 9c92: f0 f4       ..    
    stx l0027                                                         ; 9c94: 86 27       .'    
    bmi c9c9b                                                         ; 9c96: 30 03       0.    
    jsr ca2be                                                         ; 9c98: 20 be a2     ..   
; &9c9b referenced 2 times by &9c96, &9cb2
.c9c9b
    jsr sub_cbd7e                                                     ; 9c9b: 20 7e bd     ~.   
    jsr sub_ca500                                                     ; 9c9e: 20 00 a5     ..   
; &9ca1 referenced 2 times by &9cf7, &9d0b
.c9ca1
    ldx l0027                                                         ; 9ca1: a6 27       .'    
    lda #&ff                                                          ; 9ca3: a9 ff       ..    
    bne c9c45                                                         ; 9ca5: d0 9e       ..    
; &9ca7 referenced 1 time by &9c59
.c9ca7
    stx l0027                                                         ; 9ca7: 86 27       .'    
    jsr sub_cbdea                                                     ; 9ca9: 20 ea bd     ..   
    jsr sub_cbd51                                                     ; 9cac: 20 51 bd     Q.   
    jsr ca2be                                                         ; 9caf: 20 be a2     ..   
    jmp c9c9b                                                         ; 9cb2: 4c 9b 9c    L..   
; &9cb5 referenced 1 time by &9c4b
.c9cb5
    tay                                                               ; 9cb5: a8          .     
    beq c9c88                                                         ; 9cb6: f0 d0       ..    
    bmi c9ce1                                                         ; 9cb8: 30 27       0'    
    jsr sub_c9dce                                                     ; 9cba: 20 ce 9d     ..   
    tay                                                               ; 9cbd: a8          .     
    beq c9c88                                                         ; 9cbe: f0 c8       ..    
    bmi c9cfa                                                         ; 9cc0: 30 38       08    
    sec                                                               ; 9cc2: 38          8     
    ldy #0                                                            ; 9cc3: a0 00       ..    
    lda (l0004),y                                                     ; 9cc5: b1 04       ..    
    sbc l002a                                                         ; 9cc7: e5 2a       .*    
    sta l002a                                                         ; 9cc9: 85 2a       .*    
    iny                                                               ; 9ccb: c8          .     
    lda (l0004),y                                                     ; 9ccc: b1 04       ..    
    sbc l002b                                                         ; 9cce: e5 2b       .+    
    sta l002b                                                         ; 9cd0: 85 2b       .+    
    iny                                                               ; 9cd2: c8          .     
    lda (l0004),y                                                     ; 9cd3: b1 04       ..    
    sbc l002c                                                         ; 9cd5: e5 2c       .,    
    sta l002c                                                         ; 9cd7: 85 2c       .,    
    iny                                                               ; 9cd9: c8          .     
    lda (l0004),y                                                     ; 9cda: b1 04       ..    
    sbc l002d                                                         ; 9cdc: e5 2d       .-    
    jmp c9c77                                                         ; 9cde: 4c 77 9c    Lw.   
; &9ce1 referenced 1 time by &9cb8
.c9ce1
    jsr sub_cbd51                                                     ; 9ce1: 20 51 bd     Q.   
    jsr sub_c9dd1                                                     ; 9ce4: 20 d1 9d     ..   
    tay                                                               ; 9ce7: a8          .     
    beq c9c88                                                         ; 9ce8: f0 9e       ..    
    stx l0027                                                         ; 9cea: 86 27       .'    
    bmi c9cf1                                                         ; 9cec: 30 03       0.    
    jsr ca2be                                                         ; 9cee: 20 be a2     ..   
; &9cf1 referenced 1 time by &9cec
.c9cf1
    jsr sub_cbd7e                                                     ; 9cf1: 20 7e bd     ~.   
    jsr sub_ca4fd                                                     ; 9cf4: 20 fd a4     ..   
    jmp c9ca1                                                         ; 9cf7: 4c a1 9c    L..   
; &9cfa referenced 1 time by &9cc0
.c9cfa
    stx l0027                                                         ; 9cfa: 86 27       .'    
    jsr sub_cbdea                                                     ; 9cfc: 20 ea bd     ..   
    jsr sub_cbd51                                                     ; 9cff: 20 51 bd     Q.   
    jsr ca2be                                                         ; 9d02: 20 be a2     ..   
    jsr sub_cbd7e                                                     ; 9d05: 20 7e bd     ~.   
    jsr sub_ca4d0                                                     ; 9d08: 20 d0 a4     ..   
    jmp c9ca1                                                         ; 9d0b: 4c a1 9c    L..   
; &9d0e referenced 3 times by &9d60, &9d67, &9d6b
.c9d0e
    jsr ca2be                                                         ; 9d0e: 20 be a2     ..   
; &9d11 referenced 1 time by &9d5a
.loop_c9d11
    jsr sub_cbdea                                                     ; 9d11: 20 ea bd     ..   
    jsr sub_cbd51                                                     ; 9d14: 20 51 bd     Q.   
    jsr ca2be                                                         ; 9d17: 20 be a2     ..   
    jmp c9d2c                                                         ; 9d1a: 4c 2c 9d    L,.   
; &9d1d referenced 3 times by &9d45, &9d4c, &9d50
.c9d1d
    jsr ca2be                                                         ; 9d1d: 20 be a2     ..   
; &9d20 referenced 1 time by &9d3f
.loop_c9d20
    jsr sub_cbd51                                                     ; 9d20: 20 51 bd     Q.   
    jsr sub_c9e20                                                     ; 9d23: 20 20 9e      .   
    stx l0027                                                         ; 9d26: 86 27       .'    
    tay                                                               ; 9d28: a8          .     
    jsr sub_c92fd                                                     ; 9d29: 20 fd 92     ..   
; &9d2c referenced 1 time by &9d1a
.c9d2c
    jsr sub_cbd7e                                                     ; 9d2c: 20 7e bd     ~.   
    jsr sub_ca656                                                     ; 9d2f: 20 56 a6     V.   
    lda #&ff                                                          ; 9d32: a9 ff       ..    
    ldx l0027                                                         ; 9d34: a6 27       .'    
    jmp c9dd4                                                         ; 9d36: 4c d4 9d    L..   
; &9d39 referenced 2 times by &9d3d, &9d58
.c9d39
    jmp c8c0e                                                         ; 9d39: 4c 0e 8c    L..   
; &9d3c referenced 1 time by &9dcb
.c9d3c
    tay                                                               ; 9d3c: a8          .     
    beq c9d39                                                         ; 9d3d: f0 fa       ..    
    bmi loop_c9d20                                                    ; 9d3f: 30 df       0.    
    lda l002d                                                         ; 9d41: a5 2d       .-    
    cmp l002c                                                         ; 9d43: c5 2c       .,    
    bne c9d1d                                                         ; 9d45: d0 d6       ..    
    tay                                                               ; 9d47: a8          .     
    beq c9d4e                                                         ; 9d48: f0 04       ..    
    cmp #&ff                                                          ; 9d4a: c9 ff       ..    
    bne c9d1d                                                         ; 9d4c: d0 cf       ..    
; &9d4e referenced 1 time by &9d48
.c9d4e
    eor l002b                                                         ; 9d4e: 45 2b       E+    
    bmi c9d1d                                                         ; 9d50: 30 cb       0.    
    jsr sub_c9e1d                                                     ; 9d52: 20 1d 9e     ..   
    stx l0027                                                         ; 9d55: 86 27       .'    
    tay                                                               ; 9d57: a8          .     
    beq c9d39                                                         ; 9d58: f0 df       ..    
    bmi loop_c9d11                                                    ; 9d5a: 30 b5       0.    
    lda l002d                                                         ; 9d5c: a5 2d       .-    
    cmp l002c                                                         ; 9d5e: c5 2c       .,    
    bne c9d0e                                                         ; 9d60: d0 ac       ..    
    tay                                                               ; 9d62: a8          .     
    beq c9d69                                                         ; 9d63: f0 04       ..    
    cmp #&ff                                                          ; 9d65: c9 ff       ..    
    bne c9d0e                                                         ; 9d67: d0 a5       ..    
; &9d69 referenced 1 time by &9d63
.c9d69
    eor l002b                                                         ; 9d69: 45 2b       E+    
    bmi c9d0e                                                         ; 9d6b: 30 a1       0.    
    lda l002d                                                         ; 9d6d: a5 2d       .-    
    pha                                                               ; 9d6f: 48          H     
    jsr sub_cad71                                                     ; 9d70: 20 71 ad     q.   
    ldx #&39 ; '9'                                                    ; 9d73: a2 39       .9    
    jsr sub_cbe44                                                     ; 9d75: 20 44 be     D.   
    jsr sub_cbdea                                                     ; 9d78: 20 ea bd     ..   
    pla                                                               ; 9d7b: 68          h     
    eor l002d                                                         ; 9d7c: 45 2d       E-    
    sta l0037                                                         ; 9d7e: 85 37       .7    
    jsr sub_cad71                                                     ; 9d80: 20 71 ad     q.   
    ldy #0                                                            ; 9d83: a0 00       ..    
    ldx #0                                                            ; 9d85: a2 00       ..    
    sty l003f                                                         ; 9d87: 84 3f       .?    
    sty l0040                                                         ; 9d89: 84 40       .@    
; &9d8b referenced 1 time by &9db2
.loop_c9d8b
    lsr l003a                                                         ; 9d8b: 46 3a       F:    
    ror l0039                                                         ; 9d8d: 66 39       f9    
    bcc c9da6                                                         ; 9d8f: 90 15       ..    
    clc                                                               ; 9d91: 18          .     
    tya                                                               ; 9d92: 98          .     
    adc l002a                                                         ; 9d93: 65 2a       e*    
    tay                                                               ; 9d95: a8          .     
    txa                                                               ; 9d96: 8a          .     
    adc l002b                                                         ; 9d97: 65 2b       e+    
    tax                                                               ; 9d99: aa          .     
    lda l003f                                                         ; 9d9a: a5 3f       .?    
    adc l002c                                                         ; 9d9c: 65 2c       e,    
    sta l003f                                                         ; 9d9e: 85 3f       .?    
    lda l0040                                                         ; 9da0: a5 40       .@    
    adc l002d                                                         ; 9da2: 65 2d       e-    
    sta l0040                                                         ; 9da4: 85 40       .@    
; &9da6 referenced 1 time by &9d8f
.c9da6
    asl l002a                                                         ; 9da6: 06 2a       .*    
    rol l002b                                                         ; 9da8: 26 2b       &+    
    rol l002c                                                         ; 9daa: 26 2c       &,    
    rol l002d                                                         ; 9dac: 26 2d       &-    
    lda l0039                                                         ; 9dae: a5 39       .9    
    ora l003a                                                         ; 9db0: 05 3a       .:    
    bne loop_c9d8b                                                    ; 9db2: d0 d7       ..    
    sty l003d                                                         ; 9db4: 84 3d       .=    
    stx l003e                                                         ; 9db6: 86 3e       .>    
    lda l0037                                                         ; 9db8: a5 37       .7    
    php                                                               ; 9dba: 08          .     
; &9dbb referenced 1 time by &9e07
.c9dbb
    ldx #&3d ; '='                                                    ; 9dbb: a2 3d       .=    
; &9dbd referenced 1 time by &9e1a
.c9dbd
    jsr sub_caf56                                                     ; 9dbd: 20 56 af     V.   
    plp                                                               ; 9dc0: 28          (     
    bpl c9dc6                                                         ; 9dc1: 10 03       ..    
    jsr cad93                                                         ; 9dc3: 20 93 ad     ..   
; &9dc6 referenced 1 time by &9dc1
.c9dc6
    ldx l0027                                                         ; 9dc6: a6 27       .'    
    jmp c9dd4                                                         ; 9dc8: 4c d4 9d    L..   
; &9dcb referenced 1 time by &9dd6
.loop_c9dcb
    jmp c9d3c                                                         ; 9dcb: 4c 3c 9d    L<.   
; &9dce referenced 2 times by &9c53, &9cba
.sub_c9dce
    jsr sub_cbd94                                                     ; 9dce: 20 94 bd     ..   
; &9dd1 referenced 3 times by &9c42, &9c8e, &9ce4
.sub_c9dd1
    jsr sub_c9e20                                                     ; 9dd1: 20 20 9e      .   
; &9dd4 referenced 3 times by &9d36, &9dc8, &9dff
.c9dd4
    cpx #&2a ; '*'                                                    ; 9dd4: e0 2a       .*    
    beq loop_c9dcb                                                    ; 9dd6: f0 f3       ..    
    cpx #&2f ; '/'                                                    ; 9dd8: e0 2f       ./    
    beq c9de5                                                         ; 9dda: f0 09       ..    
    cpx #&83                                                          ; 9ddc: e0 83       ..    
    beq c9e01                                                         ; 9dde: f0 21       .!    
    cpx #&81                                                          ; 9de0: e0 81       ..    
    beq c9e0a                                                         ; 9de2: f0 26       .&    
    rts                                                               ; 9de4: 60          `     
; &9de5 referenced 1 time by &9dda
.c9de5
    tay                                                               ; 9de5: a8          .     
    jsr sub_c92fd                                                     ; 9de6: 20 fd 92     ..   
    jsr sub_cbd51                                                     ; 9de9: 20 51 bd     Q.   
    jsr sub_c9e20                                                     ; 9dec: 20 20 9e      .   
    stx l0027                                                         ; 9def: 86 27       .'    
    tay                                                               ; 9df1: a8          .     
    jsr sub_c92fd                                                     ; 9df2: 20 fd 92     ..   
    jsr sub_cbd7e                                                     ; 9df5: 20 7e bd     ~.   
    jsr sub_ca6ad                                                     ; 9df8: 20 ad a6     ..   
    ldx l0027                                                         ; 9dfb: a6 27       .'    
    lda #&ff                                                          ; 9dfd: a9 ff       ..    
    bne c9dd4                                                         ; 9dff: d0 d3       ..    
; &9e01 referenced 1 time by &9dde
.c9e01
    jsr sub_c99be                                                     ; 9e01: 20 be 99     ..   
    lda l0038                                                         ; 9e04: a5 38       .8    
    php                                                               ; 9e06: 08          .     
    jmp c9dbb                                                         ; 9e07: 4c bb 9d    L..   
; &9e0a referenced 1 time by &9de2
.c9e0a
    jsr sub_c99be                                                     ; 9e0a: 20 be 99     ..   
    rol l0039                                                         ; 9e0d: 26 39       &9    
    rol l003a                                                         ; 9e0f: 26 3a       &:    
    rol l003b                                                         ; 9e11: 26 3b       &;    
    rol l003c                                                         ; 9e13: 26 3c       &<    
    bit l0037                                                         ; 9e15: 24 37       $7    
    php                                                               ; 9e17: 08          .     
    ldx #&39 ; '9'                                                    ; 9e18: a2 39       .9    
    jmp c9dbd                                                         ; 9e1a: 4c bd 9d    L..   
; &9e1d referenced 2 times by &99c8, &9d52
.sub_c9e1d
    jsr sub_cbd94                                                     ; 9e1d: 20 94 bd     ..   
; &9e20 referenced 4 times by &9c18, &9d23, &9dd1, &9dec
.sub_c9e20
    jsr cadec                                                         ; 9e20: 20 ec ad     ..   
; &9e23 referenced 2 times by &9e57, &9e86
.c9e23
    pha                                                               ; 9e23: 48          H     
; &9e24 referenced 1 time by &9e2c
.loop_c9e24
    ldy l001b                                                         ; 9e24: a4 1b       ..    
    inc l001b                                                         ; 9e26: e6 1b       ..    
    lda (l0019),y                                                     ; 9e28: b1 19       ..    
    cmp #&20 ; ' '                                                    ; 9e2a: c9 20       .     
    beq loop_c9e24                                                    ; 9e2c: f0 f6       ..    
    tax                                                               ; 9e2e: aa          .     
    pla                                                               ; 9e2f: 68          h     
    cpx #&5e ; '^'                                                    ; 9e30: e0 5e       .^    
    beq c9e35                                                         ; 9e32: f0 01       ..    
    rts                                                               ; 9e34: 60          `     
; &9e35 referenced 1 time by &9e32
.c9e35
    tay                                                               ; 9e35: a8          .     
    jsr sub_c92fd                                                     ; 9e36: 20 fd 92     ..   
    jsr sub_cbd51                                                     ; 9e39: 20 51 bd     Q.   
    jsr sub_c92fa                                                     ; 9e3c: 20 fa 92     ..   
    lda l0030                                                         ; 9e3f: a5 30       .0    
    cmp #&87                                                          ; 9e41: c9 87       ..    
    bcs c9e88                                                         ; 9e43: b0 43       .C    
    jsr sub_ca486                                                     ; 9e45: 20 86 a4     ..   
    bne c9e59                                                         ; 9e48: d0 0f       ..    
    jsr sub_cbd7e                                                     ; 9e4a: 20 7e bd     ~.   
    jsr sub_ca3b5                                                     ; 9e4d: 20 b5 a3     ..   
    lda l004a                                                         ; 9e50: a5 4a       .J    
    jsr sub_cab12                                                     ; 9e52: 20 12 ab     ..   
    lda #&ff                                                          ; 9e55: a9 ff       ..    
    bne c9e23                                                         ; 9e57: d0 ca       ..    
; &9e59 referenced 1 time by &9e48
.c9e59
    jsr sub_ca381                                                     ; 9e59: 20 81 a3     ..   
    lda l0004                                                         ; 9e5c: a5 04       ..    
    sta l004b                                                         ; 9e5e: 85 4b       .K    
    lda l0005                                                         ; 9e60: a5 05       ..    
    sta l004c                                                         ; 9e62: 85 4c       .L    
    jsr sub_ca3b5                                                     ; 9e64: 20 b5 a3     ..   
    lda l004a                                                         ; 9e67: a5 4a       .J    
    jsr sub_cab12                                                     ; 9e69: 20 12 ab     ..   
; &9e6c referenced 1 time by &9e8e
.loop_c9e6c
    jsr sub_ca37d                                                     ; 9e6c: 20 7d a3     }.   
    jsr sub_cbd7e                                                     ; 9e6f: 20 7e bd     ~.   
    jsr sub_ca3b5                                                     ; 9e72: 20 b5 a3     ..   
    jsr sub_ca801                                                     ; 9e75: 20 01 a8     ..   
    jsr sub_caad1                                                     ; 9e78: 20 d1 aa     ..   
    jsr sub_caa94                                                     ; 9e7b: 20 94 aa     ..   
    jsr sub_ca7ed                                                     ; 9e7e: 20 ed a7     ..   
    jsr sub_ca656                                                     ; 9e81: 20 56 a6     V.   
    lda #&ff                                                          ; 9e84: a9 ff       ..    
    bne c9e23                                                         ; 9e86: d0 9b       ..    
; &9e88 referenced 1 time by &9e43
.c9e88
    jsr sub_ca381                                                     ; 9e88: 20 81 a3     ..   
    jsr sub_ca699                                                     ; 9e8b: 20 99 a6     ..   
    bne loop_c9e6c                                                    ; 9e8e: d0 dc       ..    
    tya                                                               ; 9e90: 98          .     
    bpl c9e96                                                         ; 9e91: 10 03       ..    
    jsr ca3e4                                                         ; 9e93: 20 e4 a3     ..   
; &9e96 referenced 1 time by &9e91
.c9e96
    ldx #0                                                            ; 9e96: a2 00       ..    
    ldy #0                                                            ; 9e98: a0 00       ..    
; &9e9a referenced 1 time by &9eae
.loop_c9e9a
    lda l002a,y                                                       ; 9e9a: b9 2a 00    .*.   
    pha                                                               ; 9e9d: 48          H     
    and #&0f                                                          ; 9e9e: 29 0f       ).    
    sta l003f,x                                                       ; 9ea0: 95 3f       .?    
    pla                                                               ; 9ea2: 68          h     
    lsr a                                                             ; 9ea3: 4a          J     
    lsr a                                                             ; 9ea4: 4a          J     
    lsr a                                                             ; 9ea5: 4a          J     
    lsr a                                                             ; 9ea6: 4a          J     
    inx                                                               ; 9ea7: e8          .     
    sta l003f,x                                                       ; 9ea8: 95 3f       .?    
    inx                                                               ; 9eaa: e8          .     
    iny                                                               ; 9eab: c8          .     
    cpy #4                                                            ; 9eac: c0 04       ..    
    bne loop_c9e9a                                                    ; 9eae: d0 ea       ..    
; &9eb0 referenced 1 time by &9eb5
.loop_c9eb0
    dex                                                               ; 9eb0: ca          .     
    beq c9eb7                                                         ; 9eb1: f0 04       ..    
    lda l003f,x                                                       ; 9eb3: b5 3f       .?    
    beq loop_c9eb0                                                    ; 9eb5: f0 f9       ..    
; &9eb7 referenced 2 times by &9eb1, &9ec5
.c9eb7
    lda l003f,x                                                       ; 9eb7: b5 3f       .?    
    cmp #&0a                                                          ; 9eb9: c9 0a       ..    
    bcc c9ebf                                                         ; 9ebb: 90 02       ..    
    adc #6                                                            ; 9ebd: 69 06       i.    
; &9ebf referenced 1 time by &9ebb
.c9ebf
    adc #&30 ; '0'                                                    ; 9ebf: 69 30       i0    
    jsr sub_ca066                                                     ; 9ec1: 20 66 a0     f.   
    dex                                                               ; 9ec4: ca          .     
    bpl c9eb7                                                         ; 9ec5: 10 f0       ..    
    rts                                                               ; 9ec7: 60          `     
    equb &10, &07, &a9, &2d, &85                                      ; 9ec8: 10 07 a9... ......
    equs ". f"                                                        ; 9ecd: 2e 20 66    . f   
    equb &a0, &a5, &30, &c9, &81, &b0, &4e, &20, &f4, &a1, &c6, &49   ; 9ed0: a0 a5 30... ..0...
    equb &4c, &d1, &9e, &ae, &02, &04, &e0, &03, &90, &02, &a2, &00   ; 9edc: 4c d1 9e... L.....
    equb &86, &37, &ad, &01, &04, &f0, &06, &c9, &0a, &b0, &06, &90   ; 9ee8: 86 37 ad... .7....
    equb &06, &e0, &02, &f0, &02, &a9, &0a, &85, &38, &85, &4e, &a9   ; 9ef4: 06 e0 02... ......
    equb &00, &85, &36, &85, &49, &24, &15, &30, &87, &98, &30, &03   ; 9f00: 00 85 36... ..6...
    equb &20, &be, &a2, &20, &da, &a1, &d0, &b4, &a5, &37, &d0, &05   ; 9f0c: 20 be a2...  .....
    equb &a9                                                          ; 9f18: a9          .     
    equs "0Lf"                                                        ; 9f19: 30 4c 66    0Lf   
    equb &a0, &4c, &9c, &9f, &20, &99, &a6, &d0, &0f, &c9, &84, &90   ; 9f1c: a0 4c 9c... .L....
    equb &10, &d0, &06, &a5, &31, &c9, &a0, &90, &08, &20, &4d, &a2   ; 9f28: 10 d0 06... ......
    equb &e6, &49, &4c, &d1, &9e, &a5, &35, &85, &27, &20, &85, &a3   ; 9f34: e6 49 4c... .IL...
    equb &a5, &4e, &85, &38, &a6, &37, &e0, &02, &d0, &12             ; 9f40: a5 4e 85... .N....
    equs "eI0R"                                                       ; 9f4a: 65 49 30... eI0...
    equb &85, &38, &c9, &0b, &90, &08, &a9, &0a, &85, &38, &a9, &00   ; 9f4e: 85 38 c9... .8....
    equb &85, &37, &20, &86, &a6, &a9, &a0, &85, &31, &a9, &83, &85   ; 9f5a: 85 37 20... .7 ...
    equb &30, &a6, &38, &f0, &06, &20, &4d, &a2, &ca, &d0, &fa, &20   ; 9f66: 30 a6 38... 0.8...
    equb &f5, &a7, &20, &4e, &a3, &a5, &27, &85, &42, &20, &0b, &a5   ; 9f72: f5 a7 20... .. ...
    equb &a5, &30, &c9, &84, &b0, &0e                                 ; 9f7e: a5 30 c9... .0....
    equs "f1f2f3f4f5"                                                 ; 9f84: 66 31 66... f1f...
    equb &e6, &30, &d0, &ec, &a5, &31, &c9, &a0, &b0, &88, &a5, &38   ; 9f8e: e6 30 d0... .0....
    equb &d0, &11, &c9, &01, &f0, &46, &20, &86, &a6, &a9, &00, &85   ; 9f9a: d0 11 c9... ......
    equb &49, &a5, &4e, &85, &38, &e6, &38, &a9, &01, &c5, &37, &f0   ; 9fa6: 49 a5 4e... I.N...
    equb &33, &a4, &49, &30, &0c, &c4, &38, &b0, &2b, &a9, &00, &85   ; 9fb2: 33 a4 49... 3.I...
    equb &49, &c8, &98, &d0, &23, &a5, &37, &c9, &02, &f0, &06, &a9   ; 9fbe: 49 c8 98... I.....
    equb &01, &c0, &ff, &d0, &17, &a9                                 ; 9fca: 01 c0 ff... ......
    equs "0 f"                                                        ; 9fd0: 30 20 66    0 f   
    equb &a0, &a9                                                     ; 9fd3: a0 a9       ..    
    equs ". f"                                                        ; 9fd5: 2e 20 66    . f   
    equb &a0, &a9, &30, &e6, &49, &f0, &05, &20, &66, &a0, &d0, &f7   ; 9fd8: a0 a9 30... ..0...
    equb &a9, &80, &85                                                ; 9fe4: a9 80 85    ...   
    equs "N @"                                                        ; 9fe7: 4e 20 40    N @   
    equb &a0, &c6, &4e, &d0, &05, &a9                                 ; 9fea: a0 c6 4e... ..N...
    equs ". f"                                                        ; 9ff0: 2e 20 66    . f   
    equb &a0, &c6, &38, &d0, &f0, &a4, &37, &88, &f0, &18, &88, &f0   ; 9ff3: a0 c6 38... ..8...
    equb &11, &a4, &36, &88, &b9, &00, &06, &c9, &30, &f0, &f8, &c9   ; 9fff: 11 a4 36... ..6...
    equb &2e, &f0, &01, &c8, &84, &36, &a5, &49, &f0, &2a, &a9        ; a00b: 2e f0 01... ......
    equs "E f"                                                        ; a016: 45 20 66    E f   
    equb &a0, &a5, &49, &10, &0a, &a9                                 ; a019: a0 a5 49... ..I...
    equs "- f"                                                        ; a01f: 2d 20 66    - f   
    equb &a0, &38, &a9, &00, &e5                                      ; a022: a0 38 a9... .8....
    equs "I R"                                                        ; a027: 49 20 52    I R   
    equb &a0, &a5, &37, &f0, &10, &a9, &20, &a4, &49, &30, &03, &20   ; a02a: a0 a5 37... ..7...
    equb &66, &a0, &e0, &00, &d0, &03, &4c, &66, &a0, &60, &a5        ; a036: 66 a0 e0... f.....
    equs "1JJJJ d"                                                    ; a041: 31 4a 4a... 1JJ...
    equb &a0, &a5, &31, &29, &0f, &85, &31, &4c, &97, &a1, &a2, &ff   ; a048: a0 a5 31... ..1...
    equb &38, &e8, &e9, &0a, &b0, &fb, &69, &0a, &48, &8a, &f0, &03   ; a054: 38 e8 e9... 8.....
    equb &20, &64, &a0, &68, &09, &30                                 ; a060: 20 64 a0...  d....
; &a066 referenced 1 time by &9ec1
.sub_ca066
    stx l003b                                                         ; a066: 86 3b       .;    
    ldx l0036                                                         ; a068: a6 36       .6    
    sta l0600,x                                                       ; a06a: 9d 00 06    ...   
    ldx l003b                                                         ; a06d: a6 3b       .;    
    inc l0036                                                         ; a06f: e6 36       .6    
    rts                                                               ; a071: 60          `     
; &a072 referenced 2 times by &a091, &a095
.ca072
    clc                                                               ; a072: 18          .     
    stx l0035                                                         ; a073: 86 35       .5    
    jsr ca1da                                                         ; a075: 20 da a1     ..   
    lda #&ff                                                          ; a078: a9 ff       ..    
    rts                                                               ; a07a: 60          `     
; &a07b referenced 1 time by &ae2a
.sub_ca07b
    ldx #0                                                            ; a07b: a2 00       ..    
    stx l0031                                                         ; a07d: 86 31       .1    
    stx l0032                                                         ; a07f: 86 32       .2    
    stx l0033                                                         ; a081: 86 33       .3    
    stx l0034                                                         ; a083: 86 34       .4    
    stx l0035                                                         ; a085: 86 35       .5    
    stx l0048                                                         ; a087: 86 48       .H    
    stx l0049                                                         ; a089: 86 49       .I    
    cmp #&2e ; '.'                                                    ; a08b: c9 2e       ..    
    beq ca0a0                                                         ; a08d: f0 11       ..    
    cmp #&3a ; ':'                                                    ; a08f: c9 3a       .:    
    bcs ca072                                                         ; a091: b0 df       ..    
    sbc #&2f ; '/'                                                    ; a093: e9 2f       ./    
    bmi ca072                                                         ; a095: 30 db       0.    
    sta l0035                                                         ; a097: 85 35       .5    
; &a099 referenced 8 times by &a0a6, &a0bc, &a0c0, &a0cf, &a0d3, &a0d7, &a0db, &a0df
.ca099
    iny                                                               ; a099: c8          .     
    lda (l0019),y                                                     ; a09a: b1 19       ..    
    cmp #&2e ; '.'                                                    ; a09c: c9 2e       ..    
    bne ca0a8                                                         ; a09e: d0 08       ..    
; &a0a0 referenced 1 time by &a08d
.ca0a0
    lda l0048                                                         ; a0a0: a5 48       .H    
    bne ca0e8                                                         ; a0a2: d0 44       .D    
    inc l0048                                                         ; a0a4: e6 48       .H    
    bne ca099                                                         ; a0a6: d0 f1       ..    
; &a0a8 referenced 1 time by &a09e
.ca0a8
    cmp #&45 ; 'E'                                                    ; a0a8: c9 45       .E    
    beq ca0e1                                                         ; a0aa: f0 35       .5    
    cmp #&3a ; ':'                                                    ; a0ac: c9 3a       .:    
    bcs ca0e8                                                         ; a0ae: b0 38       .8    
    sbc #&2f ; '/'                                                    ; a0b0: e9 2f       ./    
    bcc ca0e8                                                         ; a0b2: 90 34       .4    
    ldx l0031                                                         ; a0b4: a6 31       .1    
    cpx #&18                                                          ; a0b6: e0 18       ..    
    bcc ca0c2                                                         ; a0b8: 90 08       ..    
    ldx l0048                                                         ; a0ba: a6 48       .H    
    bne ca099                                                         ; a0bc: d0 db       ..    
    inc l0049                                                         ; a0be: e6 49       .I    
    bcs ca099                                                         ; a0c0: b0 d7       ..    
; &a0c2 referenced 1 time by &a0b8
.ca0c2
    ldx l0048                                                         ; a0c2: a6 48       .H    
    beq ca0c8                                                         ; a0c4: f0 02       ..    
    dec l0049                                                         ; a0c6: c6 49       .I    
; &a0c8 referenced 1 time by &a0c4
.ca0c8
    jsr sub_ca197                                                     ; a0c8: 20 97 a1     ..   
    adc l0035                                                         ; a0cb: 65 35       e5    
    sta l0035                                                         ; a0cd: 85 35       .5    
    bcc ca099                                                         ; a0cf: 90 c8       ..    
    inc l0034                                                         ; a0d1: e6 34       .4    
    bne ca099                                                         ; a0d3: d0 c4       ..    
    inc l0033                                                         ; a0d5: e6 33       .3    
    bne ca099                                                         ; a0d7: d0 c0       ..    
    inc l0032                                                         ; a0d9: e6 32       .2    
    bne ca099                                                         ; a0db: d0 bc       ..    
    inc l0031                                                         ; a0dd: e6 31       .1    
    bne ca099                                                         ; a0df: d0 b8       ..    
; &a0e1 referenced 1 time by &a0aa
.ca0e1
    jsr sub_ca140                                                     ; a0e1: 20 40 a1     @.   
    adc l0049                                                         ; a0e4: 65 49       eI    
    sta l0049                                                         ; a0e6: 85 49       .I    
; &a0e8 referenced 3 times by &a0a2, &a0ae, &a0b2
.ca0e8
    sty l001b                                                         ; a0e8: 84 1b       ..    
    lda l0049                                                         ; a0ea: a5 49       .I    
    ora l0048                                                         ; a0ec: 05 48       .H    
    beq ca11f                                                         ; a0ee: f0 2f       ./    
    jsr ca1da                                                         ; a0f0: 20 da a1     ..   
    beq ca11b                                                         ; a0f3: f0 26       .&    
; &a0f5 referenced 1 time by &a127
.loop_ca0f5
    lda #&a8                                                          ; a0f5: a9 a8       ..    
    sta l0030                                                         ; a0f7: 85 30       .0    
    lda #0                                                            ; a0f9: a9 00       ..    
    sta l002f                                                         ; a0fb: 85 2f       ./    
    sta l002e                                                         ; a0fd: 85 2e       ..    
    jsr ca303                                                         ; a0ff: 20 03 a3     ..   
    lda l0049                                                         ; a102: a5 49       .I    
    bmi ca111                                                         ; a104: 30 0b       0.    
    beq ca118                                                         ; a106: f0 10       ..    
; &a108 referenced 1 time by &a10d
.loop_ca108
    jsr sub_ca1f4                                                     ; a108: 20 f4 a1     ..   
    dec l0049                                                         ; a10b: c6 49       .I    
    bne loop_ca108                                                    ; a10d: d0 f9       ..    
    beq ca118                                                         ; a10f: f0 07       ..    
; &a111 referenced 2 times by &a104, &a116
.ca111
    jsr sub_ca24d                                                     ; a111: 20 4d a2     M.   
    inc l0049                                                         ; a114: e6 49       .I    
    bne ca111                                                         ; a116: d0 f9       ..    
; &a118 referenced 2 times by &a106, &a10f
.ca118
    jsr ca65c                                                         ; a118: 20 5c a6     \.   
; &a11b referenced 1 time by &a0f3
.ca11b
    sec                                                               ; a11b: 38          8     
    lda #&ff                                                          ; a11c: a9 ff       ..    
    rts                                                               ; a11e: 60          `     
; &a11f referenced 1 time by &a0ee
.ca11f
    lda l0032                                                         ; a11f: a5 32       .2    
    sta l002d                                                         ; a121: 85 2d       .-    
    and #&80                                                          ; a123: 29 80       ).    
    ora l0031                                                         ; a125: 05 31       .1    
    bne loop_ca0f5                                                    ; a127: d0 cc       ..    
    lda l0035                                                         ; a129: a5 35       .5    
    sta l002a                                                         ; a12b: 85 2a       .*    
    lda l0034                                                         ; a12d: a5 34       .4    
    sta l002b                                                         ; a12f: 85 2b       .+    
    lda l0033                                                         ; a131: a5 33       .3    
    sta l002c                                                         ; a133: 85 2c       .,    
    lda #&40 ; '@'                                                    ; a135: a9 40       .@    
    sec                                                               ; a137: 38          8     
    rts                                                               ; a138: 60          `     
; &a139 referenced 1 time by &a145
.loop_ca139
    jsr sub_ca14b                                                     ; a139: 20 4b a1     K.   
    eor #&ff                                                          ; a13c: 49 ff       I.    
    sec                                                               ; a13e: 38          8     
    rts                                                               ; a13f: 60          `     
; &a140 referenced 1 time by &a0e1
.sub_ca140
    iny                                                               ; a140: c8          .     
    lda (l0019),y                                                     ; a141: b1 19       ..    
    cmp #&2d ; '-'                                                    ; a143: c9 2d       .-    
    beq loop_ca139                                                    ; a145: f0 f2       ..    
    cmp #&2b ; '+'                                                    ; a147: c9 2b       .+    
    bne ca14e                                                         ; a149: d0 03       ..    
; &a14b referenced 1 time by &a139
.sub_ca14b
    iny                                                               ; a14b: c8          .     
    lda (l0019),y                                                     ; a14c: b1 19       ..    
; &a14e referenced 1 time by &a149
.ca14e
    cmp #&3a ; ':'                                                    ; a14e: c9 3a       .:    
    bcs ca174                                                         ; a150: b0 22       ."    
    sbc #&2f ; '/'                                                    ; a152: e9 2f       ./    
    bcc ca174                                                         ; a154: 90 1e       ..    
    sta l004a                                                         ; a156: 85 4a       .J    
    iny                                                               ; a158: c8          .     
    lda (l0019),y                                                     ; a159: b1 19       ..    
    cmp #&3a ; ':'                                                    ; a15b: c9 3a       .:    
    bcs ca170                                                         ; a15d: b0 11       ..    
    sbc #&2f ; '/'                                                    ; a15f: e9 2f       ./    
    bcc ca170                                                         ; a161: 90 0d       ..    
    iny                                                               ; a163: c8          .     
    sta l0043                                                         ; a164: 85 43       .C    
    lda l004a                                                         ; a166: a5 4a       .J    
    asl a                                                             ; a168: 0a          .     
    asl a                                                             ; a169: 0a          .     
    adc l004a                                                         ; a16a: 65 4a       eJ    
    asl a                                                             ; a16c: 0a          .     
    adc l0043                                                         ; a16d: 65 43       eC    
    rts                                                               ; a16f: 60          `     
; &a170 referenced 2 times by &a15d, &a161
.ca170
    lda l004a                                                         ; a170: a5 4a       .J    
    clc                                                               ; a172: 18          .     
    rts                                                               ; a173: 60          `     
; &a174 referenced 2 times by &a150, &a154
.ca174
    lda #0                                                            ; a174: a9 00       ..    
    clc                                                               ; a176: 18          .     
    rts                                                               ; a177: 60          `     
; &a178 referenced 2 times by &a208, &a64f
.sub_ca178
    lda l0035                                                         ; a178: a5 35       .5    
    adc l0042                                                         ; a17a: 65 42       eB    
    sta l0035                                                         ; a17c: 85 35       .5    
    lda l0034                                                         ; a17e: a5 34       .4    
    adc l0041                                                         ; a180: 65 41       eA    
    sta l0034                                                         ; a182: 85 34       .4    
    lda l0033                                                         ; a184: a5 33       .3    
    adc l0040                                                         ; a186: 65 40       e@    
    sta l0033                                                         ; a188: 85 33       .3    
    lda l0032                                                         ; a18a: a5 32       .2    
    adc l003f                                                         ; a18c: 65 3f       e?    
    sta l0032                                                         ; a18e: 85 32       .2    
    lda l0031                                                         ; a190: a5 31       .1    
    adc l003e                                                         ; a192: 65 3e       e>    
    sta l0031                                                         ; a194: 85 31       .1    
    rts                                                               ; a196: 60          `     
; &a197 referenced 1 time by &a0c8
.sub_ca197
    pha                                                               ; a197: 48          H     
    ldx l0034                                                         ; a198: a6 34       .4    
    lda l0031                                                         ; a19a: a5 31       .1    
    pha                                                               ; a19c: 48          H     
    lda l0032                                                         ; a19d: a5 32       .2    
    pha                                                               ; a19f: 48          H     
    lda l0033                                                         ; a1a0: a5 33       .3    
    pha                                                               ; a1a2: 48          H     
    lda l0035                                                         ; a1a3: a5 35       .5    
    asl a                                                             ; a1a5: 0a          .     
    rol l0034                                                         ; a1a6: 26 34       &4    
    rol l0033                                                         ; a1a8: 26 33       &3    
    rol l0032                                                         ; a1aa: 26 32       &2    
    rol l0031                                                         ; a1ac: 26 31       &1    
    asl a                                                             ; a1ae: 0a          .     
    rol l0034                                                         ; a1af: 26 34       &4    
    rol l0033                                                         ; a1b1: 26 33       &3    
    rol l0032                                                         ; a1b3: 26 32       &2    
    rol l0031                                                         ; a1b5: 26 31       &1    
    adc l0035                                                         ; a1b7: 65 35       e5    
    sta l0035                                                         ; a1b9: 85 35       .5    
    txa                                                               ; a1bb: 8a          .     
    adc l0034                                                         ; a1bc: 65 34       e4    
    sta l0034                                                         ; a1be: 85 34       .4    
    pla                                                               ; a1c0: 68          h     
    adc l0033                                                         ; a1c1: 65 33       e3    
    sta l0033                                                         ; a1c3: 85 33       .3    
    pla                                                               ; a1c5: 68          h     
    adc l0032                                                         ; a1c6: 65 32       e2    
    sta l0032                                                         ; a1c8: 85 32       .2    
    pla                                                               ; a1ca: 68          h     
    adc l0031                                                         ; a1cb: 65 31       e1    
    asl l0035                                                         ; a1cd: 06 35       .5    
    rol l0034                                                         ; a1cf: 26 34       &4    
    rol l0033                                                         ; a1d1: 26 33       &3    
    rol l0032                                                         ; a1d3: 26 32       &2    
    rol a                                                             ; a1d5: 2a          *     
    sta l0031                                                         ; a1d6: 85 31       .1    
    pla                                                               ; a1d8: 68          h     
    rts                                                               ; a1d9: 60          `     
; &a1da referenced 11 times by &a075, &a0f0, &a405, &a48e, &a50b, &a606, &a6ad, &a6e7, &a801, &ad77, &ad7e
.ca1da
    lda l0031                                                         ; a1da: a5 31       .1    
    ora l0032                                                         ; a1dc: 05 32       .2    
    ora l0033                                                         ; a1de: 05 33       .3    
    ora l0034                                                         ; a1e0: 05 34       .4    
    ora l0035                                                         ; a1e2: 05 35       .5    
    beq ca1ed                                                         ; a1e4: f0 07       ..    
    lda l002e                                                         ; a1e6: a5 2e       ..    
    bne return_14                                                     ; a1e8: d0 09       ..    
    lda #1                                                            ; a1ea: a9 01       ..    
    rts                                                               ; a1ec: 60          `     
; &a1ed referenced 1 time by &a1e4
.ca1ed
    sta l002e                                                         ; a1ed: 85 2e       ..    
    sta l0030                                                         ; a1ef: 85 30       .0    
    sta l002f                                                         ; a1f1: 85 2f       ./    
; &a1f3 referenced 1 time by &a1e8
.return_14
    rts                                                               ; a1f3: 60          `     
; &a1f4 referenced 1 time by &a108
.sub_ca1f4
    clc                                                               ; a1f4: 18          .     
    lda l0030                                                         ; a1f5: a5 30       .0    
    adc #3                                                            ; a1f7: 69 03       i.    
    sta l0030                                                         ; a1f9: 85 30       .0    
    bcc ca1ff                                                         ; a1fb: 90 02       ..    
    inc l002f                                                         ; a1fd: e6 2f       ./    
; &a1ff referenced 1 time by &a1fb
.ca1ff
    jsr sub_ca21e                                                     ; a1ff: 20 1e a2     ..   
    jsr sub_ca242                                                     ; a202: 20 42 a2     B.   
    jsr sub_ca242                                                     ; a205: 20 42 a2     B.   
; &a208 referenced 5 times by &a25b, &a26a, &a284, &a29c, &a5e0
.ca208
    jsr sub_ca178                                                     ; a208: 20 78 a1     x.   
; &a20b referenced 1 time by &a2ba
.ca20b
    bcc return_15                                                     ; a20b: 90 10       ..    
    ror l0031                                                         ; a20d: 66 31       f1    
    ror l0032                                                         ; a20f: 66 32       f2    
    ror l0033                                                         ; a211: 66 33       f3    
    ror l0034                                                         ; a213: 66 34       f4    
    ror l0035                                                         ; a215: 66 35       f5    
    inc l0030                                                         ; a217: e6 30       .0    
    bne return_15                                                     ; a219: d0 02       ..    
    inc l002f                                                         ; a21b: e6 2f       ./    
; &a21d referenced 2 times by &a20b, &a219
.return_15
    rts                                                               ; a21d: 60          `     
; &a21e referenced 5 times by &9a44, &a1ff, &a23f, &a3f8, &a6b2
.sub_ca21e
    lda l002e                                                         ; a21e: a5 2e       ..    
    sta l003b                                                         ; a220: 85 3b       .;    
    lda l002f                                                         ; a222: a5 2f       ./    
    sta l003c                                                         ; a224: 85 3c       .<    
    lda l0030                                                         ; a226: a5 30       .0    
    sta l003d                                                         ; a228: 85 3d       .=    
    lda l0031                                                         ; a22a: a5 31       .1    
    sta l003e                                                         ; a22c: 85 3e       .>    
    lda l0032                                                         ; a22e: a5 32       .2    
    sta l003f                                                         ; a230: 85 3f       .?    
    lda l0033                                                         ; a232: a5 33       .3    
    sta l0040                                                         ; a234: 85 40       .@    
    lda l0034                                                         ; a236: a5 34       .4    
    sta l0041                                                         ; a238: 85 41       .A    
    lda l0035                                                         ; a23a: a5 35       .5    
    sta l0042                                                         ; a23c: 85 42       .B    
    rts                                                               ; a23e: 60          `     
; &a23f referenced 2 times by &a258, &a25e
.sub_ca23f
    jsr sub_ca21e                                                     ; a23f: 20 1e a2     ..   
; &a242 referenced 5 times by &a202, &a205, &a261, &a264, &a267
.sub_ca242
    lsr l003e                                                         ; a242: 46 3e       F>    
    ror l003f                                                         ; a244: 66 3f       f?    
    ror l0040                                                         ; a246: 66 40       f@    
    ror l0041                                                         ; a248: 66 41       fA    
    ror l0042                                                         ; a24a: 66 42       fB    
    rts                                                               ; a24c: 60          `     
; &a24d referenced 1 time by &a111
.sub_ca24d
    sec                                                               ; a24d: 38          8     
    lda l0030                                                         ; a24e: a5 30       .0    
    sbc #4                                                            ; a250: e9 04       ..    
    sta l0030                                                         ; a252: 85 30       .0    
    bcs ca258                                                         ; a254: b0 02       ..    
    dec l002f                                                         ; a256: c6 2f       ./    
; &a258 referenced 1 time by &a254
.ca258
    jsr sub_ca23f                                                     ; a258: 20 3f a2     ?.   
    jsr ca208                                                         ; a25b: 20 08 a2     ..   
    jsr sub_ca23f                                                     ; a25e: 20 3f a2     ?.   
    jsr sub_ca242                                                     ; a261: 20 42 a2     B.   
    jsr sub_ca242                                                     ; a264: 20 42 a2     B.   
    jsr sub_ca242                                                     ; a267: 20 42 a2     B.   
    jsr ca208                                                         ; a26a: 20 08 a2     ..   
    lda #0                                                            ; a26d: a9 00       ..    
    sta l003e                                                         ; a26f: 85 3e       .>    
    lda l0031                                                         ; a271: a5 31       .1    
    sta l003f                                                         ; a273: 85 3f       .?    
    lda l0032                                                         ; a275: a5 32       .2    
    sta l0040                                                         ; a277: 85 40       .@    
    lda l0033                                                         ; a279: a5 33       .3    
    sta l0041                                                         ; a27b: 85 41       .A    
    lda l0034                                                         ; a27d: a5 34       .4    
    sta l0042                                                         ; a27f: 85 42       .B    
    lda l0035                                                         ; a281: a5 35       .5    
    rol a                                                             ; a283: 2a          *     
    jsr ca208                                                         ; a284: 20 08 a2     ..   
    lda #0                                                            ; a287: a9 00       ..    
    sta l003e                                                         ; a289: 85 3e       .>    
    sta l003f                                                         ; a28b: 85 3f       .?    
    lda l0031                                                         ; a28d: a5 31       .1    
    sta l0040                                                         ; a28f: 85 40       .@    
    lda l0032                                                         ; a291: a5 32       .2    
    sta l0041                                                         ; a293: 85 41       .A    
    lda l0033                                                         ; a295: a5 33       .3    
    sta l0042                                                         ; a297: 85 42       .B    
    lda l0034                                                         ; a299: a5 34       .4    
    rol a                                                             ; a29b: 2a          *     
    jsr ca208                                                         ; a29c: 20 08 a2     ..   
    lda l0032                                                         ; a29f: a5 32       .2    
    rol a                                                             ; a2a1: 2a          *     
    lda l0031                                                         ; a2a2: a5 31       .1    
; &a2a4 referenced 1 time by &a666
.sub_ca2a4
    adc l0035                                                         ; a2a4: 65 35       e5    
    sta l0035                                                         ; a2a6: 85 35       .5    
    bcc return_16                                                     ; a2a8: 90 13       ..    
    inc l0034                                                         ; a2aa: e6 34       .4    
    bne return_16                                                     ; a2ac: d0 0f       ..    
    inc l0033                                                         ; a2ae: e6 33       .3    
    bne return_16                                                     ; a2b0: d0 0b       ..    
    inc l0032                                                         ; a2b2: e6 32       .2    
    bne return_16                                                     ; a2b4: d0 07       ..    
    inc l0031                                                         ; a2b6: e6 31       .1    
    bne return_16                                                     ; a2b8: d0 03       ..    
    jmp ca20b                                                         ; a2ba: 4c 0b a2    L..   
; &a2bd referenced 5 times by &a2a8, &a2ac, &a2b0, &a2b4, &a2b8
.return_16
    rts                                                               ; a2bd: 60          `     
; &a2be referenced 10 times by &9301, &9a41, &9c98, &9caf, &9cee, &9d02, &9d0e, &9d17, &9d1d, &b4e6
.ca2be
    ldx #0                                                            ; a2be: a2 00       ..    
    stx l0035                                                         ; a2c0: 86 35       .5    
    stx l002f                                                         ; a2c2: 86 2f       ./    
    lda l002d                                                         ; a2c4: a5 2d       .-    
    bpl ca2cd                                                         ; a2c6: 10 05       ..    
    jsr cad93                                                         ; a2c8: 20 93 ad     ..   
    ldx #&ff                                                          ; a2cb: a2 ff       ..    
; &a2cd referenced 1 time by &a2c6
.ca2cd
    stx l002e                                                         ; a2cd: 86 2e       ..    
    lda l002a                                                         ; a2cf: a5 2a       .*    
    sta l0034                                                         ; a2d1: 85 34       .4    
    lda l002b                                                         ; a2d3: a5 2b       .+    
    sta l0033                                                         ; a2d5: 85 33       .3    
    lda l002c                                                         ; a2d7: a5 2c       .,    
    sta l0032                                                         ; a2d9: 85 32       .2    
    lda l002d                                                         ; a2db: a5 2d       .-    
    sta l0031                                                         ; a2dd: 85 31       .1    
    lda #&a0                                                          ; a2df: a9 a0       ..    
    sta l0030                                                         ; a2e1: 85 30       .0    
    jmp ca303                                                         ; a2e3: 4c 03 a3    L..   
; &a2e6 referenced 1 time by &a30f
.loop_ca2e6
    sta l002e                                                         ; a2e6: 85 2e       ..    
    sta l0030                                                         ; a2e8: 85 30       .0    
    sta l002f                                                         ; a2ea: 85 2f       ./    
; &a2ec referenced 4 times by &a2f2, &a305, &a315, &a338
.return_17
    rts                                                               ; a2ec: 60          `     
; &a2ed referenced 1 time by &a852
.sub_ca2ed
    pha                                                               ; a2ed: 48          H     
    jsr ca686                                                         ; a2ee: 20 86 a6     ..   
    pla                                                               ; a2f1: 68          h     
    beq return_17                                                     ; a2f2: f0 f8       ..    
    bpl ca2fd                                                         ; a2f4: 10 07       ..    
    sta l002e                                                         ; a2f6: 85 2e       ..    
    lda #0                                                            ; a2f8: a9 00       ..    
    sec                                                               ; a2fa: 38          8     
    sbc l002e                                                         ; a2fb: e5 2e       ..    
; &a2fd referenced 1 time by &a2f4
.ca2fd
    sta l0031                                                         ; a2fd: 85 31       .1    
    lda #&88                                                          ; a2ff: a9 88       ..    
    sta l0030                                                         ; a301: 85 30       .0    
; &a303 referenced 6 times by &a0ff, &a2e3, &a4b3, &a5dc, &a602, &a659
.ca303
    lda l0031                                                         ; a303: a5 31       .1    
    bmi return_17                                                     ; a305: 30 e5       0.    
    ora l0032                                                         ; a307: 05 32       .2    
    ora l0033                                                         ; a309: 05 33       .3    
    ora l0034                                                         ; a30b: 05 34       .4    
    ora l0035                                                         ; a30d: 05 35       .5    
    beq loop_ca2e6                                                    ; a30f: f0 d5       ..    
    lda l0030                                                         ; a311: a5 30       .0    
; &a313 referenced 2 times by &a330, &a334
.ca313
    ldy l0031                                                         ; a313: a4 31       .1    
    bmi return_17                                                     ; a315: 30 d5       0.    
    bne ca33a                                                         ; a317: d0 21       .!    
    ldx l0032                                                         ; a319: a6 32       .2    
    stx l0031                                                         ; a31b: 86 31       .1    
    ldx l0033                                                         ; a31d: a6 33       .3    
    stx l0032                                                         ; a31f: 86 32       .2    
    ldx l0034                                                         ; a321: a6 34       .4    
    stx l0033                                                         ; a323: 86 33       .3    
    ldx l0035                                                         ; a325: a6 35       .5    
    stx l0034                                                         ; a327: 86 34       .4    
    sty l0035                                                         ; a329: 84 35       .5    
    sec                                                               ; a32b: 38          8     
    sbc #8                                                            ; a32c: e9 08       ..    
    sta l0030                                                         ; a32e: 85 30       .0    
    bcs ca313                                                         ; a330: b0 e1       ..    
    dec l002f                                                         ; a332: c6 2f       ./    
    bcc ca313                                                         ; a334: 90 dd       ..    
; &a336 referenced 2 times by &a348, &a34c
.ca336
    ldy l0031                                                         ; a336: a4 31       .1    
    bmi return_17                                                     ; a338: 30 b2       0.    
; &a33a referenced 1 time by &a317
.ca33a
    asl l0035                                                         ; a33a: 06 35       .5    
    rol l0034                                                         ; a33c: 26 34       &4    
    rol l0033                                                         ; a33e: 26 33       &3    
    rol l0032                                                         ; a340: 26 32       &2    
    rol l0031                                                         ; a342: 26 31       &1    
    sbc #0                                                            ; a344: e9 00       ..    
    sta l0030                                                         ; a346: 85 30       .0    
    bcs ca336                                                         ; a348: b0 ec       ..    
    dec l002f                                                         ; a34a: c6 2f       ./    
    bcc ca336                                                         ; a34c: 90 e8       ..    
; &a34e referenced 4 times by &9a5f, &a500, &a60b, &a6ec
.sub_ca34e
    ldy #4                                                            ; a34e: a0 04       ..    
    lda (l004b),y                                                     ; a350: b1 4b       .K    
    sta l0041                                                         ; a352: 85 41       .A    
    dey                                                               ; a354: 88          .     
    lda (l004b),y                                                     ; a355: b1 4b       .K    
    sta l0040                                                         ; a357: 85 40       .@    
    dey                                                               ; a359: 88          .     
    lda (l004b),y                                                     ; a35a: b1 4b       .K    
    sta l003f                                                         ; a35c: 85 3f       .?    
    dey                                                               ; a35e: 88          .     
    lda (l004b),y                                                     ; a35f: b1 4b       .K    
    sta l003b                                                         ; a361: 85 3b       .;    
    dey                                                               ; a363: 88          .     
    sty l0042                                                         ; a364: 84 42       .B    
    sty l003c                                                         ; a366: 84 3c       .<    
    lda (l004b),y                                                     ; a368: b1 4b       .K    
    sta l003d                                                         ; a36a: 85 3d       .=    
    ora l003b                                                         ; a36c: 05 3b       .;    
    ora l003f                                                         ; a36e: 05 3f       .?    
    ora l0040                                                         ; a370: 05 40       .@    
    ora l0041                                                         ; a372: 05 41       .A    
    beq ca37a                                                         ; a374: f0 04       ..    
    lda l003b                                                         ; a376: a5 3b       .;    
    ora #&80                                                          ; a378: 09 80       ..    
; &a37a referenced 1 time by &a374
.ca37a
    sta l003e                                                         ; a37a: 85 3e       .>    
    rts                                                               ; a37c: 60          `     
; &a37d referenced 1 time by &9e6c
.sub_ca37d
    lda #&71 ; 'q'                                                    ; a37d: a9 71       .q    
    bne ca387                                                         ; a37f: d0 06       ..    
; &a381 referenced 3 times by &9e59, &9e88, &aabe
.sub_ca381
    lda #&76 ; 'v'                                                    ; a381: a9 76       .v    
    bne ca387                                                         ; a383: d0 02       ..    
; &a385 referenced 4 times by &a6a5, &a84b, &a89b, &ab1f
.sub_ca385
    lda #&6c ; 'l'                                                    ; a385: a9 6c       .l    
; &a387 referenced 3 times by &a37f, &a383, &a835
.ca387
    sta l004b                                                         ; a387: 85 4b       .K    
    lda #4                                                            ; a389: a9 04       ..    
    sta l004c                                                         ; a38b: 85 4c       .L    
    ldy #0                                                            ; a38d: a0 00       ..    
    lda l0030                                                         ; a38f: a5 30       .0    
    sta (l004b),y                                                     ; a391: 91 4b       .K    
    iny                                                               ; a393: c8          .     
    lda l002e                                                         ; a394: a5 2e       ..    
    and #&80                                                          ; a396: 29 80       ).    
    sta l002e                                                         ; a398: 85 2e       ..    
    lda l0031                                                         ; a39a: a5 31       .1    
    and #&7f                                                          ; a39c: 29 7f       ).    
    ora l002e                                                         ; a39e: 05 2e       ..    
    sta (l004b),y                                                     ; a3a0: 91 4b       .K    
    lda l0032                                                         ; a3a2: a5 32       .2    
    iny                                                               ; a3a4: c8          .     
    sta (l004b),y                                                     ; a3a5: 91 4b       .K    
    lda l0033                                                         ; a3a7: a5 33       .3    
    iny                                                               ; a3a9: c8          .     
    sta (l004b),y                                                     ; a3aa: 91 4b       .K    
    lda l0034                                                         ; a3ac: a5 34       .4    
    iny                                                               ; a3ae: c8          .     
    sta (l004b),y                                                     ; a3af: 91 4b       .K    
    rts                                                               ; a3b1: 60          `     
    equb &20, &f5, &a7                                                ; a3b2: 20 f5 a7     ..   
; &a3b5 referenced 7 times by &9a4a, &9e4d, &9e64, &9e72, &a6b5, &a8b2, &aac9
.sub_ca3b5
    ldy #4                                                            ; a3b5: a0 04       ..    
    lda (l004b),y                                                     ; a3b7: b1 4b       .K    
    sta l0034                                                         ; a3b9: 85 34       .4    
    dey                                                               ; a3bb: 88          .     
    lda (l004b),y                                                     ; a3bc: b1 4b       .K    
    sta l0033                                                         ; a3be: 85 33       .3    
    dey                                                               ; a3c0: 88          .     
    lda (l004b),y                                                     ; a3c1: b1 4b       .K    
    sta l0032                                                         ; a3c3: 85 32       .2    
    dey                                                               ; a3c5: 88          .     
    lda (l004b),y                                                     ; a3c6: b1 4b       .K    
    sta l002e                                                         ; a3c8: 85 2e       ..    
    dey                                                               ; a3ca: 88          .     
    lda (l004b),y                                                     ; a3cb: b1 4b       .K    
    sta l0030                                                         ; a3cd: 85 30       .0    
    sty l0035                                                         ; a3cf: 84 35       .5    
    sty l002f                                                         ; a3d1: 84 2f       ./    
    ora l002e                                                         ; a3d3: 05 2e       ..    
    ora l0032                                                         ; a3d5: 05 32       .2    
    ora l0033                                                         ; a3d7: 05 33       .3    
    ora l0034                                                         ; a3d9: 05 34       .4    
    beq ca3e1                                                         ; a3db: f0 04       ..    
    lda l002e                                                         ; a3dd: a5 2e       ..    
    ora #&80                                                          ; a3df: 09 80       ..    
; &a3e1 referenced 1 time by &a3db
.ca3e1
    sta l0031                                                         ; a3e1: 85 31       .1    
    rts                                                               ; a3e3: 60          `     
; &a3e4 referenced 3 times by &92f4, &9e93, &b4c3
.ca3e4
    jsr sub_ca3fe                                                     ; a3e4: 20 fe a3     ..   
    lda l0031                                                         ; a3e7: a5 31       .1    
    sta l002d                                                         ; a3e9: 85 2d       .-    
    lda l0032                                                         ; a3eb: a5 32       .2    
    sta l002c                                                         ; a3ed: 85 2c       .,    
    lda l0033                                                         ; a3ef: a5 33       .3    
    sta l002b                                                         ; a3f1: 85 2b       .+    
    lda l0034                                                         ; a3f3: a5 34       .4    
    sta l002a                                                         ; a3f5: 85 2a       .*    
    rts                                                               ; a3f7: 60          `     
; &a3f8 referenced 1 time by &a400
.loop_ca3f8
    jsr sub_ca21e                                                     ; a3f8: 20 1e a2     ..   
    jmp ca686                                                         ; a3fb: 4c 86 a6    L..   
; &a3fe referenced 2 times by &a3e4, &a491
.sub_ca3fe
    lda l0030                                                         ; a3fe: a5 30       .0    
    bpl loop_ca3f8                                                    ; a400: 10 f6       ..    
    jsr sub_ca453                                                     ; a402: 20 53 a4     S.   
    jsr ca1da                                                         ; a405: 20 da a1     ..   
    bne ca43c                                                         ; a408: d0 32       .2    
    beq ca468                                                         ; a40a: f0 5c       .\    
; &a40c referenced 2 times by &a43a, &a44e
.ca40c
    lda l0030                                                         ; a40c: a5 30       .0    
    cmp #&a0                                                          ; a40e: c9 a0       ..    
    bcs ca466                                                         ; a410: b0 54       .T    
    cmp #&99                                                          ; a412: c9 99       ..    
    bcs ca43c                                                         ; a414: b0 26       .&    
    adc #8                                                            ; a416: 69 08       i.    
    sta l0030                                                         ; a418: 85 30       .0    
    lda l0040                                                         ; a41a: a5 40       .@    
    sta l0041                                                         ; a41c: 85 41       .A    
    lda l003f                                                         ; a41e: a5 3f       .?    
    sta l0040                                                         ; a420: 85 40       .@    
    lda l003e                                                         ; a422: a5 3e       .>    
    sta l003f                                                         ; a424: 85 3f       .?    
    lda l0034                                                         ; a426: a5 34       .4    
    sta l003e                                                         ; a428: 85 3e       .>    
    lda l0033                                                         ; a42a: a5 33       .3    
    sta l0034                                                         ; a42c: 85 34       .4    
    lda l0032                                                         ; a42e: a5 32       .2    
    sta l0033                                                         ; a430: 85 33       .3    
    lda l0031                                                         ; a432: a5 31       .1    
    sta l0032                                                         ; a434: 85 32       .2    
    lda #0                                                            ; a436: a9 00       ..    
    sta l0031                                                         ; a438: 85 31       .1    
    beq ca40c                                                         ; a43a: f0 d0       ..    
; &a43c referenced 2 times by &a408, &a414
.ca43c
    lsr l0031                                                         ; a43c: 46 31       F1    
    ror l0032                                                         ; a43e: 66 32       f2    
    ror l0033                                                         ; a440: 66 33       f3    
    ror l0034                                                         ; a442: 66 34       f4    
    ror l003e                                                         ; a444: 66 3e       f>    
    ror l003f                                                         ; a446: 66 3f       f?    
    ror l0040                                                         ; a448: 66 40       f@    
    ror l0041                                                         ; a44a: 66 41       fA    
    inc l0030                                                         ; a44c: e6 30       .0    
    bne ca40c                                                         ; a44e: d0 bc       ..    
; &a450 referenced 1 time by &a466
.loop_ca450
    jmp ca66c                                                         ; a450: 4c 6c a6    Ll.   
; &a453 referenced 2 times by &a402, &a814
.sub_ca453
    lda #0                                                            ; a453: a9 00       ..    
    sta l003b                                                         ; a455: 85 3b       .;    
    sta l003c                                                         ; a457: 85 3c       .<    
    sta l003d                                                         ; a459: 85 3d       .=    
    sta l003e                                                         ; a45b: 85 3e       .>    
    sta l003f                                                         ; a45d: 85 3f       .?    
    sta l0040                                                         ; a45f: 85 40       .@    
    sta l0041                                                         ; a461: 85 41       .A    
    sta l0042                                                         ; a463: 85 42       .B    
    rts                                                               ; a465: 60          `     
; &a466 referenced 1 time by &a410
.ca466
    bne loop_ca450                                                    ; a466: d0 e8       ..    
; &a468 referenced 1 time by &a40a
.ca468
    lda l002e                                                         ; a468: a5 2e       ..    
    bpl return_18                                                     ; a46a: 10 19       ..    
; &a46c referenced 1 time by &a4b0
.sub_ca46c
    sec                                                               ; a46c: 38          8     
    lda #0                                                            ; a46d: a9 00       ..    
    sbc l0034                                                         ; a46f: e5 34       .4    
    sta l0034                                                         ; a471: 85 34       .4    
    lda #0                                                            ; a473: a9 00       ..    
    sbc l0033                                                         ; a475: e5 33       .3    
    sta l0033                                                         ; a477: 85 33       .3    
    lda #0                                                            ; a479: a9 00       ..    
    sbc l0032                                                         ; a47b: e5 32       .2    
    sta l0032                                                         ; a47d: 85 32       .2    
    lda #0                                                            ; a47f: a9 00       ..    
    sbc l0031                                                         ; a481: e5 31       .1    
    sta l0031                                                         ; a483: 85 31       .1    
; &a485 referenced 1 time by &a46a
.return_18
    rts                                                               ; a485: 60          `     
; &a486 referenced 2 times by &9e45, &aab8
.sub_ca486
    lda l0030                                                         ; a486: a5 30       .0    
    bmi ca491                                                         ; a488: 30 07       0.    
    lda #0                                                            ; a48a: a9 00       ..    
    sta l004a                                                         ; a48c: 85 4a       .J    
    jmp ca1da                                                         ; a48e: 4c da a1    L..   
; &a491 referenced 1 time by &a488
.ca491
    jsr sub_ca3fe                                                     ; a491: 20 fe a3     ..   
    lda l0034                                                         ; a494: a5 34       .4    
    sta l004a                                                         ; a496: 85 4a       .J    
    jsr sub_ca4e8                                                     ; a498: 20 e8 a4     ..   
    lda #&80                                                          ; a49b: a9 80       ..    
    sta l0030                                                         ; a49d: 85 30       .0    
    ldx l0031                                                         ; a49f: a6 31       .1    
    bpl ca4b3                                                         ; a4a1: 10 10       ..    
    eor l002e                                                         ; a4a3: 45 2e       E.    
    sta l002e                                                         ; a4a5: 85 2e       ..    
    bpl ca4ae                                                         ; a4a7: 10 05       ..    
    inc l004a                                                         ; a4a9: e6 4a       .J    
    jmp ca4b0                                                         ; a4ab: 4c b0 a4    L..   
; &a4ae referenced 1 time by &a4a7
.ca4ae
    dec l004a                                                         ; a4ae: c6 4a       .J    
; &a4b0 referenced 1 time by &a4ab
.ca4b0
    jsr sub_ca46c                                                     ; a4b0: 20 6c a4     l.   
; &a4b3 referenced 1 time by &a4a1
.ca4b3
    jmp ca303                                                         ; a4b3: 4c 03 a3    L..   
    equb &e6, &34, &d0, &0c, &e6, &33, &d0, &08, &e6, &32, &d0, &04   ; a4b6: e6 34 d0... .4....
    equb &e6, &31, &f0, &8a                                           ; a4c2: e6 31 f0... .1....
    equs "` l"                                                        ; a4c6: 60 20 6c    ` l   
    equb &a4, &20, &b6, &a4, &4c, &6c, &a4                            ; a4c9: a4 20 b6... . ....
; &a4d0 referenced 1 time by &9d08
.sub_ca4d0
    jsr sub_ca4fd                                                     ; a4d0: 20 fd a4     ..   
    jmp cad7e                                                         ; a4d3: 4c 7e ad    L~.   
    equb &20, &4e, &a3, &20, &8d, &a3                                 ; a4d6: 20 4e a3...  N....
; &a4dc referenced 2 times by &a50e, &a559
.ca4dc
    lda l003b                                                         ; a4dc: a5 3b       .;    
    sta l002e                                                         ; a4de: 85 2e       ..    
    lda l003c                                                         ; a4e0: a5 3c       .<    
    sta l002f                                                         ; a4e2: 85 2f       ./    
    lda l003d                                                         ; a4e4: a5 3d       .=    
    sta l0030                                                         ; a4e6: 85 30       .0    
; &a4e8 referenced 1 time by &a498
.sub_ca4e8
    lda l003e                                                         ; a4e8: a5 3e       .>    
    sta l0031                                                         ; a4ea: 85 31       .1    
    lda l003f                                                         ; a4ec: a5 3f       .?    
    sta l0032                                                         ; a4ee: 85 32       .2    
    lda l0040                                                         ; a4f0: a5 40       .@    
    sta l0033                                                         ; a4f2: 85 33       .3    
    lda l0041                                                         ; a4f4: a5 41       .A    
    sta l0034                                                         ; a4f6: 85 34       .4    
    lda l0042                                                         ; a4f8: a5 42       .B    
    sta l0035                                                         ; a4fa: 85 35       .5    
; &a4fc referenced 2 times by &a503, &a51d
.return_19
    rts                                                               ; a4fc: 60          `     
; &a4fd referenced 2 times by &9cf4, &a4d0
.sub_ca4fd
    jsr cad7e                                                         ; a4fd: 20 7e ad     ~.   
; &a500 referenced 4 times by &9c9e, &a848, &a863, &a8cc
.sub_ca500
    jsr sub_ca34e                                                     ; a500: 20 4e a3     N.   
    beq return_19                                                     ; a503: f0 f7       ..    
; &a505 referenced 1 time by &a830
.sub_ca505
    jsr sub_ca50b                                                     ; a505: 20 0b a5     ..   
    jmp ca65c                                                         ; a508: 4c 5c a6    L\.   
; &a50b referenced 1 time by &a505
.sub_ca50b
    jsr ca1da                                                         ; a50b: 20 da a1     ..   
    beq ca4dc                                                         ; a50e: f0 cc       ..    
    ldy #0                                                            ; a510: a0 00       ..    
    sec                                                               ; a512: 38          8     
    lda l0030                                                         ; a513: a5 30       .0    
    sbc l003d                                                         ; a515: e5 3d       .=    
    beq ca590                                                         ; a517: f0 77       .w    
    bcc ca552                                                         ; a519: 90 37       .7    
    cmp #&25 ; '%'                                                    ; a51b: c9 25       .%    
    bcs return_19                                                     ; a51d: b0 dd       ..    
    pha                                                               ; a51f: 48          H     
    and #&38 ; '8'                                                    ; a520: 29 38       )8    
    beq ca53d                                                         ; a522: f0 19       ..    
    lsr a                                                             ; a524: 4a          J     
    lsr a                                                             ; a525: 4a          J     
    lsr a                                                             ; a526: 4a          J     
    tax                                                               ; a527: aa          .     
; &a528 referenced 1 time by &a53b
.loop_ca528
    lda l0041                                                         ; a528: a5 41       .A    
    sta l0042                                                         ; a52a: 85 42       .B    
    lda l0040                                                         ; a52c: a5 40       .@    
    sta l0041                                                         ; a52e: 85 41       .A    
    lda l003f                                                         ; a530: a5 3f       .?    
    sta l0040                                                         ; a532: 85 40       .@    
    lda l003e                                                         ; a534: a5 3e       .>    
    sta l003f                                                         ; a536: 85 3f       .?    
    sty l003e                                                         ; a538: 84 3e       .>    
    dex                                                               ; a53a: ca          .     
    bne loop_ca528                                                    ; a53b: d0 eb       ..    
; &a53d referenced 1 time by &a522
.ca53d
    pla                                                               ; a53d: 68          h     
    and #7                                                            ; a53e: 29 07       ).    
    beq ca590                                                         ; a540: f0 4e       .N    
    tax                                                               ; a542: aa          .     
; &a543 referenced 1 time by &a54e
.loop_ca543
    lsr l003e                                                         ; a543: 46 3e       F>    
    ror l003f                                                         ; a545: 66 3f       f?    
    ror l0040                                                         ; a547: 66 40       f@    
    ror l0041                                                         ; a549: 66 41       fA    
    ror l0042                                                         ; a54b: 66 42       fB    
    dex                                                               ; a54d: ca          .     
    bne loop_ca543                                                    ; a54e: d0 f3       ..    
    beq ca590                                                         ; a550: f0 3e       .>    
; &a552 referenced 1 time by &a519
.ca552
    sec                                                               ; a552: 38          8     
    lda l003d                                                         ; a553: a5 3d       .=    
    sbc l0030                                                         ; a555: e5 30       .0    
    cmp #&25 ; '%'                                                    ; a557: c9 25       .%    
    bcs ca4dc                                                         ; a559: b0 81       ..    
    pha                                                               ; a55b: 48          H     
    and #&38 ; '8'                                                    ; a55c: 29 38       )8    
    beq ca579                                                         ; a55e: f0 19       ..    
    lsr a                                                             ; a560: 4a          J     
    lsr a                                                             ; a561: 4a          J     
    lsr a                                                             ; a562: 4a          J     
    tax                                                               ; a563: aa          .     
; &a564 referenced 1 time by &a577
.loop_ca564
    lda l0034                                                         ; a564: a5 34       .4    
    sta l0035                                                         ; a566: 85 35       .5    
    lda l0033                                                         ; a568: a5 33       .3    
    sta l0034                                                         ; a56a: 85 34       .4    
    lda l0032                                                         ; a56c: a5 32       .2    
    sta l0033                                                         ; a56e: 85 33       .3    
    lda l0031                                                         ; a570: a5 31       .1    
    sta l0032                                                         ; a572: 85 32       .2    
    sty l0031                                                         ; a574: 84 31       .1    
    dex                                                               ; a576: ca          .     
    bne loop_ca564                                                    ; a577: d0 eb       ..    
; &a579 referenced 1 time by &a55e
.ca579
    pla                                                               ; a579: 68          h     
    and #7                                                            ; a57a: 29 07       ).    
    beq ca58c                                                         ; a57c: f0 0e       ..    
    tax                                                               ; a57e: aa          .     
; &a57f referenced 1 time by &a58a
.loop_ca57f
    lsr l0031                                                         ; a57f: 46 31       F1    
    ror l0032                                                         ; a581: 66 32       f2    
    ror l0033                                                         ; a583: 66 33       f3    
    ror l0034                                                         ; a585: 66 34       f4    
    ror l0035                                                         ; a587: 66 35       f5    
    dex                                                               ; a589: ca          .     
    bne loop_ca57f                                                    ; a58a: d0 f3       ..    
; &a58c referenced 1 time by &a57c
.ca58c
    lda l003d                                                         ; a58c: a5 3d       .=    
    sta l0030                                                         ; a58e: 85 30       .0    
; &a590 referenced 3 times by &a517, &a540, &a550
.ca590
    lda l002e                                                         ; a590: a5 2e       ..    
    eor l003b                                                         ; a592: 45 3b       E;    
    bpl ca5df                                                         ; a594: 10 49       .I    
    lda l0031                                                         ; a596: a5 31       .1    
    cmp l003e                                                         ; a598: c5 3e       .>    
    bne ca5b7                                                         ; a59a: d0 1b       ..    
    lda l0032                                                         ; a59c: a5 32       .2    
    cmp l003f                                                         ; a59e: c5 3f       .?    
    bne ca5b7                                                         ; a5a0: d0 15       ..    
    lda l0033                                                         ; a5a2: a5 33       .3    
    cmp l0040                                                         ; a5a4: c5 40       .@    
    bne ca5b7                                                         ; a5a6: d0 0f       ..    
    lda l0034                                                         ; a5a8: a5 34       .4    
    cmp l0041                                                         ; a5aa: c5 41       .A    
    bne ca5b7                                                         ; a5ac: d0 09       ..    
    lda l0035                                                         ; a5ae: a5 35       .5    
    cmp l0042                                                         ; a5b0: c5 42       .B    
    bne ca5b7                                                         ; a5b2: d0 03       ..    
    jmp ca686                                                         ; a5b4: 4c 86 a6    L..   
; &a5b7 referenced 5 times by &a59a, &a5a0, &a5a6, &a5ac, &a5b2
.ca5b7
    bcs ca5e3                                                         ; a5b7: b0 2a       .*    
    sec                                                               ; a5b9: 38          8     
    lda l0042                                                         ; a5ba: a5 42       .B    
    sbc l0035                                                         ; a5bc: e5 35       .5    
    sta l0035                                                         ; a5be: 85 35       .5    
    lda l0041                                                         ; a5c0: a5 41       .A    
    sbc l0034                                                         ; a5c2: e5 34       .4    
    sta l0034                                                         ; a5c4: 85 34       .4    
    lda l0040                                                         ; a5c6: a5 40       .@    
    sbc l0033                                                         ; a5c8: e5 33       .3    
    sta l0033                                                         ; a5ca: 85 33       .3    
    lda l003f                                                         ; a5cc: a5 3f       .?    
    sbc l0032                                                         ; a5ce: e5 32       .2    
    sta l0032                                                         ; a5d0: 85 32       .2    
    lda l003e                                                         ; a5d2: a5 3e       .>    
    sbc l0031                                                         ; a5d4: e5 31       .1    
    sta l0031                                                         ; a5d6: 85 31       .1    
    lda l003b                                                         ; a5d8: a5 3b       .;    
    sta l002e                                                         ; a5da: 85 2e       ..    
    jmp ca303                                                         ; a5dc: 4c 03 a3    L..   
; &a5df referenced 1 time by &a594
.ca5df
    clc                                                               ; a5df: 18          .     
    jmp ca208                                                         ; a5e0: 4c 08 a2    L..   
; &a5e3 referenced 1 time by &a5b7
.ca5e3
    sec                                                               ; a5e3: 38          8     
    lda l0035                                                         ; a5e4: a5 35       .5    
    sbc l0042                                                         ; a5e6: e5 42       .B    
    sta l0035                                                         ; a5e8: 85 35       .5    
    lda l0034                                                         ; a5ea: a5 34       .4    
    sbc l0041                                                         ; a5ec: e5 41       .A    
    sta l0034                                                         ; a5ee: 85 34       .4    
    lda l0033                                                         ; a5f0: a5 33       .3    
    sbc l0040                                                         ; a5f2: e5 40       .@    
    sta l0033                                                         ; a5f4: 85 33       .3    
    lda l0032                                                         ; a5f6: a5 32       .2    
    sbc l003f                                                         ; a5f8: e5 3f       .?    
    sta l0032                                                         ; a5fa: 85 32       .2    
    lda l0031                                                         ; a5fc: a5 31       .1    
    sbc l003e                                                         ; a5fe: e5 3e       .>    
    sta l0031                                                         ; a600: 85 31       .1    
    jmp ca303                                                         ; a602: 4c 03 a3    L..   
; &a605 referenced 1 time by &a609
.return_20
    rts                                                               ; a605: 60          `     
; &a606 referenced 1 time by &a656
.sub_ca606
    jsr ca1da                                                         ; a606: 20 da a1     ..   
    beq return_20                                                     ; a609: f0 fa       ..    
    jsr sub_ca34e                                                     ; a60b: 20 4e a3     N.   
    bne ca613                                                         ; a60e: d0 03       ..    
    jmp ca686                                                         ; a610: 4c 86 a6    L..   
; &a613 referenced 1 time by &a60e
.ca613
    clc                                                               ; a613: 18          .     
    lda l0030                                                         ; a614: a5 30       .0    
    adc l003d                                                         ; a616: 65 3d       e=    
    bcc ca61d                                                         ; a618: 90 03       ..    
    inc l002f                                                         ; a61a: e6 2f       ./    
    clc                                                               ; a61c: 18          .     
; &a61d referenced 1 time by &a618
.ca61d
    sbc #&7f                                                          ; a61d: e9 7f       ..    
    sta l0030                                                         ; a61f: 85 30       .0    
    bcs ca625                                                         ; a621: b0 02       ..    
    dec l002f                                                         ; a623: c6 2f       ./    
; &a625 referenced 1 time by &a621
.ca625
    ldx #5                                                            ; a625: a2 05       ..    
    ldy #0                                                            ; a627: a0 00       ..    
; &a629 referenced 1 time by &a630
.loop_ca629
    lda l0030,x                                                       ; a629: b5 30       .0    
    sta l0042,x                                                       ; a62b: 95 42       .B    
    sty l0030,x                                                       ; a62d: 94 30       .0    
    dex                                                               ; a62f: ca          .     
    bne loop_ca629                                                    ; a630: d0 f7       ..    
    lda l002e                                                         ; a632: a5 2e       ..    
    eor l003b                                                         ; a634: 45 3b       E;    
    sta l002e                                                         ; a636: 85 2e       ..    
    ldy #&20 ; ' '                                                    ; a638: a0 20       .     
; &a63a referenced 1 time by &a653
.loop_ca63a
    lsr l003e                                                         ; a63a: 46 3e       F>    
    ror l003f                                                         ; a63c: 66 3f       f?    
    ror l0040                                                         ; a63e: 66 40       f@    
    ror l0041                                                         ; a640: 66 41       fA    
    ror l0042                                                         ; a642: 66 42       fB    
    asl l0046                                                         ; a644: 06 46       .F    
    rol l0045                                                         ; a646: 26 45       &E    
    rol l0044                                                         ; a648: 26 44       &D    
    rol l0043                                                         ; a64a: 26 43       &C    
    bcc ca652                                                         ; a64c: 90 04       ..    
    clc                                                               ; a64e: 18          .     
    jsr sub_ca178                                                     ; a64f: 20 78 a1     x.   
; &a652 referenced 1 time by &a64c
.ca652
    dey                                                               ; a652: 88          .     
    bne loop_ca63a                                                    ; a653: d0 e5       ..    
    rts                                                               ; a655: 60          `     
; &a656 referenced 7 times by &9d2f, &9e81, &a842, &a845, &a85d, &aad4, &ab2c
.sub_ca656
    jsr sub_ca606                                                     ; a656: 20 06 a6     ..   
; &a659 referenced 1 time by &a7a6
.ca659
    jsr ca303                                                         ; a659: 20 03 a3     ..   
; &a65c referenced 2 times by &a118, &a508
.ca65c
    lda l0035                                                         ; a65c: a5 35       .5    
    cmp #&80                                                          ; a65e: c9 80       ..    
    bcc ca67c                                                         ; a660: 90 1a       ..    
    beq ca676                                                         ; a662: f0 12       ..    
    lda #&ff                                                          ; a664: a9 ff       ..    
    jsr sub_ca2a4                                                     ; a666: 20 a4 a2     ..   
    jmp ca67c                                                         ; a669: 4c 7c a6    L|.   
; &a66c referenced 2 times by &a450, &a684
.ca66c
    brk                                                               ; a66c: 00          .     
    equb &14                                                          ; a66d: 14          .     
    equs "Too big"                                                    ; a66e: 54 6f 6f... Too...
    equb &00                                                          ; a675: 00          .     
; &a676 referenced 1 time by &a662
.ca676
    lda l0034                                                         ; a676: a5 34       .4    
    ora #1                                                            ; a678: 09 01       ..    
    sta l0034                                                         ; a67a: 85 34       .4    
; &a67c referenced 2 times by &a660, &a669
.ca67c
    lda #0                                                            ; a67c: a9 00       ..    
    sta l0035                                                         ; a67e: 85 35       .5    
    lda l002f                                                         ; a680: a5 2f       ./    
    beq return_21                                                     ; a682: f0 14       ..    
    bpl ca66c                                                         ; a684: 10 e6       ..    
; &a686 referenced 6 times by &a2ee, &a3fb, &a5b4, &a610, &a699, &aaa6
.ca686
    lda #0                                                            ; a686: a9 00       ..    
    sta l002e                                                         ; a688: 85 2e       ..    
    sta l002f                                                         ; a68a: 85 2f       ./    
    sta l0030                                                         ; a68c: 85 30       .0    
    sta l0031                                                         ; a68e: 85 31       .1    
    sta l0032                                                         ; a690: 85 32       .2    
    sta l0033                                                         ; a692: 85 33       .3    
    sta l0034                                                         ; a694: 85 34       .4    
    sta l0035                                                         ; a696: 85 35       .5    
; &a698 referenced 2 times by &a682, &a6ea
.return_21
    rts                                                               ; a698: 60          `     
; &a699 referenced 3 times by &9e8b, &a6a8, &ab22
.sub_ca699
    jsr ca686                                                         ; a699: 20 86 a6     ..   
    ldy #&80                                                          ; a69c: a0 80       ..    
    sty l0031                                                         ; a69e: 84 31       .1    
    iny                                                               ; a6a0: c8          .     
    sty l0030                                                         ; a6a1: 84 30       .0    
    tya                                                               ; a6a3: 98          .     
    rts                                                               ; a6a4: 60          `     
; &a6a5 referenced 1 time by &ab1a
.sub_ca6a5
    jsr sub_ca385                                                     ; a6a5: 20 85 a3     ..   
    jsr sub_ca699                                                     ; a6a8: 20 99 a6     ..   
    bne ca6e7                                                         ; a6ab: d0 3a       .:    
; &a6ad referenced 2 times by &9df8, &a8b8
.sub_ca6ad
    jsr ca1da                                                         ; a6ad: 20 da a1     ..   
    beq ca6bb                                                         ; a6b0: f0 09       ..    
    jsr sub_ca21e                                                     ; a6b2: 20 1e a2     ..   
    jsr sub_ca3b5                                                     ; a6b5: 20 b5 a3     ..   
    bne ca6f1                                                         ; a6b8: d0 37       .7    
    rts                                                               ; a6ba: 60          `     
; &a6bb referenced 2 times by &a6b0, &a6ef
.ca6bb
    jmp c99a7                                                         ; a6bb: 4c a7 99    L..   
    equb &20, &fa, &92, &20, &d3, &a9, &a5                            ; a6be: 20 fa 92...  .....
    equs "JH "                                                        ; a6c5: 4a 48 20    JH    
    equb &e9, &a7, &20, &8d, &a3, &e6, &4a, &20, &9e, &a9, &20, &e9   ; a6c8: e9 a7 20... .. ...
    equb &a7, &20, &d6, &a4, &68, &85, &4a, &20, &9e, &a9, &20, &e9   ; a6d4: a7 20 d6... . ....
    equb &a7, &20, &e7, &a6, &a9, &ff, &60                            ; a6e0: a7 20 e7... . ....
; &a6e7 referenced 1 time by &a6ab
.ca6e7
    jsr ca1da                                                         ; a6e7: 20 da a1     ..   
    beq return_21                                                     ; a6ea: f0 ac       ..    
    jsr sub_ca34e                                                     ; a6ec: 20 4e a3     N.   
    beq ca6bb                                                         ; a6ef: f0 ca       ..    
; &a6f1 referenced 1 time by &a6b8
.ca6f1
    lda l002e                                                         ; a6f1: a5 2e       ..    
    eor l003b                                                         ; a6f3: 45 3b       E;    
    sta l002e                                                         ; a6f5: 85 2e       ..    
    sec                                                               ; a6f7: 38          8     
    lda l0030                                                         ; a6f8: a5 30       .0    
    sbc l003d                                                         ; a6fa: e5 3d       .=    
    bcs ca701                                                         ; a6fc: b0 03       ..    
    dec l002f                                                         ; a6fe: c6 2f       ./    
    sec                                                               ; a700: 38          8     
; &a701 referenced 1 time by &a6fc
.ca701
    adc #&80                                                          ; a701: 69 80       i.    
    sta l0030                                                         ; a703: 85 30       .0    
    bcc ca70a                                                         ; a705: 90 03       ..    
    inc l002f                                                         ; a707: e6 2f       ./    
    clc                                                               ; a709: 18          .     
; &a70a referenced 1 time by &a705
.ca70a
    ldx #&20 ; ' '                                                    ; a70a: a2 20       .     
; &a70c referenced 1 time by &a750
.loop_ca70c
    bcs ca726                                                         ; a70c: b0 18       ..    
    lda l0031                                                         ; a70e: a5 31       .1    
    cmp l003e                                                         ; a710: c5 3e       .>    
    bne ca724                                                         ; a712: d0 10       ..    
    lda l0032                                                         ; a714: a5 32       .2    
    cmp l003f                                                         ; a716: c5 3f       .?    
    bne ca724                                                         ; a718: d0 0a       ..    
    lda l0033                                                         ; a71a: a5 33       .3    
    cmp l0040                                                         ; a71c: c5 40       .@    
    bne ca724                                                         ; a71e: d0 04       ..    
    lda l0034                                                         ; a720: a5 34       .4    
    cmp l0041                                                         ; a722: c5 41       .A    
; &a724 referenced 3 times by &a712, &a718, &a71e
.ca724
    bcc ca73f                                                         ; a724: 90 19       ..    
; &a726 referenced 1 time by &a70c
.ca726
    lda l0034                                                         ; a726: a5 34       .4    
    sbc l0041                                                         ; a728: e5 41       .A    
    sta l0034                                                         ; a72a: 85 34       .4    
    lda l0033                                                         ; a72c: a5 33       .3    
    sbc l0040                                                         ; a72e: e5 40       .@    
    sta l0033                                                         ; a730: 85 33       .3    
    lda l0032                                                         ; a732: a5 32       .2    
    sbc l003f                                                         ; a734: e5 3f       .?    
    sta l0032                                                         ; a736: 85 32       .2    
    lda l0031                                                         ; a738: a5 31       .1    
    sbc l003e                                                         ; a73a: e5 3e       .>    
    sta l0031                                                         ; a73c: 85 31       .1    
    sec                                                               ; a73e: 38          8     
; &a73f referenced 1 time by &a724
.ca73f
    rol l0046                                                         ; a73f: 26 46       &F    
    rol l0045                                                         ; a741: 26 45       &E    
    rol l0044                                                         ; a743: 26 44       &D    
    rol l0043                                                         ; a745: 26 43       &C    
    asl l0034                                                         ; a747: 06 34       .4    
    rol l0033                                                         ; a749: 26 33       &3    
    rol l0032                                                         ; a74b: 26 32       &2    
    rol l0031                                                         ; a74d: 26 31       &1    
    dex                                                               ; a74f: ca          .     
    bne loop_ca70c                                                    ; a750: d0 ba       ..    
    ldx #7                                                            ; a752: a2 07       ..    
; &a754 referenced 1 time by &a792
.loop_ca754
    bcs ca76e                                                         ; a754: b0 18       ..    
    lda l0031                                                         ; a756: a5 31       .1    
    cmp l003e                                                         ; a758: c5 3e       .>    
    bne ca76c                                                         ; a75a: d0 10       ..    
    lda l0032                                                         ; a75c: a5 32       .2    
    cmp l003f                                                         ; a75e: c5 3f       .?    
    bne ca76c                                                         ; a760: d0 0a       ..    
    lda l0033                                                         ; a762: a5 33       .3    
    cmp l0040                                                         ; a764: c5 40       .@    
    bne ca76c                                                         ; a766: d0 04       ..    
    lda l0034                                                         ; a768: a5 34       .4    
    cmp l0041                                                         ; a76a: c5 41       .A    
; &a76c referenced 3 times by &a75a, &a760, &a766
.ca76c
    bcc ca787                                                         ; a76c: 90 19       ..    
; &a76e referenced 1 time by &a754
.ca76e
    lda l0034                                                         ; a76e: a5 34       .4    
    sbc l0041                                                         ; a770: e5 41       .A    
    sta l0034                                                         ; a772: 85 34       .4    
    lda l0033                                                         ; a774: a5 33       .3    
    sbc l0040                                                         ; a776: e5 40       .@    
    sta l0033                                                         ; a778: 85 33       .3    
    lda l0032                                                         ; a77a: a5 32       .2    
    sbc l003f                                                         ; a77c: e5 3f       .?    
    sta l0032                                                         ; a77e: 85 32       .2    
    lda l0031                                                         ; a780: a5 31       .1    
    sbc l003e                                                         ; a782: e5 3e       .>    
    sta l0031                                                         ; a784: 85 31       .1    
    sec                                                               ; a786: 38          8     
; &a787 referenced 1 time by &a76c
.ca787
    rol l0035                                                         ; a787: 26 35       &5    
    asl l0034                                                         ; a789: 06 34       .4    
    rol l0033                                                         ; a78b: 26 33       &3    
    rol l0032                                                         ; a78d: 26 32       &2    
    rol l0031                                                         ; a78f: 26 31       &1    
    dex                                                               ; a791: ca          .     
    bne loop_ca754                                                    ; a792: d0 c0       ..    
    asl l0035                                                         ; a794: 06 35       .5    
    lda l0046                                                         ; a796: a5 46       .F    
    sta l0034                                                         ; a798: 85 34       .4    
    lda l0045                                                         ; a79a: a5 45       .E    
    sta l0033                                                         ; a79c: 85 33       .3    
    lda l0044                                                         ; a79e: a5 44       .D    
    sta l0032                                                         ; a7a0: 85 32       .2    
    lda l0043                                                         ; a7a2: a5 43       .C    
    sta l0031                                                         ; a7a4: 85 31       .1    
    jmp ca659                                                         ; a7a6: 4c 59 a6    LY.   
    equb &00, &15                                                     ; a7a9: 00 15       ..    
    equs "-ve root"                                                   ; a7ab: 2d 76 65... -ve...
    equb &00, &20, &fa, &92, &20, &da, &a1, &f0, &2a, &30, &eb, &20   ; a7b3: 00 20 fa... . ....
    equb &85, &a3, &a5                                                ; a7bf: 85 a3 a5    ...   
    equs "0Ji@"                                                       ; a7c2: 30 4a 69... 0Ji...
    equb &85, &30, &a9, &05, &85, &4a, &20, &ed, &a7, &20, &8d, &a3   ; a7c6: 85 30 a9... .0....
    equb &a9, &6c, &85, &4b, &20, &ad, &a6, &a9, &71, &85, &4b, &20   ; a7d2: a9 6c 85... .l....
    equb &00, &a5, &c6, &30, &c6, &4a, &d0, &e9, &a9, &ff, &60        ; a7de: 00 a5 c6... ......
; &a7e9 referenced 1 time by &a83f
.sub_ca7e9
    lda #&7b ; '{'                                                    ; a7e9: a9 7b       .{    
    bne ca7f7                                                         ; a7eb: d0 0a       ..    
; &a7ed referenced 1 time by &9e7e
.sub_ca7ed
    lda #&71 ; 'q'                                                    ; a7ed: a9 71       .q    
    bne ca7f7                                                         ; a7ef: d0 06       ..    
; &a7f1 referenced 1 time by &aad1
.sub_ca7f1
    lda #&76 ; 'v'                                                    ; a7f1: a9 76       .v    
    bne ca7f7                                                         ; a7f3: d0 02       ..    
; &a7f5 referenced 2 times by &a860, &a8b5
.sub_ca7f5
    lda #&6c ; 'l'                                                    ; a7f5: a9 6c       .l    
; &a7f7 referenced 3 times by &a7eb, &a7ef, &a7f3
.ca7f7
    sta l004b                                                         ; a7f7: 85 4b       .K    
    lda #4                                                            ; a7f9: a9 04       ..    
    sta l004c                                                         ; a7fb: 85 4c       .L    
    rts                                                               ; a7fd: 60          `     
    equb &20, &fa, &92                                                ; a7fe: 20 fa 92     ..   
; &a801 referenced 1 time by &9e75
.sub_ca801
    jsr ca1da                                                         ; a801: 20 da a1     ..   
    beq ca808                                                         ; a804: f0 02       ..    
    bpl ca814                                                         ; a806: 10 0c       ..    
; &a808 referenced 1 time by &a804
.ca808
    brk                                                               ; a808: 00          .     
    equb &16                                                          ; a809: 16          .     
    equs "Log range"                                                  ; a80a: 4c 6f 67... Log...
    equb &00                                                          ; a813: 00          .     
; &a814 referenced 1 time by &a806
.ca814
    jsr sub_ca453                                                     ; a814: 20 53 a4     S.   
    ldy #&80                                                          ; a817: a0 80       ..    
    sty l003b                                                         ; a819: 84 3b       .;    
    sty l003e                                                         ; a81b: 84 3e       .>    
    iny                                                               ; a81d: c8          .     
    sty l003d                                                         ; a81e: 84 3d       .=    
    ldx l0030                                                         ; a820: a6 30       .0    
    beq ca82a                                                         ; a822: f0 06       ..    
    lda l0031                                                         ; a824: a5 31       .1    
    cmp #&b5                                                          ; a826: c9 b5       ..    
    bcc ca82c                                                         ; a828: 90 02       ..    
; &a82a referenced 1 time by &a822
.ca82a
    inx                                                               ; a82a: e8          .     
    dey                                                               ; a82b: 88          .     
; &a82c referenced 1 time by &a828
.ca82c
    txa                                                               ; a82c: 8a          .     
    pha                                                               ; a82d: 48          H     
    sty l0030                                                         ; a82e: 84 30       .0    
    jsr sub_ca505                                                     ; a830: 20 05 a5     ..   
    lda #&7b ; '{'                                                    ; a833: a9 7b       .{    
    jsr ca387                                                         ; a835: 20 87 a3     ..   
    lda #&73 ; 's'                                                    ; a838: a9 73       .s    
    ldy #&a8                                                          ; a83a: a0 a8       ..    
    jsr sub_ca897                                                     ; a83c: 20 97 a8     ..   
    jsr sub_ca7e9                                                     ; a83f: 20 e9 a7     ..   
    jsr sub_ca656                                                     ; a842: 20 56 a6     V.   
    jsr sub_ca656                                                     ; a845: 20 56 a6     V.   
    jsr sub_ca500                                                     ; a848: 20 00 a5     ..   
    jsr sub_ca385                                                     ; a84b: 20 85 a3     ..   
    pla                                                               ; a84e: 68          h     
    sec                                                               ; a84f: 38          8     
    sbc #&81                                                          ; a850: e9 81       ..    
    jsr sub_ca2ed                                                     ; a852: 20 ed a2     ..   
    lda #&6e ; 'n'                                                    ; a855: a9 6e       .n    
    sta l004b                                                         ; a857: 85 4b       .K    
    lda #&a8                                                          ; a859: a9 a8       ..    
    sta l004c                                                         ; a85b: 85 4c       .L    
    jsr sub_ca656                                                     ; a85d: 20 56 a6     V.   
    jsr sub_ca7f5                                                     ; a860: 20 f5 a7     ..   
    jsr sub_ca500                                                     ; a863: 20 00 a5     ..   
    lda #&ff                                                          ; a866: a9 ff       ..    
    rts                                                               ; a868: 60          `     
    equb &7f, &5e, &5b, &d8, &aa, &80, &31, &72, &17, &f8, &06, &7a   ; a869: 7f 5e 5b... .^[...
    equb &12, &38, &a5, &0b, &88, &79, &0e, &9f, &f3, &7c, &2a, &ac   ; a875: 12 38 a5... .8....
    equb &3f, &b5, &86, &34, &01, &a2, &7a, &7f, &63, &8e, &37, &ec   ; a881: 3f b5 86... ?.....
    equb &82, &3f, &ff, &ff, &c1, &7f, &ff, &ff, &ff, &ff             ; a88d: 82 3f ff... .?....
; &a897 referenced 2 times by &a83c, &aade
.sub_ca897
    sta l004d                                                         ; a897: 85 4d       .M    
    sty l004e                                                         ; a899: 84 4e       .N    
    jsr sub_ca385                                                     ; a89b: 20 85 a3     ..   
    ldy #0                                                            ; a89e: a0 00       ..    
    lda (l004d),y                                                     ; a8a0: b1 4d       .M    
    sta l0048                                                         ; a8a2: 85 48       .H    
    inc l004d                                                         ; a8a4: e6 4d       .M    
    bne ca8aa                                                         ; a8a6: d0 02       ..    
    inc l004e                                                         ; a8a8: e6 4e       .N    
; &a8aa referenced 1 time by &a8a6
.ca8aa
    lda l004d                                                         ; a8aa: a5 4d       .M    
    sta l004b                                                         ; a8ac: 85 4b       .K    
    lda l004e                                                         ; a8ae: a5 4e       .N    
    sta l004c                                                         ; a8b0: 85 4c       .L    
    jsr sub_ca3b5                                                     ; a8b2: 20 b5 a3     ..   
; &a8b5 referenced 1 time by &a8d1
.loop_ca8b5
    jsr sub_ca7f5                                                     ; a8b5: 20 f5 a7     ..   
    jsr sub_ca6ad                                                     ; a8b8: 20 ad a6     ..   
    clc                                                               ; a8bb: 18          .     
    lda l004d                                                         ; a8bc: a5 4d       .M    
    adc #5                                                            ; a8be: 69 05       i.    
    sta l004d                                                         ; a8c0: 85 4d       .M    
    sta l004b                                                         ; a8c2: 85 4b       .K    
    lda l004e                                                         ; a8c4: a5 4e       .N    
    adc #0                                                            ; a8c6: 69 00       i.    
    sta l004e                                                         ; a8c8: 85 4e       .N    
    sta l004c                                                         ; a8ca: 85 4c       .L    
    jsr sub_ca500                                                     ; a8cc: 20 00 a5     ..   
    dec l0048                                                         ; a8cf: c6 48       .H    
    bne loop_ca8b5                                                    ; a8d1: d0 e2       ..    
    rts                                                               ; a8d3: 60          `     
    equb &20, &da, &a8, &4c, &27, &a9, &20, &fa, &92, &20, &da, &a1   ; a8d4: 20 da a8...  .....
    equb &10, &08                                                     ; a8e0: 10 08       ..    
    equs "F. "                                                        ; a8e2: 46 2e 20    F.    
    equb &ea, &a8, &4c, &16, &a9, &20, &81, &a3, &20, &b1, &a9, &20   ; a8e5: ea a8 4c... ..L...
    equb &da, &a1, &f0, &09, &20, &f1, &a7, &20, &ad, &a6, &4c, &0a   ; a8f1: da a1 f0... ......
    equb &a9, &20, &55, &aa, &20, &b5, &a3, &a9, &ff, &60, &20, &fa   ; a8fd: a9 20 55... . U...
    equb &92, &20, &da, &a1, &f0, &f5, &10, &0a                       ; a909: 92 20 da... . ....
    equs "F. "                                                        ; a911: 46 2e 20    F.    
    equb &1b, &a9, &a9, &80, &85, &2e, &60, &a5, &30, &c9, &81, &90   ; a914: 1b a9 a9... ......
    equb &15, &20, &a5, &a6, &20, &36, &a9, &20, &48, &aa, &20, &00   ; a920: 15 20 a5... . ....
    equb &a5, &20, &4c, &aa, &20, &00, &a5, &4c, &7e, &ad, &a5, &30   ; a92c: a5 20 4c... . L...
    equb &c9, &73, &90, &c8, &20, &81, &a3, &20, &53, &a4, &a9, &80   ; a938: c9 73 90... .s....
    equb &85, &3d, &85, &3e, &85, &3b, &20, &05, &a5, &a9, &5a, &a0   ; a944: 85 3d 85... .=....
    equb &a9, &20, &97, &a8, &20, &d1, &aa, &a9, &ff, &60, &09, &85   ; a950: a9 20 97... . ....
    equb &a3, &59, &e8, &67, &80, &1c, &9d, &07, &36, &80, &57, &bb   ; a95c: a3 59 e8... .Y....
    equb &78, &df, &80, &ca, &9a, &0e, &83, &84, &8c, &bb, &ca, &6e   ; a968: 78 df 80... x.....
    equb &81, &95, &96, &06, &de, &81, &0a, &c7, &6c, &52, &7f, &7d   ; a974: 81 95 96... ......
    equb &ad, &90, &a1, &82, &fb                                      ; a980: ad 90 a1... ......
    equs "bW/"                                                        ; a985: 62 57 2f    bW/   
    equb &80                                                          ; a988: 80          .     
    equs "mc8, "                                                      ; a989: 6d 63 38... mc8...
    equb &fa, &92, &20, &d3, &a9, &e6, &4a, &4c, &9e, &a9, &20, &fa   ; a98e: fa 92 20... .. ...
    equb &92, &20, &d3, &a9, &a5, &4a, &29, &02, &f0, &06, &20, &aa   ; a99a: 92 20 d3... . ....
    equb &a9, &4c, &7e, &ad, &46, &4a, &90, &15, &20, &c3, &a9, &20   ; a9a6: a9 4c 7e... .L~...
    equb &85, &a3, &20, &56, &a6, &20, &8d, &a3, &20, &99, &a6, &20   ; a9b2: 85 a3 20... .. ...
    equb &d0, &a4, &4c, &b7, &a7, &20, &81, &a3, &20, &56, &a6, &a9   ; a9be: d0 a4 4c... ..L...
    equb &72, &a0, &aa, &20, &97, &a8, &4c, &d1, &aa, &a5, &30, &c9   ; a9ca: 72 a0 aa... r.....
    equb &98, &b0, &5f, &20, &85, &a3, &20, &55, &aa, &20, &4e, &a3   ; a9d6: 98 b0 5f... .._...
    equb &a5, &2e, &85, &3b, &c6, &3d, &20, &05, &a5, &20, &e7, &a6   ; a9e2: a5 2e 85... ......
    equb &20, &fe, &a3, &a5, &34, &85, &4a, &05, &33, &05, &32, &05   ; a9ee: 20 fe a3...  .....
    equb &31, &f0, &38, &a9, &a0, &85, &30, &a0, &00, &84, &35, &a5   ; a9fa: 31 f0 38... 1.8...
    equb &31, &85, &2e, &10, &03, &20, &6c, &a4, &20, &03, &a3, &20   ; aa06: 31 85 2e... 1.....
    equb &7d, &a3, &20, &48, &aa, &20, &56, &a6, &20, &f5, &a7, &20   ; aa12: 7d a3 20... }. ...
    equb &00, &a5, &20, &8d, &a3, &20, &ed, &a7, &20, &b5, &a3, &20   ; aa1e: 00 a5 20... .. ...
    equb &4c, &aa, &20, &56, &a6, &20, &f5, &a7, &4c, &00, &a5, &4c   ; aa2a: 4c aa 20... L. ...
    equb &b2, &a3, &00, &17                                           ; aa36: b2 a3 00... ......
    equs "Accuracy lost"                                              ; aa3a: 41 63 63... Acc...
    equb &00, &a9, &59, &d0, &02, &a9, &5e, &85, &4b, &a9, &aa, &85   ; aa47: 00 a9 59... ..Y...
    equb &4c, &60, &a9, &63, &d0, &f5, &81, &c9, &10, &00, &00, &6f   ; aa53: 4c 60 a9... L`....
    equb &15                                                          ; aa5f: 15          .     
    equs "wza"                                                        ; aa60: 77 7a 61    wza   
    equb &81, &49, &0f, &da, &a2, &7b, &0e, &fa, &35, &12, &86, &65   ; aa63: 81 49 0f... .I....
    equb &2e, &e0, &d3, &05, &84, &8a, &ea, &0c, &1b, &84, &1a, &be   ; aa6f: 2e e0 d3... ......
    equb &bb, &2b, &84                                                ; aa7b: bb 2b 84    .+.   
    equs "7EU"                                                        ; aa7e: 37 45 55    7EU   
    equb &ab, &82, &d5                                                ; aa81: ab 82 d5    ...   
    equs "UW|"                                                        ; aa84: 55 57 7c    UW|   
    equb &83, &c0, &00, &00, &05, &81, &00, &00, &00, &00, &20, &fa   ; aa87: 83 c0 00... ......
    equb &92                                                          ; aa93: 92          .     
; &aa94 referenced 1 time by &9e7b
.sub_caa94
    lda l0030                                                         ; aa94: a5 30       .0    
    cmp #&87                                                          ; aa96: c9 87       ..    
    bcc caab8                                                         ; aa98: 90 1e       ..    
    bne caaa2                                                         ; aa9a: d0 06       ..    
    ldy l0031                                                         ; aa9c: a4 31       .1    
    cpy #&b3                                                          ; aa9e: c0 b3       ..    
    bcc caab8                                                         ; aaa0: 90 16       ..    
; &aaa2 referenced 1 time by &aa9a
.caaa2
    lda l002e                                                         ; aaa2: a5 2e       ..    
    bpl caaac                                                         ; aaa4: 10 06       ..    
    jsr ca686                                                         ; aaa6: 20 86 a6     ..   
    lda #&ff                                                          ; aaa9: a9 ff       ..    
    rts                                                               ; aaab: 60          `     
; &aaac referenced 1 time by &aaa4
.caaac
    brk                                                               ; aaac: 00          .     
    equb &18                                                          ; aaad: 18          .     
    equs "Exp range"                                                  ; aaae: 45 78 70... Exp...
    equb &00                                                          ; aab7: 00          .     
; &aab8 referenced 2 times by &aa98, &aaa0
.caab8
    jsr sub_ca486                                                     ; aab8: 20 86 a4     ..   
    jsr sub_caada                                                     ; aabb: 20 da aa     ..   
    jsr sub_ca381                                                     ; aabe: 20 81 a3     ..   
    lda #&e4                                                          ; aac1: a9 e4       ..    
    sta l004b                                                         ; aac3: 85 4b       .K    
    lda #&aa                                                          ; aac5: a9 aa       ..    
    sta l004c                                                         ; aac7: 85 4c       .L    
    jsr sub_ca3b5                                                     ; aac9: 20 b5 a3     ..   
    lda l004a                                                         ; aacc: a5 4a       .J    
    jsr sub_cab12                                                     ; aace: 20 12 ab     ..   
; &aad1 referenced 1 time by &9e78
.sub_caad1
    jsr sub_ca7f1                                                     ; aad1: 20 f1 a7     ..   
    jsr sub_ca656                                                     ; aad4: 20 56 a6     V.   
    lda #&ff                                                          ; aad7: a9 ff       ..    
    rts                                                               ; aad9: 60          `     
; &aada referenced 1 time by &aabb
.sub_caada
    lda #&e9                                                          ; aada: a9 e9       ..    
    ldy #&aa                                                          ; aadc: a0 aa       ..    
    jsr sub_ca897                                                     ; aade: 20 97 a8     ..   
    lda #&ff                                                          ; aae1: a9 ff       ..    
    rts                                                               ; aae3: 60          `     
    equb &82, &2d, &f8, &54, &58, &07, &83, &e0, &20, &86, &5b, &82   ; aae4: 82 2d f8... .-....
    equb &80, &53, &93, &b8, &83, &20, &00, &06, &a1, &82, &00, &00   ; aaf0: 80 53 93... .S....
    equb &21, &63, &82, &c0, &00, &00, &02, &82, &80, &00, &00, &0c   ; aafc: 21 63 82... !c....
    equb &81, &00, &00, &00, &00, &81, &00, &00, &00, &00             ; ab08: 81 00 00... ......
; &ab12 referenced 3 times by &9e52, &9e69, &aace
.sub_cab12
    tax                                                               ; ab12: aa          .     
    bpl cab1e                                                         ; ab13: 10 09       ..    
    dex                                                               ; ab15: ca          .     
    txa                                                               ; ab16: 8a          .     
    eor #&ff                                                          ; ab17: 49 ff       I.    
    pha                                                               ; ab19: 48          H     
    jsr sub_ca6a5                                                     ; ab1a: 20 a5 a6     ..   
    pla                                                               ; ab1d: 68          h     
; &ab1e referenced 1 time by &ab13
.cab1e
    pha                                                               ; ab1e: 48          H     
    jsr sub_ca385                                                     ; ab1f: 20 85 a3     ..   
    jsr sub_ca699                                                     ; ab22: 20 99 a6     ..   
; &ab25 referenced 1 time by &ab2f
.cab25
    pla                                                               ; ab25: 68          h     
    beq return_22                                                     ; ab26: f0 0a       ..    
    sec                                                               ; ab28: 38          8     
    sbc #1                                                            ; ab29: e9 01       ..    
    pha                                                               ; ab2b: 48          H     
    jsr sub_ca656                                                     ; ab2c: 20 56 a6     V.   
    jmp cab25                                                         ; ab2f: 4c 25 ab    L%.   
; &ab32 referenced 1 time by &ab26
.return_22
    rts                                                               ; ab32: 60          `     
    equb &20, &e3, &92, &a6, &2a, &a9, &80, &20, &f4, &ff, &8a, &4c   ; ab33: 20 e3 92...  .....
    equb &ea, &ae, &20, &dd, &92, &20, &94, &bd, &20, &ae, &8a, &20   ; ab3f: ea ae 20... .. ...
    equb &56, &ae, &20, &f0, &92, &a5, &2a, &48, &a5                  ; ab4b: 56 ae 20... V. ...
    equs "+H "                                                        ; ab54: 2b 48 20    +H    
    equb &ea, &bd, &68, &85, &2d, &68, &85, &2c, &a2, &2a, &a9, &09   ; ab57: ea bd 68... ..h...
    equb &20, &f1, &ff, &a5                                           ; ab63: 20 f1 ff...  .....
    equs ".03L"                                                       ; ab67: 2e 30 33... .03...
    equb &d8, &ae, &a9, &86, &20, &f4, &ff, &8a, &4c, &d8, &ae, &a9   ; ab6b: d8 ae a9... ......
    equb &86, &20, &f4, &ff, &98, &4c, &d8, &ae, &20, &da, &a1, &f0   ; ab77: 86 20 f4... . ....
    equb &1e, &10, &1a, &30, &15, &20, &ec, &ad, &f0, &59, &30, &f0   ; ab83: 1e 10 1a... ......
    equb &a5, &2d, &05, &2c, &05, &2b, &05, &2a, &f0, &0c, &a5, &2d   ; ab8f: a5 2d 05... .-....
    equb &10, &03, &4c, &c4, &ac, &a9, &01, &4c, &d8, &ae, &a9        ; ab9b: 10 03 4c... ..L...
    equs "@` "                                                        ; aba6: 40 60 20    @`    
    equb &fe, &a7, &a0, &69, &a9, &a8, &d0, &07, &20, &fa, &92, &a0   ; aba9: fe a7 a0... ......
    equb &68, &a9, &aa, &84, &4b, &85                                 ; abb5: 68 a9 aa... h.....
    equs "L V"                                                        ; abbb: 4c 20 56    L V   
    equb &a6, &a9, &ff, &60, &20, &fa, &92, &a0, &6d, &a9, &aa, &d0   ; abbe: a6 a9 ff... ......
    equb &ed, &20, &fe, &a8, &e6, &30, &a8, &60, &20, &e3, &92, &20   ; abca: ed 20 fe... . ....
    equb &1e, &8f, &85, &2a, &86, &2b, &84, &2c, &08, &68, &85, &2d   ; abd6: 1e 8f 85... ......
    equb &d8, &a9                                                     ; abe2: d8 a9       ..    
    equs "@`L"                                                        ; abe4: 40 60 4c    @`L   
    equb &0e, &8c, &20, &ec, &ad, &d0, &f8, &e6, &36, &a4, &36, &a9   ; abe7: 0e 8c 20... .. ...
    equb &0d, &99, &ff, &05, &20, &b2, &bd, &a5, &19, &48, &a5, &1a   ; abf3: 0d 99 ff... ......
    equb &48, &a5, &1b, &48, &a4, &04, &a6, &05, &c8, &84, &19, &84   ; abff: 48 a5 1b... H.....
    equb &37, &d0, &01, &e8, &86, &1a, &86, &38, &a0, &ff, &84, &3b   ; ac0b: 37 d0 01... 7.....
    equb &c8, &84, &1b, &20, &55, &89, &20, &29, &9b, &20, &dc, &bd   ; ac17: c8 84 1b... ......
    equb &68, &85, &1b, &68, &85, &1a, &68, &85, &19, &a5             ; ac23: 68 85 1b... h.....
    equs "'` "                                                        ; ac2d: 27 60 20    '`    
    equb &ec, &ad, &d0, &67, &a4, &36, &a9, &00, &99, &00, &06, &a5   ; ac30: ec ad d0... ......
    equb &19, &48, &a5, &1a, &48, &a5, &1b, &48, &a9, &00, &85, &1b   ; ac3c: 19 48 a5... .H....
    equb &a9, &00, &85, &19, &a9, &06, &85, &1a, &20, &8c, &8a, &c9   ; ac48: a9 00 85... ......
    equb &2d, &f0, &0f, &c9, &2b, &d0, &03, &20, &8c, &8a, &c6, &1b   ; ac54: 2d f0 0f... -.....
    equb &20, &7b, &a0, &4c, &73, &ac, &20, &8c, &8a, &c6, &1b, &20   ; ac60: 20 7b a0...  {....
    equb &7b, &a0, &90, &03, &20, &8f, &ad, &85                       ; ac6c: 7b a0 90... {.....
    equs "'L#"                                                        ; ac74: 27 4c 23    'L#   
    equb &ac, &20, &ec, &ad, &f0, &1e, &10, &1b, &a5, &2e, &08, &20   ; ac77: ac 20 ec... . ....
    equb &fe, &a3, &28, &10, &0d, &a5, &3e, &05, &3f, &05, &40, &05   ; ac83: fe a3 28... ..(...
    equb &41, &f0, &03, &20, &c7, &a4, &20, &e7, &a3, &a9             ; ac8f: 41 f0 03... A.....
    equs "@`L"                                                        ; ac99: 40 60 4c    @`L   
    equb &0e, &8c, &20, &ec, &ad, &d0, &f8, &a5, &36, &f0, &1d, &ad   ; ac9c: 0e 8c 20... .. ...
    equb &00, &06, &4c, &d8, &ae, &20, &ad, &af, &c0, &00, &d0, &10   ; aca8: 00 06 4c... ..L...
    equb &8a, &4c, &ea, &ae, &20, &b5, &bf, &aa, &a9, &7f, &20, &f4   ; acb4: 8a 4c ea... .L....
    equb &ff, &8a, &f0, &e6, &a9, &ff, &85, &2a, &85, &2b, &85, &2c   ; acc0: ff 8a f0... ......
    equb &85, &2d, &a9                                                ; accc: 85 2d a9    .-.   
    equs "@` "                                                        ; accf: 40 60 20    @`    
    equb &e3, &92, &a2, &03, &b5, &2a, &49, &ff, &95, &2a, &ca, &10   ; acd2: e3 92 a2... ......
    equb &f7, &a9                                                     ; acde: f7 a9       ..    
    equs "@` )"                                                       ; ace0: 40 60 20... @` ...
    equb &9b, &d0, &b4, &e0, &2c, &d0, &18, &e6, &1b, &20, &b2, &bd   ; ace4: 9b d0 b4... ......
    equb &20, &29, &9b, &d0, &a6, &a9, &01, &85, &2a, &e6, &1b, &e0   ; acf0: 20 29 9b...  )....
    equb &29, &f0, &13, &e0, &2c, &f0, &03, &4c, &a2, &8a, &20, &b2   ; acfc: 29 f0 13... ).....
    equb &bd, &20, &56, &ae, &20, &f0, &92, &20, &cb, &bd, &a0, &00   ; ad08: bd 20 56... . V...
    equb &a6, &2a, &d0, &02, &a2, &01, &86, &2a, &8a, &ca, &86, &2d   ; ad14: a6 2a d0... .*....
    equb &18, &65, &04, &85, &37, &98, &65, &05, &85, &38, &b1, &04   ; ad20: 18 65 04... .e....
    equb &38, &e5, &2d, &90, &21, &e5, &36, &90, &1d, &69, &00, &85   ; ad2c: 38 e5 2d... 8.-...
    equb &2b, &20, &dc, &bd, &a0, &00, &a6, &36, &f0, &0b, &b1, &37   ; ad38: 2b 20 dc... + ....
    equb &d9, &00, &06, &d0, &10, &c8, &ca, &d0, &f5, &a5, &2a, &4c   ; ad44: d9 00 06... ......
    equb &d8, &ae, &20, &dc, &bd, &a9, &00, &f0, &f6, &e6, &2a, &c6   ; ad50: d8 ae 20... .. ...
    equb &2b, &f0, &f6, &e6, &37, &d0, &d9, &e6, &38, &d0, &d5        ; ad5c: 2b f0 f6... +.....
; &ad67 referenced 1 time by &ad8f
.loop_cad67
    jmp c8c0e                                                         ; ad67: 4c 0e 8c    L..   
    equb &20, &ec, &ad, &f0, &f8, &30, &06                            ; ad6a: 20 ec ad...  .....
; &ad71 referenced 4 times by &99c5, &99d8, &9d70, &9d80
.sub_cad71
    bit l002d                                                         ; ad71: 24 2d       $-    
    bmi cad93                                                         ; ad73: 30 1e       0.    
    bpl cadaa                                                         ; ad75: 10 33       .3    
    jsr ca1da                                                         ; ad77: 20 da a1     ..   
    bpl cad89                                                         ; ad7a: 10 0d       ..    
    bmi cad83                                                         ; ad7c: 30 05       0.    
; &ad7e referenced 3 times by &a4d3, &a4fd, &ad91
.cad7e
    jsr ca1da                                                         ; ad7e: 20 da a1     ..   
    beq cad89                                                         ; ad81: f0 06       ..    
; &ad83 referenced 1 time by &ad7c
.cad83
    lda l002e                                                         ; ad83: a5 2e       ..    
    eor #&80                                                          ; ad85: 49 80       I.    
    sta l002e                                                         ; ad87: 85 2e       ..    
; &ad89 referenced 2 times by &ad7a, &ad81
.cad89
    lda #&ff                                                          ; ad89: a9 ff       ..    
    rts                                                               ; ad8b: 60          `     
; &ad8c referenced 1 time by &adf8
.loop_cad8c
    jsr sub_cae02                                                     ; ad8c: 20 02 ae     ..   
    beq loop_cad67                                                    ; ad8f: f0 d6       ..    
    bmi cad7e                                                         ; ad91: 30 eb       0.    
; &ad93 referenced 3 times by &9dc3, &a2c8, &ad73
.cad93
    sec                                                               ; ad93: 38          8     
    lda #0                                                            ; ad94: a9 00       ..    
    tay                                                               ; ad96: a8          .     
    sbc l002a                                                         ; ad97: e5 2a       .*    
    sta l002a                                                         ; ad99: 85 2a       .*    
    tya                                                               ; ad9b: 98          .     
    sbc l002b                                                         ; ad9c: e5 2b       .+    
    sta l002b                                                         ; ad9e: 85 2b       .+    
    tya                                                               ; ada0: 98          .     
    sbc l002c                                                         ; ada1: e5 2c       .,    
    sta l002c                                                         ; ada3: 85 2c       .,    
    tya                                                               ; ada5: 98          .     
    sbc l002d                                                         ; ada6: e5 2d       .-    
    sta l002d                                                         ; ada8: 85 2d       .-    
; &adaa referenced 1 time by &ad75
.cadaa
    lda #&40 ; '@'                                                    ; adaa: a9 40       .@    
    rts                                                               ; adac: 60          `     
    equb &20, &8c, &8a, &c9, &22, &f0, &15, &a2, &00, &b1, &19, &9d   ; adad: 20 8c 8a...  .....
    equb &00, &06, &c8, &e8, &c9, &0d, &f0, &04, &c9, &2c, &d0, &f1   ; adb9: 00 06 c8... ......
    equb &88, &4c, &e1, &ad                                           ; adc5: 88 4c e1... .L....
; &adc9 referenced 1 time by &adfc
.loop_cadc9
    ldx #0                                                            ; adc9: a2 00       ..    
; &adcb referenced 1 time by &addf
.loop_cadcb
    iny                                                               ; adcb: c8          .     
; &adcc referenced 1 time by &add9
.loop_cadcc
    lda (l0019),y                                                     ; adcc: b1 19       ..    
    cmp #&0d                                                          ; adce: c9 0d       ..    
    beq cade9                                                         ; add0: f0 17       ..    
    iny                                                               ; add2: c8          .     
    sta l0600,x                                                       ; add3: 9d 00 06    ...   
    inx                                                               ; add6: e8          .     
    cmp #&22                                                          ; add7: c9 22       ."    
    bne loop_cadcc                                                    ; add9: d0 f1       ..    
    lda (l0019),y                                                     ; addb: b1 19       ..    
    cmp #&22                                                          ; addd: c9 22       ."    
    beq loop_cadcb                                                    ; addf: f0 ea       ..    
    dex                                                               ; ade1: ca          .     
    stx l0036                                                         ; ade2: 86 36       .6    
    sty l001b                                                         ; ade4: 84 1b       ..    
    lda #0                                                            ; ade6: a9 00       ..    
    rts                                                               ; ade8: 60          `     
; &ade9 referenced 1 time by &add0
.cade9
    jmp c8e98                                                         ; ade9: 4c 98 8e    L..   
; &adec referenced 4 times by &92e3, &92fa, &9e20, &adf4
.cadec
    ldy l001b                                                         ; adec: a4 1b       ..    
    inc l001b                                                         ; adee: e6 1b       ..    
    lda (l0019),y                                                     ; adf0: b1 19       ..    
    cmp #&20 ; ' '                                                    ; adf2: c9 20       .     
    beq cadec                                                         ; adf4: f0 f6       ..    
    cmp #&2d ; '-'                                                    ; adf6: c9 2d       .-    
    beq loop_cad8c                                                    ; adf8: f0 92       ..    
    cmp #&22                                                          ; adfa: c9 22       ."    
    beq loop_cadc9                                                    ; adfc: f0 cb       ..    
    cmp #&2b ; '+'                                                    ; adfe: c9 2b       .+    
    bne cae05                                                         ; ae00: d0 03       ..    
; &ae02 referenced 1 time by &ad8c
.sub_cae02
    jsr c8a8c                                                         ; ae02: 20 8c 8a     ..   
; &ae05 referenced 1 time by &ae00
.cae05
    cmp #&8e                                                          ; ae05: c9 8e       ..    
    bcc cae10                                                         ; ae07: 90 07       ..    
    cmp #&c6                                                          ; ae09: c9 c6       ..    
    bcs cae43                                                         ; ae0b: b0 36       .6    
    jmp c8bb1                                                         ; ae0d: 4c b1 8b    L..   
; &ae10 referenced 1 time by &ae07
.cae10
    cmp #&3f ; '?'                                                    ; ae10: c9 3f       .?    
    bcs cae20                                                         ; ae12: b0 0c       ..    
    cmp #&2e ; '.'                                                    ; ae14: c9 2e       ..    
    bcs cae2a                                                         ; ae16: b0 12       ..    
    cmp #&26 ; '&'                                                    ; ae18: c9 26       .&    
    beq cae6d                                                         ; ae1a: f0 51       .Q    
    cmp #&28 ; '('                                                    ; ae1c: c9 28       .(    
    beq cae56                                                         ; ae1e: f0 36       .6    
; &ae20 referenced 1 time by &ae12
.cae20
    dec l001b                                                         ; ae20: c6 1b       ..    
    jsr sub_c95dd                                                     ; ae22: 20 dd 95     ..   
    beq cae30                                                         ; ae25: f0 09       ..    
    jmp cb32c                                                         ; ae27: 4c 2c b3    L,.   
; &ae2a referenced 1 time by &ae16
.cae2a
    jsr sub_ca07b                                                     ; ae2a: 20 7b a0     {.   
    bcc cae43                                                         ; ae2d: 90 14       ..    
    rts                                                               ; ae2f: 60          `     
; &ae30 referenced 1 time by &ae25
.cae30
    lda l0028                                                         ; ae30: a5 28       .(    
    and #2                                                            ; ae32: 29 02       ).    
    bne cae43                                                         ; ae34: d0 0d       ..    
    bcs cae43                                                         ; ae36: b0 0b       ..    
    stx l001b                                                         ; ae38: 86 1b       ..    
; &ae3a referenced 1 time by &85af
.sub_cae3a
    lda l0440                                                         ; ae3a: ad 40 04    .@.   
    ldy l0441                                                         ; ae3d: ac 41 04    .A.   
    jmp caeea                                                         ; ae40: 4c ea ae    L..   
; &ae43 referenced 5 times by &ae0b, &ae2d, &ae34, &ae36, &aec7
.cae43
    brk                                                               ; ae43: 00          .     
    equb &1a                                                          ; ae44: 1a          .     
    equs "No such variable"                                           ; ae45: 4e 6f 20... No ...
    equb &00                                                          ; ae55: 00          .     
; &ae56 referenced 3 times by &9747, &976c, &ae1e
.cae56
    jsr sub_c9b29                                                     ; ae56: 20 29 9b     ).   
    inc l001b                                                         ; ae59: e6 1b       ..    
    cpx #&29 ; ')'                                                    ; ae5b: e0 29       .)    
    bne cae61                                                         ; ae5d: d0 02       ..    
    tay                                                               ; ae5f: a8          .     
    rts                                                               ; ae60: 60          `     
; &ae61 referenced 1 time by &ae5d
.cae61
    brk                                                               ; ae61: 00          .     
    equb &1b                                                          ; ae62: 1b          .     
    equs "Missing )"                                                  ; ae63: 4d 69 73... Mis...
    equb &00                                                          ; ae6c: 00          .     
; &ae6d referenced 1 time by &ae1a
.cae6d
    ldx #0                                                            ; ae6d: a2 00       ..    
    stx l002a                                                         ; ae6f: 86 2a       .*    
    stx l002b                                                         ; ae71: 86 2b       .+    
    stx l002c                                                         ; ae73: 86 2c       .,    
    stx l002d                                                         ; ae75: 86 2d       .-    
    ldy l001b                                                         ; ae77: a4 1b       ..    
; &ae79 referenced 1 time by &aea0
.loop_cae79
    lda (l0019),y                                                     ; ae79: b1 19       ..    
    cmp #&30 ; '0'                                                    ; ae7b: c9 30       .0    
    bcc caea2                                                         ; ae7d: 90 23       .#    
    cmp #&3a ; ':'                                                    ; ae7f: c9 3a       .:    
    bcc cae8d                                                         ; ae81: 90 0a       ..    
    sbc #&37 ; '7'                                                    ; ae83: e9 37       .7    
    cmp #&0a                                                          ; ae85: c9 0a       ..    
    bcc caea2                                                         ; ae87: 90 19       ..    
    cmp #&10                                                          ; ae89: c9 10       ..    
    bcs caea2                                                         ; ae8b: b0 15       ..    
; &ae8d referenced 1 time by &ae81
.cae8d
    asl a                                                             ; ae8d: 0a          .     
    asl a                                                             ; ae8e: 0a          .     
    asl a                                                             ; ae8f: 0a          .     
    asl a                                                             ; ae90: 0a          .     
    ldx #3                                                            ; ae91: a2 03       ..    
; &ae93 referenced 1 time by &ae9d
.loop_cae93
    asl a                                                             ; ae93: 0a          .     
    rol l002a                                                         ; ae94: 26 2a       &*    
    rol l002b                                                         ; ae96: 26 2b       &+    
    rol l002c                                                         ; ae98: 26 2c       &,    
    rol l002d                                                         ; ae9a: 26 2d       &-    
    dex                                                               ; ae9c: ca          .     
    bpl loop_cae93                                                    ; ae9d: 10 f4       ..    
    iny                                                               ; ae9f: c8          .     
    bne loop_cae79                                                    ; aea0: d0 d7       ..    
; &aea2 referenced 3 times by &ae7d, &ae87, &ae8b
.caea2
    txa                                                               ; aea2: 8a          .     
    bpl caeaa                                                         ; aea3: 10 05       ..    
    sty l001b                                                         ; aea5: 84 1b       ..    
    lda #&40 ; '@'                                                    ; aea7: a9 40       .@    
    rts                                                               ; aea9: 60          `     
; &aeaa referenced 1 time by &aea3
.caeaa
    brk                                                               ; aeaa: 00          .     
    equb &1c                                                          ; aeab: 1c          .     
    equs "Bad HEX"                                                    ; aeac: 42 61 64... Bad...
    equb &00, &a2, &2a, &a0, &00, &a9, &01, &20, &f1, &ff, &a9, &40   ; aeb3: 00 a2 2a... ..*...
    equb &60, &a9, &00, &a4, &18, &4c, &ea, &ae                       ; aebf: 60 a9 00... `.....
; &aec7 referenced 1 time by &aee2
.loop_caec7
    jmp cae43                                                         ; aec7: 4c 43 ae    LC.   
    equb &a9, &00, &f0, &0a, &4c, &0e, &8c, &20, &ec, &ad, &d0, &f8   ; aeca: a9 00 f0... ......
    equb &a5, &36                                                     ; aed6: a5 36       .6    
; &aed8 referenced 1 time by &96f8
.sub_caed8
    ldy #0                                                            ; aed8: a0 00       ..    
    beq caeea                                                         ; aeda: f0 0e       ..    
    ldy l001b                                                         ; aedc: a4 1b       ..    
    lda (l0019),y                                                     ; aede: b1 19       ..    
    cmp #&50 ; 'P'                                                    ; aee0: c9 50       .P    
    bne loop_caec7                                                    ; aee2: d0 e3       ..    
    inc l001b                                                         ; aee4: e6 1b       ..    
    lda l0012                                                         ; aee6: a5 12       ..    
    ldy l0013                                                         ; aee8: a4 13       ..    
; &aeea referenced 4 times by &98a4, &ae40, &aeda, &b351
.caeea
    sta l002a                                                         ; aeea: 85 2a       .*    
    sty l002b                                                         ; aeec: 84 2b       .+    
    lda #0                                                            ; aeee: a9 00       ..    
    sta l002c                                                         ; aef0: 85 2c       .,    
    sta l002d                                                         ; aef2: 85 2d       .-    
    lda #&40 ; '@'                                                    ; aef4: a9 40       .@    
    rts                                                               ; aef6: 60          `     
    equb &a5, &1e, &4c, &d8, &ae, &a5, &00, &a4, &01, &4c, &ea, &ae   ; aef7: a5 1e 4c... ..L...
    equb &a5, &06, &a4, &07, &4c, &ea, &ae, &e6, &1b, &20, &56, &ae   ; af03: a5 06 a4... ......
    equb &20, &f0, &92, &a5                                           ; af0f: 20 f0 92...  .....
    equs "-0)"                                                        ; af13: 2d 30 29    -0)   
    equb &05, &2c, &05, &2b, &d0, &08, &a5, &2a, &f0, &4c, &c9, &01   ; af16: 05 2c 05... .,....
    equb &f0, &45, &20, &be, &a2, &20, &51, &bd, &20, &69, &af, &20   ; af22: f0 45 20... .E ...
    equb &7e, &bd, &20, &06, &a6, &20, &03, &a3, &20, &e4, &a3, &20   ; af2e: 7e bd 20... ~. ...
    equb &22, &92, &a9, &40, &60, &a2, &0d, &20, &44, &be, &a9, &40   ; af3a: 22 92 a9... ".....
    equb &85, &11, &60, &a4, &1b, &b1, &19, &c9, &28, &f0, &b9, &20   ; af46: 85 11 60... ..`...
    equb &87, &af, &a2, &0d                                           ; af52: 87 af a2... ......
; &af56 referenced 1 time by &9dbd
.sub_caf56
    lda l0000,x                                                       ; af56: b5 00       ..    
    sta l002a                                                         ; af58: 85 2a       .*    
    lda l0001,x                                                       ; af5a: b5 01       ..    
    sta l002b                                                         ; af5c: 85 2b       .+    
    lda l0002,x                                                       ; af5e: b5 02       ..    
    sta l002c                                                         ; af60: 85 2c       .,    
    lda l0003,x                                                       ; af62: b5 03       ..    
    sta l002d                                                         ; af64: 85 2d       .-    
    lda #&40 ; '@'                                                    ; af66: a9 40       .@    
    rts                                                               ; af68: 60          `     
    equb &20, &87, &af, &a2, &00, &86, &2e, &86, &2f, &86, &35, &a9   ; af69: 20 87 af...  .....
    equb &80, &85, &30, &b5, &0d, &95, &31, &e8, &e0, &04, &d0, &f7   ; af75: 80 85 30... ..0...
    equb &20, &59, &a6, &a9, &ff, &60, &a0, &20, &a5, &0f             ; af81: 20 59 a6...  Y....
    equs "JJJE"                                                       ; af8b: 4a 4a 4a... JJJ...
    equb &11, &6a, &26, &0d, &26, &0e, &26, &0f, &26, &10, &26, &11   ; af8f: 11 6a 26... .j&...
    equb &88, &d0, &eb, &60, &a4, &09, &a5, &08, &4c, &ea, &ae, &a0   ; af9b: 88 d0 eb... ......
    equb &00, &b1, &fd, &4c, &ea, &ae, &20, &e3, &92, &a9, &81, &a6   ; afa7: 00 b1 fd... ......
    equb &2a, &a4, &2b, &4c, &f4, &ff, &20, &e0, &ff, &4c, &d8, &ae   ; afb3: 2a a4 2b... *.+...
    equb &20, &e0, &ff                                                ; afbf: 20 e0 ff     ..   
; &afc2 referenced 1 time by &b3c2
.cafc2
    sta l0600                                                         ; afc2: 8d 00 06    ...   
    lda #1                                                            ; afc5: a9 01       ..    
    sta l0036                                                         ; afc7: 85 36       .6    
    lda #0                                                            ; afc9: a9 00       ..    
    rts                                                               ; afcb: 60          `     
    equb &20, &29, &9b, &d0, &62, &e0, &2c, &d0, &61, &e6, &1b, &20   ; afcc: 20 29 9b...  )....
    equb &b2, &bd, &20, &56, &ae, &20, &f0, &92, &20, &cb, &bd, &a5   ; afd8: b2 bd 20... .. ...
    equb &2a, &c5, &36, &b0, &02, &85, &36, &a9, &00                  ; afe4: 2a c5 36... *.6...
    equs "` )"                                                        ; afed: 60 20 29    ` )   
    equb &9b, &d0, &40, &e0, &2c, &d0, &3f, &e6, &1b, &20, &b2, &bd   ; aff0: 9b d0 40... ..@...
    equb &20, &56, &ae, &20, &f0, &92, &20, &cb, &bd, &a5, &36, &38   ; affc: 20 56 ae...  V....
    equb &e5, &2a, &90, &17, &f0, &17, &aa, &a5, &2a, &85, &36, &f0   ; b008: e5 2a 90... .*....
    equb &10, &a0, &00, &bd, &00, &06, &99, &00, &06, &e8, &c8, &c6   ; b014: 10 a0 00... ......
    equb &2a, &d0, &f4, &a9, &00, &60, &20, &ad, &af, &8a, &c0, &00   ; b020: 2a d0 f4... *.....
    equb &f0, &94, &a9, &00, &85                                      ; b02c: f0 94 a9... ......
    equs "6`L"                                                        ; b031: 36 60 4c    6`L   
    equb &0e, &8c, &4c, &a2, &8a, &20, &29, &9b, &d0, &f5, &e0, &2c   ; b034: 0e 8c 4c... ..L...
    equb &d0, &f4, &20, &b2, &bd, &e6, &1b, &20, &dd, &92, &a5, &2a   ; b040: d0 f4 20... .. ...
    equb &48, &a9, &ff, &85, &2a, &e6, &1b, &e0, &29, &f0, &0a, &e0   ; b04c: 48 a9 ff... H.....
    equb &2c, &d0, &db, &20, &56, &ae, &20, &f0, &92, &20, &cb, &bd   ; b058: 2c d0 db... ,.....
    equb &68, &a8, &18, &f0, &06, &e5, &36, &b0, &c1, &88, &98, &85   ; b064: 68 a8 18... h.....
    equb &2c, &aa, &a0, &00, &a5, &36, &38, &e5, &2c, &c5, &2a, &b0   ; b070: 2c aa a0... ,.....
    equb &02, &85, &2a, &a5, &2a, &f0, &ab, &bd, &00, &06, &99, &00   ; b07c: 02 85 2a... ..*...
    equb &06, &c8, &e8, &c4, &2a, &d0, &f4, &84, &36, &a9, &00, &60   ; b088: 06 c8 e8... ......
    equb &20, &8c, &8a, &a0, &ff, &c9, &7e, &f0, &04, &a0, &00, &c6   ; b094: 20 8c 8a...  .....
    equb &1b, &98, &48, &20, &ec, &ad, &f0, &17, &a8, &68, &85, &15   ; b0a0: 1b 98 48... ..H...
    equb &ad, &03, &04, &d0, &08, &85, &37, &20, &f9, &9e, &a9, &00   ; b0ac: ad 03 04... ......
    equb &60, &20, &df, &9e, &a9, &00, &60, &4c, &0e, &8c, &20, &dd   ; b0b8: 60 20 df... ` ....
    equb &92, &20, &94, &bd, &20, &ae, &8a, &20, &56, &ae, &d0, &ef   ; b0c4: 92 20 94... . ....
    equb &20, &ea, &bd, &a4, &36, &f0, &1e, &a5, &2a, &f0, &1d, &c6   ; b0d0: 20 ea bd...  .....
    equb &2a, &f0, &16, &a2, &00, &bd, &00, &06, &99, &00, &06, &e8   ; b0dc: 2a f0 16... *.....
    equb &c8, &f0, &10, &e4, &36, &90, &f2, &c6, &2a, &d0, &ec, &84   ; b0e8: c8 f0 10... ......
    equb &36, &a9, &00, &60, &85                                      ; b0f4: 36 a9 00... 6.....
    equs "6`L"                                                        ; b0f9: 36 60 4c    6`L   
    equb &03, &9c, &68, &85, &0c, &68, &85, &0b, &00, &1d             ; b0fc: 03 9c 68... ..h...
    equs "No such "                                                   ; b106: 4e 6f 20... No ...
    equb &a4, &2f, &f2, &00, &a5, &18, &85, &0c, &a9, &00, &85, &0b   ; b10e: a4 2f f2... ./....
    equb &a0, &01, &b1, &0b, &30, &de, &a0, &03, &c8, &b1, &0b, &c9   ; b11a: a0 01 b1... ......
    equb &20, &f0, &f9, &c9, &dd, &f0, &0f, &a0, &03, &b1, &0b, &18   ; b126: 20 f0 f9...  .....
    equb &65, &0b, &85, &0b, &90, &e2, &e6, &0c, &b0, &de, &c8, &84   ; b132: 65 0b 85... e.....
    equb &0a, &20, &97, &8a, &98, &aa, &18, &65, &0b, &a4, &0c, &90   ; b13e: 0a 20 97... . ....
    equb &02, &c8, &18, &e9, &00, &85, &3c, &98, &e9, &00, &85, &3d   ; b14a: 02 c8 18... ......
    equb &a0, &00, &c8, &e8, &b1, &3c, &d1, &37, &d0, &cd, &c4, &39   ; b156: a0 00 c8... ......
    equb &d0, &f4, &c8, &b1                                           ; b162: d0 f4 c8... ......
    equs "< &"                                                        ; b166: 3c 20 26    < &   
    equb &89, &b0, &c1, &8a, &a8, &20, &6d, &98, &20, &ed, &94, &a2   ; b169: 89 b0 c1... ......
    equb &01, &20, &31, &95, &a0, &00, &a5, &0b, &91, &02, &c8, &a5   ; b175: 01 20 31... . 1...
    equb &0c, &91, &02, &20, &39, &95, &4c, &f4, &b1, &00, &1e        ; b181: 0c 91 02... ......
    equs "Bad call"                                                   ; b18c: 42 61 64... Bad...
    equb &00, &a9, &a4, &85, &27, &ba, &8a, &18, &65, &04, &20, &2e   ; b194: 00 a9 a4... ......
    equb &be, &a0, &00, &8a, &91, &04, &e8, &c8, &bd, &00, &01, &91   ; b1a0: be a0 00... ......
    equb &04, &e0, &ff, &d0, &f5, &9a, &a5, &27, &48, &a5, &0a, &48   ; b1ac: 04 e0 ff... ......
    equb &a5, &0b, &48, &a5, &0c, &48, &a5, &1b, &aa, &18, &65, &19   ; b1b8: a5 0b 48... ..H...
    equb &a4, &1a, &90, &02, &c8, &18, &e9, &01, &85, &37, &98, &e9   ; b1c4: a4 1a 90... ......
    equb &00, &85, &38, &a0, &02, &20, &5b, &95, &c0, &02, &f0, &ae   ; b1d0: 00 85 38... ..8...
    equb &86, &1b, &88, &84                                           ; b1dc: 86 1b 88... ......
    equs "9 ["                                                        ; b1e0: 39 20 5b    9 [   
    equb &94, &d0, &03, &4c, &12, &b1, &a0, &00, &b1, &2a, &85, &0b   ; b1e3: 94 d0 03... ......
    equb &c8, &b1, &2a, &85, &0c, &a9, &00, &48, &85, &0a, &20, &97   ; b1ef: c8 b1 2a... ..*...
    equb &8a, &c9, &28, &f0, &4d, &c6, &0a, &a5, &1b, &48, &a5, &19   ; b1fb: 8a c9 28... ..(...
    equb &48, &a5, &1a, &48, &20, &a3, &8b, &68, &85, &1a, &68, &85   ; b207: 48 a5 1a... H.....
    equb &19, &68, &85, &1b, &68, &f0, &0c, &85, &3f, &20, &0b, &be   ; b213: 19 68 85... .h....
    equb &20, &c1, &8c, &c6, &3f, &d0, &f6, &68, &85, &0c, &68, &85   ; b21f: 20 c1 8c...  .....
    equb &0b, &68, &85, &0a, &68, &a0, &00, &b1, &04, &aa, &9a, &c8   ; b22b: 0b 68 85... .h....
    equb &e8, &b1, &04, &9d, &00, &01, &e0, &ff, &d0, &f5, &98, &65   ; b237: e8 b1 04... ......
    equb &04, &85, &04, &90, &02, &e6, &05, &a5, &27, &60, &a5, &1b   ; b243: 04 85 04... ......
    equb &48, &a5, &19, &48, &a5, &1a, &48, &20, &82, &95, &f0, &5a   ; b24f: 48 a5 19... H.....
    equb &a5, &1b, &85, &0a, &68, &85, &1a, &68, &85, &19, &68, &85   ; b25b: a5 1b 85... ......
    equb &1b, &68, &aa, &a5, &2c, &48, &a5, &2b, &48, &a5, &2a, &48   ; b267: 1b 68 aa... .h....
    equb &e8, &8a, &48, &20, &0d, &b3, &20, &97, &8a, &c9, &2c, &f0   ; b273: e8 8a 48... ..H...
    equb &cd, &c9, &29, &d0, &31, &a9, &00, &48, &20, &8c, &8a, &c9   ; b27f: cd c9 29... ..)...
    equb &28, &d0                                                     ; b28b: 28 d0       (.    
    equs "' )"                                                        ; b28d: 27 20 29    ' )   
    equb &9b, &20, &90, &bd, &a5, &27, &85, &2d, &20, &94, &bd, &68   ; b290: 9b 20 90... . ....
    equb &aa, &e8, &8a, &48, &20, &8c, &8a, &c9, &2c, &f0, &e7, &c9   ; b29c: aa e8 8a... ......
    equb &29, &d0, &0a, &68, &68, &85, &4d, &85, &4e, &e4, &4d, &f0   ; b2a8: 29 d0 0a... ).....
    equb &15, &a2, &fb, &9a, &68, &85, &0c, &68, &85, &0b, &00, &1f   ; b2b4: 15 a2 fb... ......
    equs "Arguments"                                                  ; b2c0: 41 72 67... Arg...
    equb &00, &20, &ea, &bd, &68, &85, &2a, &68, &85, &2b, &68, &85   ; b2c9: 00 20 ea... . ....
    equs ",0!"                                                        ; b2d5: 2c 30 21    ,0!   
    equb &a5, &2d, &f0, &d9, &85, &27, &a2                            ; b2d8: a5 2d f0... .-....
    equs "7 D"                                                        ; b2df: 37 20 44    7 D   
    equb &be, &a5, &27, &10, &09, &20, &7e, &bd, &20, &b5, &a3, &4c   ; b2e2: be a5 27... ..'...
    equb &f3, &b2, &20, &ea, &bd, &20, &b7, &b4, &4c, &03, &b3, &a5   ; b2ee: f3 b2 20... .. ...
    equb &2d, &d0, &b8, &20, &cb, &bd, &20, &21, &8c, &c6, &4d, &d0   ; b2fa: 2d d0 b8... -.....
    equb &c3, &a5                                                     ; b306: c3 a5       ..    
    equs "NHL"                                                        ; b308: 4e 48 4c    NHL   
    equb &02, &b2, &a4, &2c, &c0, &04, &d0, &05, &a2                  ; b30b: 02 b2 a4... ......
    equs "7 D"                                                        ; b314: 37 20 44    7 D   
    equb &be, &20, &2c, &b3, &08, &20, &90, &bd, &28, &f0, &07, &30   ; b317: be 20 2c... . ,...
    equb &05, &a2                                                     ; b323: 05 a2       ..    
    equs "7 V"                                                        ; b325: 37 20 56    7 V   
    equb &af, &4c, &94, &bd                                           ; b328: af 4c 94... .L....
; &b32c referenced 2 times by &9685, &ae27
.cb32c
    ldy l002c                                                         ; b32c: a4 2c       .,    
    bmi cb384                                                         ; b32e: 30 54       0T    
    beq cb34f                                                         ; b330: f0 1d       ..    
    cpy #5                                                            ; b332: c0 05       ..    
    beq cb354                                                         ; b334: f0 1e       ..    
    ldy #3                                                            ; b336: a0 03       ..    
    lda (l002a),y                                                     ; b338: b1 2a       .*    
    sta l002d                                                         ; b33a: 85 2d       .-    
    dey                                                               ; b33c: 88          .     
    lda (l002a),y                                                     ; b33d: b1 2a       .*    
    sta l002c                                                         ; b33f: 85 2c       .,    
    dey                                                               ; b341: 88          .     
    lda (l002a),y                                                     ; b342: b1 2a       .*    
    tax                                                               ; b344: aa          .     
    dey                                                               ; b345: 88          .     
    lda (l002a),y                                                     ; b346: b1 2a       .*    
    sta l002a                                                         ; b348: 85 2a       .*    
    stx l002b                                                         ; b34a: 86 2b       .+    
    lda #&40 ; '@'                                                    ; b34c: a9 40       .@    
    rts                                                               ; b34e: 60          `     
; &b34f referenced 1 time by &b330
.cb34f
    lda (l002a),y                                                     ; b34f: b1 2a       .*    
    jmp caeea                                                         ; b351: 4c ea ae    L..   
; &b354 referenced 1 time by &b334
.cb354
    dey                                                               ; b354: 88          .     
    lda (l002a),y                                                     ; b355: b1 2a       .*    
    sta l0034                                                         ; b357: 85 34       .4    
    dey                                                               ; b359: 88          .     
    lda (l002a),y                                                     ; b35a: b1 2a       .*    
    sta l0033                                                         ; b35c: 85 33       .3    
    dey                                                               ; b35e: 88          .     
    lda (l002a),y                                                     ; b35f: b1 2a       .*    
    sta l0032                                                         ; b361: 85 32       .2    
    dey                                                               ; b363: 88          .     
    lda (l002a),y                                                     ; b364: b1 2a       .*    
    sta l002e                                                         ; b366: 85 2e       ..    
    dey                                                               ; b368: 88          .     
    lda (l002a),y                                                     ; b369: b1 2a       .*    
    sta l0030                                                         ; b36b: 85 30       .0    
    sty l0035                                                         ; b36d: 84 35       .5    
    sty l002f                                                         ; b36f: 84 2f       ./    
    ora l002e                                                         ; b371: 05 2e       ..    
    ora l0032                                                         ; b373: 05 32       .2    
    ora l0033                                                         ; b375: 05 33       .3    
    ora l0034                                                         ; b377: 05 34       .4    
    beq cb37f                                                         ; b379: f0 04       ..    
    lda l002e                                                         ; b37b: a5 2e       ..    
    ora #&80                                                          ; b37d: 09 80       ..    
; &b37f referenced 1 time by &b379
.cb37f
    sta l0031                                                         ; b37f: 85 31       .1    
    lda #&ff                                                          ; b381: a9 ff       ..    
    rts                                                               ; b383: 60          `     
; &b384 referenced 1 time by &b32e
.cb384
    cpy #&80                                                          ; b384: c0 80       ..    
    beq cb3a7                                                         ; b386: f0 1f       ..    
    ldy #3                                                            ; b388: a0 03       ..    
    lda (l002a),y                                                     ; b38a: b1 2a       .*    
    sta l0036                                                         ; b38c: 85 36       .6    
    beq return_23                                                     ; b38e: f0 16       ..    
    ldy #1                                                            ; b390: a0 01       ..    
    lda (l002a),y                                                     ; b392: b1 2a       .*    
    sta l0038                                                         ; b394: 85 38       .8    
    dey                                                               ; b396: 88          .     
    lda (l002a),y                                                     ; b397: b1 2a       .*    
    sta l0037                                                         ; b399: 85 37       .7    
    ldy l0036                                                         ; b39b: a4 36       .6    
; &b39d referenced 1 time by &b3a4
.loop_cb39d
    dey                                                               ; b39d: 88          .     
    lda (l0037),y                                                     ; b39e: b1 37       .7    
    sta l0600,y                                                       ; b3a0: 99 00 06    ...   
    tya                                                               ; b3a3: 98          .     
    bne loop_cb39d                                                    ; b3a4: d0 f7       ..    
; &b3a6 referenced 1 time by &b38e
.return_23
    rts                                                               ; b3a6: 60          `     
; &b3a7 referenced 1 time by &b386
.cb3a7
    lda l002b                                                         ; b3a7: a5 2b       .+    
    beq cb3c0                                                         ; b3a9: f0 15       ..    
    ldy #0                                                            ; b3ab: a0 00       ..    
; &b3ad referenced 1 time by &b3b7
.loop_cb3ad
    lda (l002a),y                                                     ; b3ad: b1 2a       .*    
    sta l0600,y                                                       ; b3af: 99 00 06    ...   
    eor #&0d                                                          ; b3b2: 49 0d       I.    
    beq cb3ba                                                         ; b3b4: f0 04       ..    
    iny                                                               ; b3b6: c8          .     
    bne loop_cb3ad                                                    ; b3b7: d0 f4       ..    
    tya                                                               ; b3b9: 98          .     
; &b3ba referenced 1 time by &b3b4
.cb3ba
    sty l0036                                                         ; b3ba: 84 36       .6    
    rts                                                               ; b3bc: 60          `     
    equb &20, &e3, &92                                                ; b3bd: 20 e3 92     ..   
; &b3c0 referenced 1 time by &b3a9
.cb3c0
    lda l002a                                                         ; b3c0: a5 2a       .*    
    jmp cafc2                                                         ; b3c2: 4c c2 af    L..   
    equb &a0, &00, &84, &08, &84, &09, &a6, &18, &86, &38, &84, &37   ; b3c5: a0 00 84... ......
    equb &a6, &0c, &e0, &07, &f0, &2a, &a6, &0b, &20, &42, &89, &c9   ; b3d1: a6 0c e0... ......
    equb &0d, &d0, &19, &e4, &37, &a5, &0c, &e5, &38, &90, &19, &20   ; b3dd: 0d d0 19... ......
    equb &42, &89, &09, &00, &30, &12, &85, &09, &20, &42, &89, &85   ; b3e9: 42 89 09... B.....
    equb &08, &20, &42, &89, &e4, &37, &a5, &0c, &e5, &38, &b0, &d8   ; b3f5: 08 20 42... . B...
    equb &60, &20, &c5, &b3, &84, &20, &b1, &fd, &d0, &08, &a9, &33   ; b401: 60 20 c5... ` ....
    equb &85, &16, &a9, &b4, &85, &17, &a5, &16, &85, &0b, &a5, &17   ; b40d: 85 16 a9... ......
    equb &85, &0c, &20, &3a, &bd, &aa, &86, &0a, &a9, &da, &20, &f4   ; b419: 85 0c 20... .. ...
    equb &ff, &a9, &7e, &20, &f4, &ff, &a2, &ff, &86, &28, &9a, &4c   ; b425: ff a9 7e... ..~...
    equb &a3, &8b, &f6, &3a, &e7, &9e, &f1                            ; b431: a3 8b f6... ......
    equb &22, " at line ", &22, ";"                                   ; b438: 22 20 61... " a...
    equb &9e, &3a, &e0, &8b, &f1, &3a, &e0, &0d, &20, &21, &88, &a2   ; b444: 9e 3a e0... .:....
    equb &03, &a5, &2a, &48, &a5, &2b, &48, &8a, &48, &20, &da, &92   ; b450: 03 a5 2a... ..*...
    equb &68, &aa, &ca, &d0, &f0, &20, &52, &98, &a5, &2a, &85, &3d   ; b45c: 68 aa ca... h.....
    equb &a5, &2b, &85, &3e, &a0, &07, &a2, &05, &d0, &1d, &20, &21   ; b468: a5 2b 85... .+....
    equb &88, &a2, &0d, &a5, &2a, &48, &8a, &48, &20, &da, &92, &68   ; b474: 88 a2 0d... ......
    equb &aa, &ca, &d0, &f3, &20, &52, &98, &a5, &2a, &85, &44, &a2   ; b480: aa ca d0... ......
    equb &0c, &a0, &08, &68, &95, &37, &ca, &10, &fa, &98, &a2, &37   ; b48c: 0c a0 08... ......
    equb &a0, &00, &20, &f1, &ff, &4c, &9b, &8b, &20, &21, &88, &20   ; b498: a0 00 20... .. ...
    equb &52, &98, &a4, &2a, &88, &84, &23, &4c, &9b, &8b             ; b4a4: 52 98 a4... R.....
; &b4ae referenced 2 times by &b4bf, &b4e2
.cb4ae
    jmp c8c0e                                                         ; b4ae: 4c 0e 8c    L..   
    equb &20, &29, &9b                                                ; b4b1: 20 29 9b     ).   
; &b4b4 referenced 2 times by &85b4, &8c05
.sub_cb4b4
    jsr sub_cbe0b                                                     ; b4b4: 20 0b be     ..   
    lda l0039                                                         ; b4b7: a5 39       .9    
    cmp #5                                                            ; b4b9: c9 05       ..    
    beq cb4e0                                                         ; b4bb: f0 23       .#    
    lda l0027                                                         ; b4bd: a5 27       .'    
    beq cb4ae                                                         ; b4bf: f0 ed       ..    
    bpl cb4c6                                                         ; b4c1: 10 03       ..    
    jsr ca3e4                                                         ; b4c3: 20 e4 a3     ..   
; &b4c6 referenced 1 time by &b4c1
.cb4c6
    ldy #0                                                            ; b4c6: a0 00       ..    
    lda l002a                                                         ; b4c8: a5 2a       .*    
    sta (l0037),y                                                     ; b4ca: 91 37       .7    
    lda l0039                                                         ; b4cc: a5 39       .9    
    beq return_24                                                     ; b4ce: f0 0f       ..    
    lda l002b                                                         ; b4d0: a5 2b       .+    
    iny                                                               ; b4d2: c8          .     
    sta (l0037),y                                                     ; b4d3: 91 37       .7    
    lda l002c                                                         ; b4d5: a5 2c       .,    
    iny                                                               ; b4d7: c8          .     
    sta (l0037),y                                                     ; b4d8: 91 37       .7    
    lda l002d                                                         ; b4da: a5 2d       .-    
    iny                                                               ; b4dc: c8          .     
    sta (l0037),y                                                     ; b4dd: 91 37       .7    
; &b4df referenced 1 time by &b4ce
.return_24
    rts                                                               ; b4df: 60          `     
; &b4e0 referenced 1 time by &b4bb
.cb4e0
    lda l0027                                                         ; b4e0: a5 27       .'    
    beq cb4ae                                                         ; b4e2: f0 ca       ..    
    bmi cb4e9                                                         ; b4e4: 30 03       0.    
    jsr ca2be                                                         ; b4e6: 20 be a2     ..   
; &b4e9 referenced 1 time by &b4e4
.cb4e9
    ldy #0                                                            ; b4e9: a0 00       ..    
    lda l0030                                                         ; b4eb: a5 30       .0    
    sta (l0037),y                                                     ; b4ed: 91 37       .7    
    iny                                                               ; b4ef: c8          .     
    lda l002e                                                         ; b4f0: a5 2e       ..    
    and #&80                                                          ; b4f2: 29 80       ).    
    sta l002e                                                         ; b4f4: 85 2e       ..    
    lda l0031                                                         ; b4f6: a5 31       .1    
    and #&7f                                                          ; b4f8: 29 7f       ).    
    ora l002e                                                         ; b4fa: 05 2e       ..    
    sta (l0037),y                                                     ; b4fc: 91 37       .7    
    iny                                                               ; b4fe: c8          .     
    lda l0032                                                         ; b4ff: a5 32       .2    
    sta (l0037),y                                                     ; b501: 91 37       .7    
    iny                                                               ; b503: c8          .     
    lda l0033                                                         ; b504: a5 33       .3    
    sta (l0037),y                                                     ; b506: 91 37       .7    
    iny                                                               ; b508: c8          .     
    lda l0034                                                         ; b509: a5 34       .4    
    sta (l0037),y                                                     ; b50b: 91 37       .7    
    rts                                                               ; b50d: 60          `     
; &b50e referenced 1 time by &8571
.sub_cb50e
    sta l0037                                                         ; b50e: 85 37       .7    
    cmp #&80                                                          ; b510: c9 80       ..    
    bcc cb558                                                         ; b512: 90 44       .D    
    lda #&71 ; 'q'                                                    ; b514: a9 71       .q    
    sta l0038                                                         ; b516: 85 38       .8    
    lda #&80                                                          ; b518: a9 80       ..    
    sta l0039                                                         ; b51a: 85 39       .9    
    sty l003a                                                         ; b51c: 84 3a       .:    
; &b51e referenced 2 times by &b530, &b534
.cb51e
    ldy #0                                                            ; b51e: a0 00       ..    
; &b520 referenced 1 time by &b523
.loop_cb520
    iny                                                               ; b520: c8          .     
    lda (l0038),y                                                     ; b521: b1 38       .8    
    bpl loop_cb520                                                    ; b523: 10 fb       ..    
    cmp l0037                                                         ; b525: c5 37       .7    
    beq cb536                                                         ; b527: f0 0d       ..    
    iny                                                               ; b529: c8          .     
    tya                                                               ; b52a: 98          .     
    sec                                                               ; b52b: 38          8     
    adc l0038                                                         ; b52c: 65 38       e8    
    sta l0038                                                         ; b52e: 85 38       .8    
    bcc cb51e                                                         ; b530: 90 ec       ..    
    inc l0039                                                         ; b532: e6 39       .9    
    bcs cb51e                                                         ; b534: b0 e8       ..    
; &b536 referenced 1 time by &b527
.cb536
    ldy #0                                                            ; b536: a0 00       ..    
; &b538 referenced 1 time by &b540
.loop_cb538
    lda (l0038),y                                                     ; b538: b1 38       .8    
    bmi cb542                                                         ; b53a: 30 06       0.    
    jsr cb558                                                         ; b53c: 20 58 b5     X.   
    iny                                                               ; b53f: c8          .     
    bne loop_cb538                                                    ; b540: d0 f6       ..    
; &b542 referenced 1 time by &b53a
.cb542
    ldy l003a                                                         ; b542: a4 3a       .:    
    rts                                                               ; b544: 60          `     
; &b545 referenced 2 times by &8526, &b562
.sub_cb545
    pha                                                               ; b545: 48          H     
    lsr a                                                             ; b546: 4a          J     
    lsr a                                                             ; b547: 4a          J     
    lsr a                                                             ; b548: 4a          J     
    lsr a                                                             ; b549: 4a          J     
    jsr sub_cb550                                                     ; b54a: 20 50 b5     P.   
    pla                                                               ; b54d: 68          h     
    and #&0f                                                          ; b54e: 29 0f       ).    
; &b550 referenced 1 time by &b54a
.sub_cb550
    cmp #&0a                                                          ; b550: c9 0a       ..    
    bcc cb556                                                         ; b552: 90 02       ..    
    adc #6                                                            ; b554: 69 06       i.    
; &b556 referenced 1 time by &b552
.cb556
    adc #&30 ; '0'                                                    ; b556: 69 30       i0    
; &b558 referenced 8 times by &855c, &855f, &9911, &9919, &9964, &b512, &b53c, &bc02
.cb558
    cmp #&0d                                                          ; b558: c9 0d       ..    
    bne cb567                                                         ; b55a: d0 0b       ..    
    jsr oswrch                                                        ; b55c: 20 ee ff     ..   
    jmp cbc28                                                         ; b55f: 4c 28 bc    L(.   
; &b562 referenced 2 times by &852b, &854e
.sub_cb562
    jsr sub_cb545                                                     ; b562: 20 45 b5     E.   
; &b565 referenced 4 times by &8544, &8559, &991c, &995a
.cb565
    lda #&20 ; ' '                                                    ; b565: a9 20       .     
; &b567 referenced 1 time by &b55a
.cb567
    pha                                                               ; b567: 48          H     
    lda l0023                                                         ; b568: a5 23       .#    
    cmp l001e                                                         ; b56a: c5 1e       ..    
    bcs cb571                                                         ; b56c: b0 03       ..    
    jsr sub_cbc25                                                     ; b56e: 20 25 bc     %.   
; &b571 referenced 1 time by &b56c
.cb571
    pla                                                               ; b571: 68          h     
    inc l001e                                                         ; b572: e6 1e       ..    
    jmp (wrchv)                                                       ; b574: 6c 0e 02    l..   
    equb &25, &1f, &f0, &0e, &8a, &f0, &0b, &30, &e5, &20, &65, &b5   ; b577: 25 1f f0... %.....
    equb &20, &58, &b5, &ca, &d0, &f7, &60, &e6, &0a, &20, &1d, &9b   ; b583: 20 58 b5...  X....
    equb &20, &4c, &98, &20, &ee, &92, &a5, &2a, &85, &1f, &4c, &f6   ; b58f: 20 4c 98...  L....
    equb &8a, &c8, &b1, &0b, &c9, &4f, &f0, &e7, &a9, &00, &85, &3b   ; b59b: 8a c8 b1... ......
    equb &85, &3c, &20, &d8, &ae, &20, &df, &97, &08, &20, &94, &bd   ; b5a7: 85 3c 20... .< ...
    equb &a9, &ff, &85, &2a, &a9, &7f, &85, &2b, &28, &90, &11, &20   ; b5b3: a9 ff 85... ......
    equb &97, &8a, &c9, &2c, &f0, &13, &20, &ea, &bd, &20, &94, &bd   ; b5bf: 97 8a c9... ......
    equb &c6, &0a, &10, &0c, &20, &97, &8a, &c9, &2c, &f0, &02, &c6   ; b5cb: c6 0a 10... ......
    equb &0a, &20, &df, &97, &a5, &2a, &85, &31, &a5, &2b, &85        ; b5d7: 0a 20 df... . ....
    equs "2 W"                                                        ; b5e2: 32 20 57    2 W   
    equb &98, &20, &6f, &be, &20, &ea, &bd, &20, &70, &99, &a5, &3d   ; b5e5: 98 20 6f... . o...
    equb &85, &0b, &a5, &3e, &85, &0c, &90, &16, &88, &b0, &06, &20   ; b5f1: 85 0b a5... ......
    equb &25, &bc, &20, &6d, &98, &b1, &0b, &85, &2b, &c8, &b1, &0b   ; b5fd: 25 bc 20... %. ...
    equb &85, &2a, &c8, &c8, &84, &0a, &a5, &2a, &18, &e5, &31, &a5   ; b609: 85 2a c8... .*....
    equb &2b, &e5, &32, &90, &03, &4c, &f6, &8a, &20, &23, &99, &a2   ; b615: 2b e5 32... +.2...
    equb &ff, &86, &4d, &a9, &01, &20, &77, &b5, &a6, &3b, &a9, &02   ; b621: ff 86 4d... ..M...
    equb &20, &77, &b5, &a6, &3c, &a9, &04, &20, &77, &b5, &a4, &0a   ; b62d: 20 77 b5...  w....
    equb &b1, &0b, &c9, &0d, &f0, &bd, &c9, &22, &d0, &0e, &a9, &ff   ; b639: b1 0b c9... ......
    equb &45, &4d, &85, &4d, &a9                                      ; b645: 45 4d 85... EM....
    equb &22, " X"                                                    ; b64a: 22 20 58    " X   
    equb &b5, &c8, &d0, &e8, &24, &4d, &10, &f6, &c9, &8d, &d0, &0f   ; b64d: b5 c8 d0... ......
    equb &20, &eb, &97, &84, &0a, &a9, &00, &85, &14, &20, &1f, &99   ; b659: 20 eb 97...  .....
    equb &4c, &37, &b6, &c9, &e3, &d0, &02, &e6, &3b, &c9, &ed, &d0   ; b665: 4c 37 b6... L7....
    equb &06, &a6, &3b, &f0, &02, &c6, &3b, &c9, &f5, &d0, &02, &e6   ; b671: 06 a6 3b... ..;...
    equb &3c, &c9, &fd, &d0, &06, &a6, &3c, &f0, &02, &c6, &3c, &20   ; b67d: 3c c9 fd... <.....
    equb &0e, &b5, &c8, &d0, &ab, &00                                 ; b689: 0e b5 c8... ......
    equs " No "                                                       ; b68f: 20 4e 6f...  No...
    equb &e3, &00, &20, &c9, &95, &d0, &09, &a6, &26, &f0, &f0, &b0   ; b693: e3 00 20... .. ...
    equs "7L*"                                                        ; b69f: 37 4c 2a    7L*   
    equb &98, &b0, &fb, &a6, &26, &f0, &e5, &a5, &2a, &dd, &f1, &04   ; b6a2: 98 b0 fb... ......
    equb &d0, &0e, &a5, &2b, &dd, &f2, &04, &d0, &07, &a5, &2c, &dd   ; b6ae: d0 0e a5... ......
    equb &f3, &04, &f0, &19, &8a, &38, &e9, &0f, &aa, &86, &26, &d0   ; b6ba: f3 04 f0... ......
    equb &e2, &00                                                     ; b6c6: e2 00       ..    
    equs "!Can't Match "                                              ; b6c8: 21 43 61... !Ca...
    equb &e3, &00, &bd, &f1, &04, &85, &2a, &bd, &f2, &04, &85, &2b   ; b6d5: e3 00 bd... ......
    equb &bc, &f3, &04, &c0, &05, &f0, &7e, &a0, &00, &b1, &2a, &7d   ; b6e1: bc f3 04... ......
    equb &f4, &04, &91, &2a, &85, &37, &c8, &b1, &2a, &7d, &f5, &04   ; b6ed: f4 04 91... ......
    equb &91, &2a, &85, &38, &c8, &b1, &2a, &7d, &f6, &04, &91, &2a   ; b6f9: 91 2a 85... .*....
    equb &85, &39, &c8, &b1, &2a, &7d, &f7, &04, &91, &2a, &a8, &a5   ; b705: 85 39 c8... .9....
    equb &37, &38, &fd, &f9, &04, &85, &37, &a5, &38, &fd, &fa, &04   ; b711: 37 38 fd... 78....
    equb &85, &38, &a5, &39, &fd, &fb, &04, &85, &39, &98, &fd, &fc   ; b71d: 85 38 a5... .8....
    equb &04, &05, &37, &05, &38, &05, &39, &f0, &0f, &98, &5d, &f7   ; b729: 04 05 37... ..7...
    equb &04, &5d, &fc, &04, &10, &04, &b0, &04, &90, &12, &b0, &10   ; b735: 04 5d fc... .]....
    equb &bc, &fe, &04, &bd, &ff, &04, &84, &0b, &85, &0c, &20, &77   ; b741: bc fe 04... ......
    equb &98, &4c, &a3, &8b, &a5, &26, &38, &e9, &0f, &85, &26, &a4   ; b74d: 98 4c a3... .L....
    equb &1b, &84, &0a, &20, &97, &8a, &c9, &2c, &d0, &3e, &4c, &95   ; b759: 1b 84 0a... ......
    equb &b6, &20, &54, &b3, &a5, &26, &18, &69, &f4, &85, &4b, &a9   ; b765: b6 20 54... . T...
    equb &05, &85, &4c, &20, &00, &a5, &a5, &2a, &85, &37, &a5, &2b   ; b771: 05 85 4c... ..L...
    equb &85, &38, &20, &e9, &b4, &a5, &26, &85, &27, &18, &69, &f9   ; b77d: 85 38 20... .8 ...
    equb &85, &4b, &a9, &05, &85                                      ; b789: 85 4b a9... .K....
    equs "L _"                                                        ; b78e: 4c 20 5f    L _   
    equb &9a, &f0, &ad, &bd, &f5, &04, &30, &04, &b0, &a6, &90, &b4   ; b791: 9a f0 ad... ......
    equb &90, &a2, &b0, &b0, &4c, &96, &8b, &00, &22, &e3             ; b79d: 90 a2 b0... ......
    equs " variable"                                                  ; b7a7: 20 76 61...  va...
    equb &00                                                          ; b7b0: 00          .     
    equs "#Too many "                                                 ; b7b1: 23 54 6f... #To...
    equb &e3, &73, &00                                                ; b7bb: e3 73 00    .s.   
    equs "$No "                                                       ; b7be: 24 4e 6f... $No...
    equb &b8, &00, &20, &82, &95, &f0, &db, &b0, &d9, &20, &94, &bd   ; b7c2: b8 00 20... .. ...
    equb &20, &41, &98, &20, &b1, &b4, &a4, &26, &c0, &96, &b0, &d6   ; b7ce: 20 41 98...  A....
    equb &a5, &37, &99, &00, &05, &a5, &38, &99, &01, &05, &a5, &39   ; b7da: a5 37 99... .7....
    equb &99, &02, &05, &aa, &20, &8c, &8a, &c9, &b8, &d0, &cc, &e0   ; b7e6: 99 02 05... ......
    equb &05, &f0, &5a, &20, &dd, &92, &a4, &26, &a5, &2a, &99, &08   ; b7f2: 05 f0 5a... ..Z...
    equb &05, &a5, &2b, &99, &09, &05, &a5, &2c, &99, &0a, &05, &a5   ; b7fe: 05 a5 2b... ..+...
    equb &2d, &99, &0b, &05, &a9, &01, &20, &d8, &ae, &20, &8c, &8a   ; b80a: 2d 99 0b... -.....
    equb &c9, &88, &d0, &05, &20, &dd, &92, &a4, &1b, &84, &0a, &a4   ; b816: c9 88 d0... ......
    equb &26, &a5, &2a, &99, &03, &05, &a5, &2b, &99, &04, &05, &a5   ; b822: 26 a5 2a... &.*...
    equb &2c, &99, &05, &05, &a5, &2d, &99, &06, &05, &20, &80, &98   ; b82e: 2c 99 05... ,.....
    equb &a4, &26, &a5, &0b, &99, &0d, &05, &a5, &0c, &99, &0e, &05   ; b83a: a4 26 a5... .&....
    equb &18, &98, &69, &0f, &85, &26, &4c, &a3, &8b, &20, &29, &9b   ; b846: 18 98 69... ..i...
    equb &20, &fd, &92, &a5, &26, &18, &69, &08, &85, &4b, &a9, &05   ; b852: 20 fd 92...  .....
    equb &85, &4c, &20, &8d, &a3, &20, &99, &a6, &20, &8c, &8a, &c9   ; b85e: 85 4c 20... .L ...
    equb &88, &d0, &08, &20, &29, &9b, &20, &fd, &92, &a4, &1b, &84   ; b86a: 88 d0 08... ......
    equb &0a, &a5, &26, &18, &69, &03, &85, &4b, &a9, &05, &85, &4c   ; b876: 0a a5 26... ..&...
    equb &20, &8d, &a3, &4c, &37, &b8, &20, &9a, &b9, &20, &57, &98   ; b882: 20 8d a3...  .....
    equb &a4, &25, &c0, &1a, &b0, &0e, &a5, &0b, &99, &cc, &05, &a5   ; b88e: a4 25 c0... .%....
    equb &0c, &99, &e6, &05, &e6, &25, &90, &30, &00                  ; b89a: 0c 99 e6... ......
    equs "%Too many "                                                 ; b8a3: 25 54 6f... %To...
    equb &e4, &73, &00                                                ; b8ad: e4 73 00    .s.   
    equs "&No "                                                       ; b8b0: 26 4e 6f... &No...
    equb &e4, &00, &20, &57, &98, &a6, &25, &f0, &f2, &c6, &25, &bc   ; b8b4: e4 00 20... .. ...
    equb &cb, &05, &bd, &e5, &05, &84, &0b, &85, &0c, &4c, &9b, &8b   ; b8c0: cb 05 bd... ......
    equb &20, &9a, &b9, &20, &57, &98, &a5, &20, &f0, &03, &20, &05   ; b8cc: 20 9a b9...  .....
    equb &99, &a4, &3d, &a5, &3e, &84, &0b, &85, &0c, &4c, &a3, &8b   ; b8d8: 99 a4 3d... ..=...
    equb &20, &57, &98, &a9, &33, &85, &16, &a9, &b4, &85, &17, &4c   ; b8e4: 20 57 98...  W....
    equb &9b, &8b, &20, &97, &8a, &c9, &87, &f0, &eb, &a4, &0a, &88   ; b8f0: 9b 8b 20... .. ...
    equb &20, &6d, &98, &a5, &0b, &85, &16, &a5, &0c, &85, &17, &4c   ; b8fc: 20 6d 98...  m....
    equb &7d, &8b, &00, &27, &ee                                      ; b908: 7d 8b 00... }.....
    equs " syntax"                                                    ; b90d: 20 73 79...  sy...
    equb &00, &20, &97, &8a, &c9, &85, &f0, &d6, &c6, &0a, &20, &1d   ; b914: 00 20 97... . ....
    equb &9b, &20, &f0, &92, &a4, &1b, &c8, &84, &0a, &e0, &e5, &f0   ; b920: 9b 20 f0... . ....
    equb &04, &e0, &e4, &d0, &d9, &8a, &48, &a5, &2b, &05, &2c, &05   ; b92c: 04 e0 e4... ......
    equb &2d, &d0, &42, &a6, &2a, &f0, &3e, &ca, &f0, &1a, &a4, &0a   ; b938: 2d d0 42... -.B...
    equb &b1, &0b, &c8, &c9, &0d, &f0, &32, &c9, &3a, &f0, &2e, &c9   ; b944: b1 0b c8... ......
    equb &8b, &f0, &2a, &c9, &2c, &d0, &ed, &ca, &d0, &ea, &84, &0a   ; b950: 8b f0 2a... ..*...
    equb &20, &9a, &b9, &68, &c9, &e4, &f0, &06, &20, &77, &98, &4c   ; b95c: 20 9a b9...  .....
    equb &d2, &b8, &a4, &0a, &b1, &0b, &c8, &c9, &0d, &f0, &04, &c9   ; b968: d2 b8 a4... ......
    equb &3a, &d0, &f5, &88, &84, &0a, &4c, &8b, &b8, &a4, &0a, &68   ; b974: 3a d0 f5... :.....
    equb &b1, &0b, &c8, &c9, &8b, &f0, &0e, &c9, &0d, &d0, &f5, &00   ; b980: b1 0b c8... ......
    equb &28, &ee                                                     ; b98c: 28 ee       (.    
    equs " range"                                                     ; b98e: 20 72 61...  ra...
    equb &00, &84, &0a, &4c, &e3, &98, &20, &df, &97, &b0, &10, &20   ; b994: 00 84 0a... ......
    equb &1d, &9b, &20, &f0, &92, &a5, &1b, &85, &0a, &a5, &2b, &29   ; b9a0: 1d 9b 20... .. ...
    equb &7f, &85                                                     ; b9ac: 7f 85       ..    
    equs "+ p"                                                        ; b9ae: 2b 20 70    + p   
    equb &99, &b0, &01, &60, &00                                      ; b9b1: 99 b0 01... ......
    equs ")No such line"                                              ; b9b6: 29 4e 6f... )No...
    equb &00, &4c, &0e, &8c, &4c, &2a, &98, &84, &0a, &4c, &98, &8b   ; b9c3: 00 4c 0e... .L....
    equb &c6, &0a, &20, &a9, &bf, &a5, &1b, &85, &0a, &84, &4d, &20   ; b9cf: c6 0a 20... .. ...
    equb &97, &8a, &c9, &2c, &d0, &e9, &a5                            ; b9db: 97 8a c9... ......
    equs "MH "                                                        ; b9e2: 4d 48 20    MH    
    equb &82, &95, &f0, &de, &a5, &1b, &85, &0a, &68, &85, &4d, &08   ; b9e5: 82 95 f0... ......
    equb &20, &94, &bd, &a4, &4d, &20, &d7, &ff, &85, &27, &28, &90   ; b9f1: 20 94 bd...  .....
    equb &1b, &a5, &27, &d0, &c2, &20, &d7, &ff, &85, &36, &aa, &f0   ; b9fd: 1b a5 27... ..'...
    equb &09, &20, &d7, &ff, &9d, &ff, &05, &ca, &d0, &f7, &20, &1e   ; ba09: 09 20 d7... . ....
    equb &8c, &4c, &da, &b9, &a5, &27, &f0, &a7, &30, &0c, &a2, &03   ; ba15: 8c 4c da... .L....
    equb &20, &d7, &ff, &95, &2a, &ca, &10, &f8, &30, &0e, &a2, &04   ; ba21: 20 d7 ff...  .....
    equb &20, &d7, &ff, &9d, &6c, &04, &ca, &10, &f7, &20, &b2, &a3   ; ba2d: 20 d7 ff...  .....
    equb &20, &b4, &b4, &4c, &da, &b9                                 ; ba39: 20 b4 b4...  .....
    equs "hhL"                                                        ; ba3f: 68 68 4c    hhL   
    equb &98, &8b, &20, &97, &8a, &c9, &23, &f0, &84, &c9, &86, &f0   ; ba42: 98 8b 20... .. ...
    equb &03, &c6, &0a, &18                                           ; ba4e: 03 c6 0a... ......
    equs "fMFM"                                                       ; ba52: 66 4d 46... fMF...
    equb &a9, &ff, &85, &4e, &20, &8a, &8e, &b0, &0a, &20, &8a, &8e   ; ba56: a9 ff 85... ......
    equb &90, &fb, &a2, &ff, &86, &4e, &18, &08, &06                  ; ba62: 90 fb a2... ......
    equs "M(fM"                                                       ; ba6b: 4d 28 66... M(f...
    equb &c9, &2c, &f0, &e7, &c9, &3b, &f0, &e3, &c6, &0a, &a5, &4d   ; ba6f: c9 2c f0... .,....
    equb &48, &a5                                                     ; ba7b: 48 a5       H.    
    equs "NH "                                                        ; ba7d: 4e 48 20    NH    
    equb &82, &95, &f0, &bb, &68, &85, &4e, &68, &85, &4d, &a5, &1b   ; ba80: 82 95 f0... ......
    equb &85, &0a, &08                                                ; ba8c: 85 0a 08    ...   
    equs "$Mp"                                                        ; ba8f: 24 4d 70    $Mp   
    equb &06, &a5, &4e, &c9, &ff, &d0, &17, &24, &4d, &10, &05, &a9   ; ba92: 06 a5 4e... ..N...
    equs "? X"                                                        ; ba9e: 3f 20 58    ? X   
    equb &b5, &20, &fc, &bb, &84, &36, &06, &4d, &18                  ; baa1: b5 20 fc... . ....
    equs "fM$Mp"                                                      ; baaa: 66 4d 24... fM$...
    equb &1d, &85, &1b, &a9, &00, &85, &19, &a9, &06, &85, &1a, &20   ; baaf: 1d 85 1b... ......
    equb &ad, &ad, &20, &8c, &8a, &c9, &2c, &f0, &06, &c9, &0d, &d0   ; babb: ad ad 20... .. ...
    equb &f5, &a0, &fe, &c8, &84, &4e, &28, &b0, &0c, &20, &94, &bd   ; bac7: f5 a0 fe... ......
    equb &20, &34, &ac, &20, &b4, &b4, &4c, &5a, &ba, &a9, &00, &85   ; bad3: 20 34 ac...  4....
    equs "' !"                                                        ; badf: 27 20 21    ' !   
    equb &8c, &4c, &5a, &ba, &a0, &00, &84, &3d, &a4, &18, &84, &3e   ; bae2: 8c 4c 5a... .LZ...
    equb &20, &97, &8a, &c6, &0a, &c9, &3a, &f0, &10, &c9, &0d, &f0   ; baee: 20 97 8a...  .....
    equb &0c, &c9, &8b, &f0, &08, &20, &9a, &b9, &a0, &01, &20, &55   ; bafa: 0c c9 8b... ......
    equb &be, &20, &57, &98, &a5, &3d, &85, &1c, &a5, &3e, &85, &1d   ; bb06: be 20 57... . W...
    equb &4c, &9b, &8b, &20, &97, &8a, &c9, &2c, &f0, &03, &4c, &96   ; bb12: 4c 9b 8b... L.....
    equb &8b, &20, &82, &95, &f0, &f1, &b0, &0c, &20, &50, &bb, &20   ; bb1e: 8b 20 82... . ....
    equb &94, &bd, &20, &b1, &b4, &4c, &40, &bb, &20, &50, &bb, &20   ; bb2a: 94 bd 20... .. ...
    equb &94, &bd, &20, &ad, &ad, &85, &27, &20, &1e, &8c, &18, &a5   ; bb36: 94 bd 20... .. ...
    equb &1b, &65, &19, &85, &1c, &a5, &1a, &69, &00, &85, &1d, &4c   ; bb42: 1b 65 19... .e....
    equb &15, &bb, &a5, &1b, &85, &0a, &a5, &1c, &85, &19, &a5, &1d   ; bb4e: 15 bb a5... ......
    equb &85, &1a, &a0, &00, &84, &1b, &20, &8c, &8a, &c9, &2c, &f0   ; bb5a: 85 1a a0... ......
    equb &49, &c9, &dc, &f0, &45, &c9, &0d, &f0, &0b, &20, &8c, &8a   ; bb66: 49 c9 dc... I.....
    equb &c9, &2c, &f0, &3a, &c9, &0d, &d0, &f5, &a4, &1b, &b1, &19   ; bb72: c9 2c f0... .,....
    equb &30, &1c, &c8, &c8, &b1, &19, &aa, &c8, &b1, &19, &c9, &20   ; bb7e: 30 1c c8... 0.....
    equb &f0, &f9, &c9, &dc, &f0, &1d, &8a, &18, &65, &19, &85, &19   ; bb8a: f0 f9 c9... ......
    equb &90, &e2, &e6, &1a, &b0, &de, &00                            ; bb96: 90 e2 e6... ......
    equs "*Out of "                                                   ; bb9d: 2a 4f 75... *Ou...
    equb &dc, &00                                                     ; bba5: dc 00       ..    
    equs "+No "                                                       ; bba7: 2b 4e 6f... +No...
    equb &f5, &00, &c8, &84, &1b, &60, &20, &1d, &9b, &20, &4c, &98   ; bbab: f5 00 c8... ......
    equb &20, &ee, &92, &a6, &24, &f0, &e8, &a5, &2a, &05, &2b, &05   ; bbb7: 20 ee 92...  .....
    equb &2c, &05, &2d, &f0, &05, &c6, &24, &4c, &9b, &8b, &bc, &a3   ; bbc3: 2c 05 2d... ,.-...
    equb &05, &bd, &b7, &05, &4c, &dd, &b8, &00                       ; bbcf: 05 bd b7... ......
    equs ",Too many "                                                 ; bbd7: 2c 54 6f... ,To...
    equb &f5, &73, &00, &a6, &24, &e0, &14, &b0, &ec, &20, &6d, &98   ; bbe1: f5 73 00... .s....
    equb &a5, &0b, &9d, &a4, &05, &a5, &0c, &9d, &b8, &05, &e6, &24   ; bbed: a5 0b 9d... ......
    equb &4c, &a3, &8b, &a0, &00, &a9, &06, &d0, &07                  ; bbf9: 4c a3 8b... L.....
; &bc02 referenced 1 time by &8b08
.sub_cbc02
    jsr cb558                                                         ; bc02: 20 58 b5     X.   
    ldy #0                                                            ; bc05: a0 00       ..    
    lda #7                                                            ; bc07: a9 07       ..    
    sty l0037                                                         ; bc09: 84 37       .7    
    sta l0038                                                         ; bc0b: 85 38       .8    
    lda #&ee                                                          ; bc0d: a9 ee       ..    
    sta l0039                                                         ; bc0f: 85 39       .9    
    lda #&20 ; ' '                                                    ; bc11: a9 20       .     
    sta l003a                                                         ; bc13: 85 3a       .:    
    ldy #&ff                                                          ; bc15: a0 ff       ..    
    sty l003b                                                         ; bc17: 84 3b       .;    
    iny                                                               ; bc19: c8          .     
    ldx #&37 ; '7'                                                    ; bc1a: a2 37       .7    
    tya                                                               ; bc1c: 98          .     
    jsr osword                                                        ; bc1d: 20 f1 ff     ..   
    bcc cbc28                                                         ; bc20: 90 06       ..    
    jmp c9838                                                         ; bc22: 4c 38 98    L8.   
; &bc25 referenced 3 times by &853f, &857b, &b56e
.sub_cbc25
    jsr osnewl                                                        ; bc25: 20 e7 ff     ..   
; &bc28 referenced 2 times by &b55f, &bc20
.cbc28
    lda #0                                                            ; bc28: a9 00       ..    
    sta l001e                                                         ; bc2a: 85 1e       ..    
    rts                                                               ; bc2c: 60          `     
; &bc2d referenced 1 time by &bc8f
.sub_cbc2d
    jsr sub_c9970                                                     ; bc2d: 20 70 99     p.   
    bcs return_25                                                     ; bc30: b0 4e       .N    
    lda l003d                                                         ; bc32: a5 3d       .=    
    sbc #2                                                            ; bc34: e9 02       ..    
    sta l0037                                                         ; bc36: 85 37       .7    
    sta l003d                                                         ; bc38: 85 3d       .=    
    sta l0012                                                         ; bc3a: 85 12       ..    
    lda l003e                                                         ; bc3c: a5 3e       .>    
    sbc #0                                                            ; bc3e: e9 00       ..    
    sta l0038                                                         ; bc40: 85 38       .8    
    sta l0013                                                         ; bc42: 85 13       ..    
    sta l003e                                                         ; bc44: 85 3e       .>    
    ldy #3                                                            ; bc46: a0 03       ..    
    lda (l0037),y                                                     ; bc48: b1 37       .7    
    clc                                                               ; bc4a: 18          .     
    adc l0037                                                         ; bc4b: 65 37       e7    
    sta l0037                                                         ; bc4d: 85 37       .7    
    bcc cbc53                                                         ; bc4f: 90 02       ..    
    inc l0038                                                         ; bc51: e6 38       .8    
; &bc53 referenced 1 time by &bc4f
.cbc53
    ldy #0                                                            ; bc53: a0 00       ..    
; &bc55 referenced 2 times by &bc5e, &bc64
.cbc55
    lda (l0037),y                                                     ; bc55: b1 37       .7    
    sta (l0012),y                                                     ; bc57: 91 12       ..    
    cmp #&0d                                                          ; bc59: c9 0d       ..    
    beq cbc66                                                         ; bc5b: f0 09       ..    
; &bc5d referenced 1 time by &bc79
.cbc5d
    iny                                                               ; bc5d: c8          .     
    bne cbc55                                                         ; bc5e: d0 f5       ..    
    inc l0038                                                         ; bc60: e6 38       .8    
    inc l0013                                                         ; bc62: e6 13       ..    
    bne cbc55                                                         ; bc64: d0 ef       ..    
; &bc66 referenced 1 time by &bc5b
.cbc66
    iny                                                               ; bc66: c8          .     
    bne cbc6d                                                         ; bc67: d0 04       ..    
    inc l0038                                                         ; bc69: e6 38       .8    
    inc l0013                                                         ; bc6b: e6 13       ..    
; &bc6d referenced 1 time by &bc67
.cbc6d
    lda (l0037),y                                                     ; bc6d: b1 37       .7    
    sta (l0012),y                                                     ; bc6f: 91 12       ..    
    bmi cbc7c                                                         ; bc71: 30 09       0.    
    jsr sub_cbc81                                                     ; bc73: 20 81 bc     ..   
    jsr sub_cbc81                                                     ; bc76: 20 81 bc     ..   
    jmp cbc5d                                                         ; bc79: 4c 5d bc    L].   
; &bc7c referenced 1 time by &bc71
.cbc7c
    jsr sub_cbe92                                                     ; bc7c: 20 92 be     ..   
    clc                                                               ; bc7f: 18          .     
; &bc80 referenced 1 time by &bc30
.return_25
    rts                                                               ; bc80: 60          `     
; &bc81 referenced 2 times by &bc73, &bc76
.sub_cbc81
    iny                                                               ; bc81: c8          .     
    bne cbc88                                                         ; bc82: d0 04       ..    
    inc l0013                                                         ; bc84: e6 13       ..    
    inc l0038                                                         ; bc86: e6 38       .8    
; &bc88 referenced 1 time by &bc82
.cbc88
    lda (l0037),y                                                     ; bc88: b1 37       .7    
    sta (l0012),y                                                     ; bc8a: 91 12       ..    
    rts                                                               ; bc8c: 60          `     
; &bc8d referenced 1 time by &8b32
.sub_cbc8d
    sty l003b                                                         ; bc8d: 84 3b       .;    
    jsr sub_cbc2d                                                     ; bc8f: 20 2d bc     -.   
    ldy #7                                                            ; bc92: a0 07       ..    
    sty l003c                                                         ; bc94: 84 3c       .<    
    ldy #0                                                            ; bc96: a0 00       ..    
    lda #&0d                                                          ; bc98: a9 0d       ..    
    cmp (l003b),y                                                     ; bc9a: d1 3b       .;    
    beq return_26                                                     ; bc9c: f0 72       .r    
; &bc9e referenced 1 time by &bca1
.loop_cbc9e
    iny                                                               ; bc9e: c8          .     
    cmp (l003b),y                                                     ; bc9f: d1 3b       .;    
    bne loop_cbc9e                                                    ; bca1: d0 fb       ..    
    iny                                                               ; bca3: c8          .     
    iny                                                               ; bca4: c8          .     
    iny                                                               ; bca5: c8          .     
    sty l003f                                                         ; bca6: 84 3f       .?    
    inc l003f                                                         ; bca8: e6 3f       .?    
    lda l0012                                                         ; bcaa: a5 12       ..    
    sta l0039                                                         ; bcac: 85 39       .9    
    lda l0013                                                         ; bcae: a5 13       ..    
    sta l003a                                                         ; bcb0: 85 3a       .:    
    jsr sub_cbe92                                                     ; bcb2: 20 92 be     ..   
    sta l0037                                                         ; bcb5: 85 37       .7    
    lda l0013                                                         ; bcb7: a5 13       ..    
    sta l0038                                                         ; bcb9: 85 38       .8    
    dey                                                               ; bcbb: 88          .     
    lda l0006                                                         ; bcbc: a5 06       ..    
    cmp l0012                                                         ; bcbe: c5 12       ..    
    lda l0007                                                         ; bcc0: a5 07       ..    
    sbc l0013                                                         ; bcc2: e5 13       ..    
    bcs cbcd6                                                         ; bcc4: b0 10       ..    
    jsr sub_cbe6f                                                     ; bcc6: 20 6f be     o.   
    jsr sub_cbd20                                                     ; bcc9: 20 20 bd      .   
    brk                                                               ; bccc: 00          .     
    equb &00, &86                                                     ; bccd: 00 86       ..    
    equs " space"                                                     ; bccf: 20 73 70...  sp...
    equb &00                                                          ; bcd5: 00          .     
; &bcd6 referenced 2 times by &bcc4, &bcef
.cbcd6
    lda (l0039),y                                                     ; bcd6: b1 39       .9    
    sta (l0037),y                                                     ; bcd8: 91 37       .7    
    tya                                                               ; bcda: 98          .     
    bne cbce1                                                         ; bcdb: d0 04       ..    
    dec l003a                                                         ; bcdd: c6 3a       .:    
    dec l0038                                                         ; bcdf: c6 38       .8    
; &bce1 referenced 1 time by &bcdb
.cbce1
    dey                                                               ; bce1: 88          .     
    tya                                                               ; bce2: 98          .     
    adc l0039                                                         ; bce3: 65 39       e9    
    ldx l003a                                                         ; bce5: a6 3a       .:    
    bcc cbcea                                                         ; bce7: 90 01       ..    
    inx                                                               ; bce9: e8          .     
; &bcea referenced 1 time by &bce7
.cbcea
    cmp l003d                                                         ; bcea: c5 3d       .=    
    txa                                                               ; bcec: 8a          .     
    sbc l003e                                                         ; bced: e5 3e       .>    
    bcs cbcd6                                                         ; bcef: b0 e5       ..    
    sec                                                               ; bcf1: 38          8     
    ldy #1                                                            ; bcf2: a0 01       ..    
    lda l002b                                                         ; bcf4: a5 2b       .+    
    sta (l003d),y                                                     ; bcf6: 91 3d       .=    
    iny                                                               ; bcf8: c8          .     
    lda l002a                                                         ; bcf9: a5 2a       .*    
    sta (l003d),y                                                     ; bcfb: 91 3d       .=    
    iny                                                               ; bcfd: c8          .     
    lda l003f                                                         ; bcfe: a5 3f       .?    
    sta (l003d),y                                                     ; bd00: 91 3d       .=    
    jsr sub_cbe56                                                     ; bd02: 20 56 be     V.   
    ldy #&ff                                                          ; bd05: a0 ff       ..    
; &bd07 referenced 1 time by &bd0e
.loop_cbd07
    iny                                                               ; bd07: c8          .     
    lda (l003b),y                                                     ; bd08: b1 3b       .;    
    sta (l003d),y                                                     ; bd0a: 91 3d       .=    
    cmp #&0d                                                          ; bd0c: c9 0d       ..    
    bne loop_cbd07                                                    ; bd0e: d0 f7       ..    
; &bd10 referenced 1 time by &bc9c
.return_26
    rts                                                               ; bd10: 60          `     
    equb &20, &57, &98, &20, &20, &bd, &a5, &18, &85, &0c, &86, &0b   ; bd11: 20 57 98...  W....
    equb &4c, &0b, &8b                                                ; bd1d: 4c 0b 8b    L..   
; &bd20 referenced 2 times by &8af3, &bcc9
.sub_cbd20
    lda l0012                                                         ; bd20: a5 12       ..    
    sta l0000                                                         ; bd22: 85 00       ..    
    sta l0002                                                         ; bd24: 85 02       ..    
    lda l0013                                                         ; bd26: a5 13       ..    
    sta l0001                                                         ; bd28: 85 01       ..    
    sta l0003                                                         ; bd2a: 85 03       ..    
    jsr sub_cbd3a                                                     ; bd2c: 20 3a bd     :.   
    ldx #&80                                                          ; bd2f: a2 80       ..    
    lda #0                                                            ; bd31: a9 00       ..    
; &bd33 referenced 1 time by &bd37
.loop_cbd33
    sta l047f,x                                                       ; bd33: 9d 7f 04    ...   
    dex                                                               ; bd36: ca          .     
    bne loop_cbd33                                                    ; bd37: d0 fa       ..    
    rts                                                               ; bd39: 60          `     
; &bd3a referenced 2 times by &8b1a, &bd2c
.sub_cbd3a
    lda l0018                                                         ; bd3a: a5 18       ..    
    sta l001d                                                         ; bd3c: 85 1d       ..    
    lda l0006                                                         ; bd3e: a5 06       ..    
    sta l0004                                                         ; bd40: 85 04       ..    
    lda l0007                                                         ; bd42: a5 07       ..    
    sta l0005                                                         ; bd44: 85 05       ..    
    lda #0                                                            ; bd46: a9 00       ..    
    sta l0024                                                         ; bd48: 85 24       .$    
    sta l0026                                                         ; bd4a: 85 26       .&    
    sta l0025                                                         ; bd4c: 85 25       .%    
    sta l001c                                                         ; bd4e: 85 1c       ..    
    rts                                                               ; bd50: 60          `     
; &bd51 referenced 10 times by &9a3e, &9a50, &9c8b, &9cac, &9ce1, &9cff, &9d14, &9d20, &9de9, &9e39
.sub_cbd51
    lda l0004                                                         ; bd51: a5 04       ..    
    sec                                                               ; bd53: 38          8     
    sbc #5                                                            ; bd54: e9 05       ..    
    jsr sub_cbe2e                                                     ; bd56: 20 2e be     ..   
    ldy #0                                                            ; bd59: a0 00       ..    
    lda l0030                                                         ; bd5b: a5 30       .0    
    sta (l0004),y                                                     ; bd5d: 91 04       ..    
    iny                                                               ; bd5f: c8          .     
    lda l002e                                                         ; bd60: a5 2e       ..    
    and #&80                                                          ; bd62: 29 80       ).    
    sta l002e                                                         ; bd64: 85 2e       ..    
    lda l0031                                                         ; bd66: a5 31       .1    
    and #&7f                                                          ; bd68: 29 7f       ).    
    ora l002e                                                         ; bd6a: 05 2e       ..    
    sta (l0004),y                                                     ; bd6c: 91 04       ..    
    iny                                                               ; bd6e: c8          .     
    lda l0032                                                         ; bd6f: a5 32       .2    
    sta (l0004),y                                                     ; bd71: 91 04       ..    
    iny                                                               ; bd73: c8          .     
    lda l0033                                                         ; bd74: a5 33       .3    
    sta (l0004),y                                                     ; bd76: 91 04       ..    
    iny                                                               ; bd78: c8          .     
    lda l0034                                                         ; bd79: a5 34       .4    
    sta (l0004),y                                                     ; bd7b: 91 04       ..    
    rts                                                               ; bd7d: 60          `     
; &bd7e referenced 9 times by &9a47, &9a5c, &9c9b, &9cf1, &9d05, &9d2c, &9df5, &9e4a, &9e6f
.sub_cbd7e
    lda l0004                                                         ; bd7e: a5 04       ..    
    clc                                                               ; bd80: 18          .     
    sta l004b                                                         ; bd81: 85 4b       .K    
    adc #5                                                            ; bd83: 69 05       i.    
    sta l0004                                                         ; bd85: 85 04       ..    
    lda l0005                                                         ; bd87: a5 05       ..    
    sta l004c                                                         ; bd89: 85 4c       .L    
    adc #0                                                            ; bd8b: 69 00       i.    
    sta l0005                                                         ; bd8d: 85 05       ..    
    rts                                                               ; bd8f: 60          `     
    equb &f0, &20, &30, &bd                                           ; bd90: f0 20 30... . 0...
; &bd94 referenced 10 times by &85ac, &8beb, &8bfb, &96ff, &9744, &9aa2, &9b6f, &9b7e, &9dce, &9e1d
.sub_cbd94
    lda l0004                                                         ; bd94: a5 04       ..    
    sec                                                               ; bd96: 38          8     
    sbc #4                                                            ; bd97: e9 04       ..    
    jsr sub_cbe2e                                                     ; bd99: 20 2e be     ..   
    ldy #3                                                            ; bd9c: a0 03       ..    
    lda l002d                                                         ; bd9e: a5 2d       .-    
    sta (l0004),y                                                     ; bda0: 91 04       ..    
    dey                                                               ; bda2: 88          .     
    lda l002c                                                         ; bda3: a5 2c       .,    
    sta (l0004),y                                                     ; bda5: 91 04       ..    
    dey                                                               ; bda7: 88          .     
    lda l002b                                                         ; bda8: a5 2b       .+    
    sta (l0004),y                                                     ; bdaa: 91 04       ..    
    dey                                                               ; bdac: 88          .     
    lda l002a                                                         ; bdad: a5 2a       .*    
    sta (l0004),y                                                     ; bdaf: 91 04       ..    
    rts                                                               ; bdb1: 60          `     
; &bdb2 referenced 2 times by &9ae7, &9c15
.sub_cbdb2
    clc                                                               ; bdb2: 18          .     
    lda l0004                                                         ; bdb3: a5 04       ..    
    sbc l0036                                                         ; bdb5: e5 36       .6    
    jsr sub_cbe2e                                                     ; bdb7: 20 2e be     ..   
    ldy l0036                                                         ; bdba: a4 36       .6    
    beq cbdc6                                                         ; bdbc: f0 08       ..    
; &bdbe referenced 1 time by &bdc4
.loop_cbdbe
    lda l05ff,y                                                       ; bdbe: b9 ff 05    ...   
    sta (l0004),y                                                     ; bdc1: 91 04       ..    
    dey                                                               ; bdc3: 88          .     
    bne loop_cbdbe                                                    ; bdc4: d0 f8       ..    
; &bdc6 referenced 1 time by &bdbc
.cbdc6
    lda l0036                                                         ; bdc6: a5 36       .6    
    sta (l0004),y                                                     ; bdc8: 91 04       ..    
    rts                                                               ; bdca: 60          `     
; &bdcb referenced 1 time by &9c37
.sub_cbdcb
    ldy #0                                                            ; bdcb: a0 00       ..    
    lda (l0004),y                                                     ; bdcd: b1 04       ..    
    sta l0036                                                         ; bdcf: 85 36       .6    
    beq cbddc                                                         ; bdd1: f0 09       ..    
    tay                                                               ; bdd3: a8          .     
; &bdd4 referenced 1 time by &bdda
.loop_cbdd4
    lda (l0004),y                                                     ; bdd4: b1 04       ..    
    sta l05ff,y                                                       ; bdd6: 99 ff 05    ...   
    dey                                                               ; bdd9: 88          .     
    bne loop_cbdd4                                                    ; bdda: d0 f8       ..    
; &bddc referenced 2 times by &9b16, &bdd1
.cbddc
    ldy #0                                                            ; bddc: a0 00       ..    
    lda (l0004),y                                                     ; bdde: b1 04       ..    
    sec                                                               ; bde0: 38          8     
    adc l0004                                                         ; bde1: 65 04       e.    
    sta l0004                                                         ; bde3: 85 04       ..    
    bcc return_27                                                     ; bde5: 90 23       .#    
    inc l0005                                                         ; bde7: e6 05       ..    
    rts                                                               ; bde9: 60          `     
; &bdea referenced 6 times by &8c1e, &9a3b, &9ca9, &9cfc, &9d11, &9d78
.sub_cbdea
    ldy #3                                                            ; bdea: a0 03       ..    
    lda (l0004),y                                                     ; bdec: b1 04       ..    
    sta l002d                                                         ; bdee: 85 2d       .-    
    dey                                                               ; bdf0: 88          .     
    lda (l0004),y                                                     ; bdf1: b1 04       ..    
    sta l002c                                                         ; bdf3: 85 2c       .,    
    dey                                                               ; bdf5: 88          .     
    lda (l0004),y                                                     ; bdf6: b1 04       ..    
    sta l002b                                                         ; bdf8: 85 2b       .+    
    dey                                                               ; bdfa: 88          .     
    lda (l0004),y                                                     ; bdfb: b1 04       ..    
    sta l002a                                                         ; bdfd: 85 2a       .*    
; &bdff referenced 2 times by &9b4e, &9b95
.sub_cbdff
    clc                                                               ; bdff: 18          .     
    lda l0004                                                         ; be00: a5 04       ..    
    adc #4                                                            ; be02: 69 04       i.    
    sta l0004                                                         ; be04: 85 04       ..    
    bcc return_27                                                     ; be06: 90 02       ..    
    inc l0005                                                         ; be08: e6 05       ..    
; &be0a referenced 3 times by &bde5, &be06, &be29
.return_27
    rts                                                               ; be0a: 60          `     
; &be0b referenced 1 time by &b4b4
.sub_cbe0b
    ldx #&37 ; '7'                                                    ; be0b: a2 37       .7    
; &be0d referenced 3 times by &970d, &9755, &99dd
.sub_cbe0d
    ldy #3                                                            ; be0d: a0 03       ..    
    lda (l0004),y                                                     ; be0f: b1 04       ..    
    sta l0003,x                                                       ; be11: 95 03       ..    
    dey                                                               ; be13: 88          .     
    lda (l0004),y                                                     ; be14: b1 04       ..    
    sta l0002,x                                                       ; be16: 95 02       ..    
    dey                                                               ; be18: 88          .     
    lda (l0004),y                                                     ; be19: b1 04       ..    
    sta l0001,x                                                       ; be1b: 95 01       ..    
    dey                                                               ; be1d: 88          .     
    lda (l0004),y                                                     ; be1e: b1 04       ..    
    sta l0000,x                                                       ; be20: 95 00       ..    
    clc                                                               ; be22: 18          .     
    lda l0004                                                         ; be23: a5 04       ..    
    adc #4                                                            ; be25: 69 04       i.    
    sta l0004                                                         ; be27: 85 04       ..    
    bcc return_27                                                     ; be29: 90 df       ..    
    inc l0005                                                         ; be2b: e6 05       ..    
    rts                                                               ; be2d: 60          `     
; &be2e referenced 3 times by &bd56, &bd99, &bdb7
.sub_cbe2e
    sta l0004                                                         ; be2e: 85 04       ..    
    bcs cbe34                                                         ; be30: b0 02       ..    
    dec l0005                                                         ; be32: c6 05       ..    
; &be34 referenced 1 time by &be30
.cbe34
    ldy l0005                                                         ; be34: a4 05       ..    
    cpy l0003                                                         ; be36: c4 03       ..    
    bcc cbe41                                                         ; be38: 90 07       ..    
    bne return_28                                                     ; be3a: d0 04       ..    
    cmp l0002                                                         ; be3c: c5 02       ..    
    bcc cbe41                                                         ; be3e: 90 01       ..    
; &be40 referenced 1 time by &be3a
.return_28
    rts                                                               ; be40: 60          `     
; &be41 referenced 2 times by &be38, &be3e
.cbe41
    jmp c8cb7                                                         ; be41: 4c b7 8c    L..   
; &be44 referenced 2 times by &885f, &9d75
.sub_cbe44
    lda l002a                                                         ; be44: a5 2a       .*    
    sta l0000,x                                                       ; be46: 95 00       ..    
    lda l002b                                                         ; be48: a5 2b       .+    
    sta l0001,x                                                       ; be4a: 95 01       ..    
    lda l002c                                                         ; be4c: a5 2c       .,    
    sta l0002,x                                                       ; be4e: 95 02       ..    
    lda l002d                                                         ; be50: a5 2d       .-    
    sta l0003,x                                                       ; be52: 95 03       ..    
    rts                                                               ; be54: 60          `     
    equb &18                                                          ; be55: 18          .     
; &be56 referenced 1 time by &bd02
.sub_cbe56
    tya                                                               ; be56: 98          .     
    adc l003d                                                         ; be57: 65 3d       e=    
    sta l003d                                                         ; be59: 85 3d       .=    
    bcc cbe5f                                                         ; be5b: 90 02       ..    
    inc l003e                                                         ; be5d: e6 3e       .>    
; &be5f referenced 1 time by &be5b
.cbe5f
    ldy #1                                                            ; be5f: a0 01       ..    
    rts                                                               ; be61: 60          `     
    equb &20, &dd, &be, &a8, &a9, &ff, &84, &3d, &a2, &37, &20, &dd   ; be62: 20 dd be...  .....
    equb &ff                                                          ; be6e: ff          .     
; &be6f referenced 1 time by &bcc6
.sub_cbe6f
    lda l0018                                                         ; be6f: a5 18       ..    
    sta l0013                                                         ; be71: 85 13       ..    
    ldy #0                                                            ; be73: a0 00       ..    
    sty l0012                                                         ; be75: 84 12       ..    
    iny                                                               ; be77: c8          .     
; &be78 referenced 1 time by &be8e
.loop_cbe78
    dey                                                               ; be78: 88          .     
    lda (l0012),y                                                     ; be79: b1 12       ..    
    cmp #&0d                                                          ; be7b: c9 0d       ..    
    bne cbe9e                                                         ; be7d: d0 1f       ..    
    iny                                                               ; be7f: c8          .     
    lda (l0012),y                                                     ; be80: b1 12       ..    
    bmi cbe90                                                         ; be82: 30 0c       0.    
    ldy #3                                                            ; be84: a0 03       ..    
    lda (l0012),y                                                     ; be86: b1 12       ..    
    beq cbe9e                                                         ; be88: f0 14       ..    
    clc                                                               ; be8a: 18          .     
    jsr sub_cbe93                                                     ; be8b: 20 93 be     ..   
    bne loop_cbe78                                                    ; be8e: d0 e8       ..    
; &be90 referenced 1 time by &be82
.cbe90
    iny                                                               ; be90: c8          .     
    clc                                                               ; be91: 18          .     
; &be92 referenced 2 times by &bc7c, &bcb2
.sub_cbe92
    tya                                                               ; be92: 98          .     
; &be93 referenced 1 time by &be8b
.sub_cbe93
    adc l0012                                                         ; be93: 65 12       e.    
    sta l0012                                                         ; be95: 85 12       ..    
    bcc cbe9b                                                         ; be97: 90 02       ..    
    inc l0013                                                         ; be99: e6 13       ..    
; &be9b referenced 1 time by &be97
.cbe9b
    ldy #1                                                            ; be9b: a0 01       ..    
    rts                                                               ; be9d: 60          `     
; &be9e referenced 2 times by &be7d, &be88
.cbe9e
    jsr sub_cbfcf                                                     ; be9e: 20 cf bf     ..   
    ora l6142                                                         ; bea1: 0d 42 61    .Ba   
    equs "d program"                                                  ; bea4: 64 20 70... d p...
    equb &0d, &ea, &4c, &f6, &8a, &a9, &00, &85, &37, &a9, &06, &85   ; bead: 0d ea 4c... ..L...
    equb &38                                                          ; beb9: 38          8     
; &beba referenced 1 time by &8ca2
.sub_cbeba
    ldy l0036                                                         ; beba: a4 36       .6    
    lda #&0d                                                          ; bebc: a9 0d       ..    
    sta l0600,y                                                       ; bebe: 99 00 06    ...   
    rts                                                               ; bec1: 60          `     
    equb &20, &d2, &be, &a2, &00, &a0, &06, &20, &f7, &ff, &4c, &9b   ; bec2: 20 d2 be...  .....
    equb &8b, &4c, &0e, &8c, &20, &1d, &9b, &d0, &f8, &20, &b2, &be   ; bece: 8b 4c 0e... .L....
    equb &4c, &4c, &98, &20, &d2, &be, &88, &84, &39, &a5, &18, &85   ; beda: 4c 4c 98... LL....
    equb &3a, &a9, &82, &20, &f4, &ff, &86, &3b, &84, &3c, &a9, &00   ; bee6: 3a a9 82... :.....
    equs "` o"                                                        ; bef2: 60 20 6f    ` o   
    equb &be, &a5, &12, &85, &45, &a5, &13, &85, &46, &a9, &23, &85   ; bef5: be a5 12... ......
    equb &3d, &a9, &80, &85, &3e, &a5, &18, &85, &42, &20, &dd, &be   ; bf01: 3d a9 80... =.....
    equb &86, &3f, &84, &40, &86, &43, &84, &44, &86, &47, &84, &48   ; bf0d: 86 3f 84... .?....
    equb &85, &41, &a8, &a2, &37, &20, &dd, &ff, &4c, &9b, &8b, &20   ; bf19: 85 41 a8... .A....
    equb &62, &be, &4c, &f3, &8a, &20, &62, &be, &4c, &14, &bd, &20   ; bf25: 62 be 4c... b.L...
    equb &a9, &bf, &48, &20, &13, &98, &20, &ee, &92, &68, &a8, &a2   ; bf31: a9 bf 48... ..H...
    equb &2a, &a9, &01, &20, &da, &ff, &4c, &9b, &8b, &38, &a9, &00   ; bf3d: 2a a9 01... *.....
    equs "**H "                                                       ; bf49: 2a 2a 48... **H...
    equb &b5, &bf, &a2                                                ; bf4d: b5 bf a2    ...   
    equs "*h "                                                        ; bf50: 2a 68 20    *h    
    equb &da, &ff, &a9                                                ; bf53: da ff a9    ...   
    equs "@` "                                                        ; bf56: 40 60 20    @`    
    equb &a9, &bf, &48, &20, &ae, &8a, &20, &49, &98, &20, &ee, &92   ; bf59: a9 bf 48... ..H...
    equb &68, &a8, &a5, &2a, &20, &d4, &ff, &4c, &9b, &8b, &20, &b5   ; bf65: 68 a8 a5... h.....
    equb &bf, &20, &d7, &ff, &4c, &d8, &ae, &a9, &40, &d0, &06, &a9   ; bf71: bf 20 d7... . ....
    equb &80, &d0, &02, &a9, &c0, &48, &20, &ec, &ad, &d0, &0e, &20   ; bf7d: 80 d0 02... ......
    equb &ba, &be, &a2, &00, &a0, &06, &68, &20, &ce, &ff, &4c, &d8   ; bf89: ba be a2... ......
    equb &ae, &4c, &0e, &8c, &20, &a9, &bf, &20, &52, &98, &a4, &2a   ; bf95: ae 4c 0e... .L....
    equb &a9, &00, &20, &ce, &ff, &4c, &9b, &8b, &a5, &0a, &85, &1b   ; bfa1: a9 00 20... .. ...
    equb &a5, &0b, &85, &19, &a5, &0c, &85, &1a, &20, &8c, &8a, &c9   ; bfad: a5 0b 85... ......
    equb &23, &d0, &07, &20, &e3, &92, &a4, &2a, &98, &60, &00        ; bfb9: 23 d0 07... #.....
    equs "-Missing #"                                                 ; bfc4: 2d 4d 69... -Mi...
    equb &00                                                          ; bfce: 00          .     
; &bfcf referenced 1 time by &be9e
.sub_cbfcf
    pla                                                               ; bfcf: 68          h     
    sta l0037                                                         ; bfd0: 85 37       .7    
    pla                                                               ; bfd2: 68          h     
    sta l0038                                                         ; bfd3: 85 38       .8    
    ldy #0                                                            ; bfd5: a0 00       ..    
    beq cbfdc                                                         ; bfd7: f0 03       ..    
; &bfd9 referenced 1 time by &bfdf
.loop_cbfd9
    jsr osasci                                                        ; bfd9: 20 e3 ff     ..   
; &bfdc referenced 1 time by &bfd7
.cbfdc
    jsr sub_c894b                                                     ; bfdc: 20 4b 89     K.   
    bpl loop_cbfd9                                                    ; bfdf: 10 f8       ..    
    jmp (l0037)                                                       ; bfe1: 6c 37 00    l7.   
    equb &20, &57, &98, &20, &25, &bc, &a0, &01, &b1, &fd, &f0, &06   ; bfe4: 20 57 98...  W....
    equb &20, &0e, &b5, &c8, &d0, &f6, &4c, &9b, &8b, &00             ; bff0: 20 0e b5...  .....
    equs "Roger"                                                      ; bffa: 52 6f 67... Rog...
    equb &00                                                          ; bfff: 00          .     
.pydis_end

save pydis_start, pydis_end

; Label references by decreasing frequency:
;     l002a:       97
;     l0037:       81
;     l002b:       66
;     l0004:       60
;     l0031:       60
;     l0034:       58
;     l0032:       56
;     l0033:       55
;     l003d:       54
;     l002c:       48
;     l003e:       47
;     l003f:       47
;     l0039:       43
;     l0030:       42
;     l002d:       41
;     l001b:       40
;     l003b:       40
;     l002e:       38
;     l0035:       38
;     l003a:       38
;     l0040:       34
;     l000a:       33
;     l0038:       32
;     l000b:       29
;     l003c:       25
;     c8a97:       24
;     l0036:       24
;     l0041:       23
;     l004b:       23
;     l0019:       22
;     l0027:       21
;     l002f:       19
;     l0012:       18
;     l0002:       15
;     l0042:       15
;     l0005:       13
;     c92f0:       12
;     l0003:       12
;     l0013:       12
;     sub_c8821:   12
;     ca1da:       11
;     l004a:       11
;     ca2be:       10
;     l000c:       10
;     l0028:       10
;     l0600:       10
;     sub_cbd51:   10
;     sub_cbd94:   10
;     c8c0e:        9
;     l0049:        9
;     sub_cbd7e:    9
;     c870d:        8
;     ca099:        8
;     cb558:        8
;     l0048:        8
;     l004c:        8
;     sub_c8944:    8
;     c862b:        7
;     c9bb5:        7
;     sub_c882c:    7
;     sub_ca3b5:    7
;     sub_ca656:    7
;     c9bb4:        6
;     c9c88:        6
;     ca303:        6
;     ca686:        6
;     l004d:        6
;     sub_cbdea:    6
;     c8735:        5
;     c8957:        5
;     c8961:        5
;     c9a93:        5
;     ca208:        5
;     ca5b7:        5
;     cae43:        5
;     l0018:        5
;     l0043:        5
;     l004e:        5
;     l05ff:        5
;     return_16:    5
;     sub_c92fd:    5
;     sub_c9a9d:    5
;     sub_ca21e:    5
;     sub_ca242:    5
;     c8604:        4
;     c88d5:        4
;     c9479:        4
;     c94b3:        4
;     c9641:        4
;     c982a:        4
;     c986d:        4
;     c9c45:        4
;     cadec:        4
;     caeea:        4
;     cb565:        4
;     l0000:        4
;     l0001:        4
;     l001a:        4
;     l001e:        4
;     l0029:        4
;     l0440:        4
;     l0441:        4
;     return_17:    4
;     sub_c8926:    4
;     sub_c9c42:    4
;     sub_c9e20:    4
;     sub_ca34e:    4
;     sub_ca385:    4
;     sub_ca500:    4
;     sub_cad71:    4
;     c8620:        3
;     c8738:        3
;     c8858:        3
;     c8924:        3
;     c8936:        3
;     c89b5:        3
;     c8a8c:        3
;     c8af6:        3
;     c8ba3:        3
;     c8cb7:        3
;     c92f7:        3
;     c961b:        3
;     c9813:        3
;     c9960:        3
;     c99a4:        3
;     c9d0e:        3
;     c9d1d:        3
;     c9dd4:        3
;     ca0e8:        3
;     ca387:        3
;     ca3e4:        3
;     ca590:        3
;     ca724:        3
;     ca76c:        3
;     ca7f7:        3
;     cad7e:        3
;     cad93:        3
;     cae56:        3
;     caea2:        3
;     l0006:        3
;     l0007:        3
;     l0044:        3
;     l0045:        3
;     l0046:        3
;     return_27:    3
;     sub_c882f:    3
;     sub_c8832:    3
;     sub_c894b:    3
;     sub_c92e3:    3
;     sub_c9469:    3
;     sub_c97ba:    3
;     sub_c9b1d:    3
;     sub_c9b29:    3
;     sub_c9dd1:    3
;     sub_ca381:    3
;     sub_ca699:    3
;     sub_cab12:    3
;     sub_cbc25:    3
;     sub_cbe0d:    3
;     sub_cbe2e:    3
;     c8556:        2
;     c8650:        2
;     c866f:        2
;     c8691:        2
;     c86a6:        2
;     c86a8:        2
;     c86c5:        2
;     c86c8:        2
;     c879a:        2
;     c87ed:        2
;     c8810:        2
;     c889d:        2
;     c88da:        2
;     c896a:        2
;     c89c2:        2
;     c89d0:        2
;     c89d2:        2
;     c89e3:        2
;     c8a0d:        2
;     c8a19:        2
;     c8a37:        2
;     c8a54:        2
;     c8b59:        2
;     c8b9b:        2
;     c8bb1:        2
;     c8bbf:        2
;     c8c43:        2
;     c8c5f:        2
;     c8c84:        2
;     c9556:        2
;     c957f:        2
;     c95ff:        2
;     c9677:        2
;     c96d7:        2
;     c97d1:        2
;     c9838:        2
;     c9978:        2
;     c99a7:        2
;     c9a9a:        2
;     c9c9b:        2
;     c9ca1:        2
;     c9d39:        2
;     c9e23:        2
;     c9eb7:        2
;     ca072:        2
;     ca111:        2
;     ca118:        2
;     ca170:        2
;     ca174:        2
;     ca313:        2
;     ca336:        2
;     ca40c:        2
;     ca43c:        2
;     ca4dc:        2
;     ca65c:        2
;     ca66c:        2
;     ca67c:        2
;     ca6bb:        2
;     caab8:        2
;     cad89:        2
;     cb32c:        2
;     cb4ae:        2
;     cb51e:        2
;     cbc28:        2
;     cbc55:        2
;     cbcd6:        2
;     cbddc:        2
;     cbe41:        2
;     cbe9e:        2
;     l000d:        2
;     l000e:        2
;     l000f:        2
;     l0014:        2
;     l0016:        2
;     l0017:        2
;     l0020:        2
;     l0023:        2
;     l0400:        2
;     l0401:        2
;     l043c:        2
;     l043d:        2
;     osbyte:       2
;     return_1:     2
;     return_15:    2
;     return_19:    2
;     return_2:     2
;     return_21:    2
;     return_3:     2
;     return_6:     2
;     return_7:     2
;     return_9:     2
;     sub_c8827:    2
;     sub_c887c:    2
;     sub_c94fc:    2
;     sub_c9531:    2
;     sub_c9582:    2
;     sub_c95dd:    2
;     sub_c96df:    2
;     sub_c9890:    2
;     sub_c99be:    2
;     sub_c9b6b:    2
;     sub_c9b9c:    2
;     sub_c9dce:    2
;     sub_c9e1d:    2
;     sub_ca178:    2
;     sub_ca23f:    2
;     sub_ca3fe:    2
;     sub_ca453:    2
;     sub_ca486:    2
;     sub_ca4fd:    2
;     sub_ca6ad:    2
;     sub_ca7f5:    2
;     sub_ca897:    2
;     sub_cb4b4:    2
;     sub_cb545:    2
;     sub_cb562:    2
;     sub_cbc81:    2
;     sub_cbd20:    2
;     sub_cbd3a:    2
;     sub_cbdb2:    2
;     sub_cbdff:    2
;     sub_cbe44:    2
;     sub_cbe92:    2
;     brkv:         1
;     brkv+1:       1
;     c8063:        1
;     c8504:        1
;     c8508:        1
;     c8536:        1
;     c854c:        1
;     c8565:        1
;     c8577:        1
;     c857b:        1
;     c857e:        1
;     c858c:        1
;     c859f:        1
;     c85a2:        1
;     c85f1:        1
;     c8601:        1
;     c8607:        1
;     c8643:        1
;     c865b:        1
;     c8665:        1
;     c8673:        1
;     c86a5:        1
;     c86ad:        1
;     c86b2:        1
;     c86b7:        1
;     c86cc:        1
;     c86d3:        1
;     c86da:        1
;     c86fb:        1
;     c8715:        1
;     c873f:        1
;     c8750:        1
;     c8767:        1
;     c876e:        1
;     c8780:        1
;     c8782:        1
;     c8788:        1
;     c8797:        1
;     c879c:        1
;     c879f:        1
;     c87b2:        1
;     c87cc:        1
;     c87de:        1
;     c87f0:        1
;     c8813:        1
;     c883a:        1
;     c886a:        1
;     c8966:        1
;     c897c:        1
;     c898c:        1
;     c8996:        1
;     c89a3:        1
;     c89df:        1
;     c89e9:        1
;     c89ec:        1
;     c89f8:        1
;     c8a18:        1
;     c8a25:        1
;     c8a30:        1
;     c8a48:        1
;     c8a66:        1
;     c8a6d:        1
;     c8a72:        1
;     c8a7f:        1
;     c8a81:        1
;     c8a86:        1
;     c8add:        1
;     c8af3:        1
;     c8b38:        1
;     c8b73:        1
;     c8b96:        1
;     c8bdf:        1
;     c8be9:        1
;     c8bfb:        1
;     c8c0b:        1
;     c8ca2:        1
;     c8cb4:        1
;     c8e98:        1
;     c9127:        1
;     c924b:        1
;     c925a:        1
;     c92f4:        1
;     c949a:        1
;     c94a7:        1
;     c94d4:        1
;     c94e1:        1
;     c9516:        1
;     c9541:        1
;     c954d:        1
;     c95a5:        1
;     c95a7:        1
;     c95b0:        1
;     c95bf:        1
;     c960e:        1
;     c9615:        1
;     c962d:        1
;     c9635:        1
;     c9654:        1
;     c9661:        1
;     c9665:        1
;     c9673:        1
;     c967b:        1
;     c967f:        1
;     c9681:        1
;     c969f:        1
;     c96a6:        1
;     c96af:        1
;     c96c9:        1
;     c976c:        1
;     c977d:        1
;     c979b:        1
;     c97a3:        1
;     c97ad:        1
;     c9805:        1
;     c9849:        1
;     c984c:        1
;     c9861:        1
;     c9877:        1
;     c98ac:        1
;     c98b7:        1
;     c98bc:        1
;     c9925:        1
;     c9943:        1
;     c994f:        1
;     c998e:        1
;     c9a33:        1
;     c9a35:        1
;     c9a62:        1
;     c9ae5:        1
;     c9ae7:        1
;     c9aff:        1
;     c9b11:        1
;     c9b15:        1
;     c9b3a:        1
;     c9b55:        1
;     c9b7a:        1
;     c9ba8:        1
;     c9bc0:        1
;     c9bd4:        1
;     c9bdf:        1
;     c9be8:        1
;     c9bfa:        1
;     c9c4e:        1
;     c9c77:        1
;     c9c8b:        1
;     c9ca7:        1
;     c9cb5:        1
;     c9ce1:        1
;     c9cf1:        1
;     c9cfa:        1
;     c9d2c:        1
;     c9d3c:        1
;     c9d4e:        1
;     c9d69:        1
;     c9da6:        1
;     c9dbb:        1
;     c9dbd:        1
;     c9dc6:        1
;     c9de5:        1
;     c9e01:        1
;     c9e0a:        1
;     c9e35:        1
;     c9e59:        1
;     c9e88:        1
;     c9e96:        1
;     c9ebf:        1
;     ca0a0:        1
;     ca0a8:        1
;     ca0c2:        1
;     ca0c8:        1
;     ca0e1:        1
;     ca11b:        1
;     ca11f:        1
;     ca14e:        1
;     ca1ed:        1
;     ca1ff:        1
;     ca20b:        1
;     ca258:        1
;     ca2cd:        1
;     ca2fd:        1
;     ca33a:        1
;     ca37a:        1
;     ca3e1:        1
;     ca466:        1
;     ca468:        1
;     ca491:        1
;     ca4ae:        1
;     ca4b0:        1
;     ca4b3:        1
;     ca53d:        1
;     ca552:        1
;     ca579:        1
;     ca58c:        1
;     ca5df:        1
;     ca5e3:        1
;     ca613:        1
;     ca61d:        1
;     ca625:        1
;     ca652:        1
;     ca659:        1
;     ca676:        1
;     ca6e7:        1
;     ca6f1:        1
;     ca701:        1
;     ca70a:        1
;     ca726:        1
;     ca73f:        1
;     ca76e:        1
;     ca787:        1
;     ca808:        1
;     ca814:        1
;     ca82a:        1
;     ca82c:        1
;     ca8aa:        1
;     caaa2:        1
;     caaac:        1
;     cab1e:        1
;     cab25:        1
;     cad83:        1
;     cadaa:        1
;     cade9:        1
;     cae05:        1
;     cae10:        1
;     cae20:        1
;     cae2a:        1
;     cae30:        1
;     cae61:        1
;     cae6d:        1
;     cae8d:        1
;     caeaa:        1
;     cafc2:        1
;     cb34f:        1
;     cb354:        1
;     cb37f:        1
;     cb384:        1
;     cb3a7:        1
;     cb3ba:        1
;     cb3c0:        1
;     cb4c6:        1
;     cb4e0:        1
;     cb4e9:        1
;     cb536:        1
;     cb542:        1
;     cb556:        1
;     cb567:        1
;     cb571:        1
;     cbc53:        1
;     cbc5d:        1
;     cbc66:        1
;     cbc6d:        1
;     cbc7c:        1
;     cbc88:        1
;     cbce1:        1
;     cbcea:        1
;     cbdc6:        1
;     cbe34:        1
;     cbe5f:        1
;     cbe90:        1
;     cbe9b:        1
;     cbfdc:        1
;     l0010:        1
;     l0011:        1
;     l001c:        1
;     l001d:        1
;     l001f:        1
;     l0021:        1
;     l0022:        1
;     l0024:        1
;     l0025:        1
;     l0026:        1
;     l00ff:        1
;     l01ff:        1
;     l0402:        1
;     l0403:        1
;     l047f:        1
;     l6142:        1
;     l82df:        1
;     l8351:        1
;     l8450:        1
;     l848a:        1
;     l84c4:        1
;     l996b:        1
;     l99b9:        1
;     loop_c84fd:   1
;     loop_c853c:   1
;     loop_c8544:   1
;     loop_c8567:   1
;     loop_c8571:   1
;     loop_c8581:   1
;     loop_c85a5:   1
;     loop_c85d5:   1
;     loop_c85e6:   1
;     loop_c85f5:   1
;     loop_c872f:   1
;     loop_c8864:   1
;     loop_c8867:   1
;     loop_c888d:   1
;     loop_c88ec:   1
;     loop_c8980:   1
;     loop_c89cb:   1
;     loop_c89fe:   1
;     loop_c8b41:   1
;     loop_c8b44:   1
;     loop_c8b47:   1
;     loop_c8b60:   1
;     loop_c8b7d:   1
;     loop_c8b82:   1
;     loop_c8b87:   1
;     loop_c8c97:   1
;     loop_c8ca9:   1
;     loop_c923a:   1
;     loop_c9495:   1
;     loop_c94cf:   1
;     loop_c9507:   1
;     loop_c9527:   1
;     loop_c9533:   1
;     loop_c9595:   1
;     loop_c95d4:   1
;     loop_c96ff:   1
;     loop_c97dd:   1
;     loop_c9821:   1
;     loop_c985a:   1
;     loop_c9929:   1
;     loop_c992e:   1
;     loop_c9948:   1
;     loop_c995a:   1
;     loop_c9980:   1
;     loop_c99f4:   1
;     loop_c9a01:   1
;     loop_c9a39:   1
;     loop_c9a50:   1
;     loop_c9b03:   1
;     loop_c9b2c:   1
;     loop_c9b43:   1
;     loop_c9b4e:   1
;     loop_c9b5e:   1
;     loop_c9b75:   1
;     loop_c9b8a:   1
;     loop_c9c03:   1
;     loop_c9c15:   1
;     loop_c9c2d:   1
;     loop_c9d11:   1
;     loop_c9d20:   1
;     loop_c9d8b:   1
;     loop_c9dcb:   1
;     loop_c9e24:   1
;     loop_c9e6c:   1
;     loop_c9e9a:   1
;     loop_c9eb0:   1
;     loop_ca0f5:   1
;     loop_ca108:   1
;     loop_ca139:   1
;     loop_ca2e6:   1
;     loop_ca3f8:   1
;     loop_ca450:   1
;     loop_ca528:   1
;     loop_ca543:   1
;     loop_ca564:   1
;     loop_ca57f:   1
;     loop_ca629:   1
;     loop_ca63a:   1
;     loop_ca70c:   1
;     loop_ca754:   1
;     loop_ca8b5:   1
;     loop_cad67:   1
;     loop_cad8c:   1
;     loop_cadc9:   1
;     loop_cadcb:   1
;     loop_cadcc:   1
;     loop_cae79:   1
;     loop_cae93:   1
;     loop_caec7:   1
;     loop_cb39d:   1
;     loop_cb3ad:   1
;     loop_cb520:   1
;     loop_cb538:   1
;     loop_cbc9e:   1
;     loop_cbd07:   1
;     loop_cbd33:   1
;     loop_cbdbe:   1
;     loop_cbdd4:   1
;     loop_cbe78:   1
;     loop_cbfd9:   1
;     osasci:       1
;     oscli:        1
;     osnewl:       1
;     osword:       1
;     oswrch:       1
;     return_10:    1
;     return_11:    1
;     return_12:    1
;     return_13:    1
;     return_14:    1
;     return_18:    1
;     return_20:    1
;     return_22:    1
;     return_23:    1
;     return_24:    1
;     return_25:    1
;     return_26:    1
;     return_28:    1
;     return_4:     1
;     return_5:     1
;     return_8:     1
;     sub_c85ba:    1
;     sub_c8897:    1
;     sub_c893d:    1
;     sub_c8c1e:    1
;     sub_c9236:    1
;     sub_c92dd:    1
;     sub_c92fa:    1
;     sub_c95c9:    1
;     sub_c97df:    1
;     sub_c9841:    1
;     sub_c9857:    1
;     sub_c9859:    1
;     sub_c9905:    1
;     sub_c991f:    1
;     sub_c9970:    1
;     sub_c9a9e:    1
;     sub_c9b72:    1
;     sub_ca066:    1
;     sub_ca07b:    1
;     sub_ca140:    1
;     sub_ca14b:    1
;     sub_ca197:    1
;     sub_ca1f4:    1
;     sub_ca24d:    1
;     sub_ca2a4:    1
;     sub_ca2ed:    1
;     sub_ca37d:    1
;     sub_ca46c:    1
;     sub_ca4d0:    1
;     sub_ca4e8:    1
;     sub_ca505:    1
;     sub_ca50b:    1
;     sub_ca606:    1
;     sub_ca6a5:    1
;     sub_ca7e9:    1
;     sub_ca7ed:    1
;     sub_ca7f1:    1
;     sub_ca801:    1
;     sub_caa94:    1
;     sub_caad1:    1
;     sub_caada:    1
;     sub_cae02:    1
;     sub_cae3a:    1
;     sub_caed8:    1
;     sub_caf56:    1
;     sub_cb50e:    1
;     sub_cb550:    1
;     sub_cbc02:    1
;     sub_cbc2d:    1
;     sub_cbc8d:    1
;     sub_cbdcb:    1
;     sub_cbe0b:    1
;     sub_cbe56:    1
;     sub_cbe6f:    1
;     sub_cbe93:    1
;     sub_cbeba:    1
;     sub_cbfcf:    1
;     wrchv:        1

; Automatically generated labels:
;     c8063
;     c8504
;     c8508
;     c8536
;     c854c
;     c8556
;     c8565
;     c8577
;     c857b
;     c857e
;     c858c
;     c859f
;     c85a2
;     c85f1
;     c8601
;     c8604
;     c8607
;     c8620
;     c862b
;     c8643
;     c8650
;     c865b
;     c8665
;     c866f
;     c8673
;     c8691
;     c86a5
;     c86a6
;     c86a8
;     c86ad
;     c86b2
;     c86b7
;     c86c5
;     c86c8
;     c86cc
;     c86d3
;     c86da
;     c86fb
;     c870d
;     c8715
;     c8735
;     c8738
;     c873f
;     c8750
;     c8767
;     c876e
;     c8780
;     c8782
;     c8788
;     c8797
;     c879a
;     c879c
;     c879f
;     c87b2
;     c87cc
;     c87de
;     c87ed
;     c87f0
;     c8810
;     c8813
;     c883a
;     c8858
;     c886a
;     c889d
;     c88d5
;     c88da
;     c8924
;     c8936
;     c8957
;     c8961
;     c8966
;     c896a
;     c897c
;     c898c
;     c8996
;     c89a3
;     c89b5
;     c89c2
;     c89d0
;     c89d2
;     c89df
;     c89e3
;     c89e9
;     c89ec
;     c89f8
;     c8a0d
;     c8a18
;     c8a19
;     c8a25
;     c8a30
;     c8a37
;     c8a48
;     c8a54
;     c8a66
;     c8a6d
;     c8a72
;     c8a7f
;     c8a81
;     c8a86
;     c8a8c
;     c8a97
;     c8add
;     c8af3
;     c8af6
;     c8b38
;     c8b59
;     c8b73
;     c8b96
;     c8b9b
;     c8ba3
;     c8bb1
;     c8bbf
;     c8bdf
;     c8be9
;     c8bfb
;     c8c0b
;     c8c0e
;     c8c43
;     c8c5f
;     c8c84
;     c8ca2
;     c8cb4
;     c8cb7
;     c8e98
;     c9127
;     c924b
;     c925a
;     c92f0
;     c92f4
;     c92f7
;     c9479
;     c949a
;     c94a7
;     c94b3
;     c94d4
;     c94e1
;     c9516
;     c9541
;     c954d
;     c9556
;     c957f
;     c95a5
;     c95a7
;     c95b0
;     c95bf
;     c95ff
;     c960e
;     c9615
;     c961b
;     c962d
;     c9635
;     c9641
;     c9654
;     c9661
;     c9665
;     c9673
;     c9677
;     c967b
;     c967f
;     c9681
;     c969f
;     c96a6
;     c96af
;     c96c9
;     c96d7
;     c976c
;     c977d
;     c979b
;     c97a3
;     c97ad
;     c97d1
;     c9805
;     c9813
;     c982a
;     c9838
;     c9849
;     c984c
;     c9861
;     c986d
;     c9877
;     c98ac
;     c98b7
;     c98bc
;     c9925
;     c9943
;     c994f
;     c9960
;     c9978
;     c998e
;     c99a4
;     c99a7
;     c9a33
;     c9a35
;     c9a62
;     c9a93
;     c9a9a
;     c9ae5
;     c9ae7
;     c9aff
;     c9b11
;     c9b15
;     c9b3a
;     c9b55
;     c9b7a
;     c9ba8
;     c9bb4
;     c9bb5
;     c9bc0
;     c9bd4
;     c9bdf
;     c9be8
;     c9bfa
;     c9c45
;     c9c4e
;     c9c77
;     c9c88
;     c9c8b
;     c9c9b
;     c9ca1
;     c9ca7
;     c9cb5
;     c9ce1
;     c9cf1
;     c9cfa
;     c9d0e
;     c9d1d
;     c9d2c
;     c9d39
;     c9d3c
;     c9d4e
;     c9d69
;     c9da6
;     c9dbb
;     c9dbd
;     c9dc6
;     c9dd4
;     c9de5
;     c9e01
;     c9e0a
;     c9e23
;     c9e35
;     c9e59
;     c9e88
;     c9e96
;     c9eb7
;     c9ebf
;     ca072
;     ca099
;     ca0a0
;     ca0a8
;     ca0c2
;     ca0c8
;     ca0e1
;     ca0e8
;     ca111
;     ca118
;     ca11b
;     ca11f
;     ca14e
;     ca170
;     ca174
;     ca1da
;     ca1ed
;     ca1ff
;     ca208
;     ca20b
;     ca258
;     ca2be
;     ca2cd
;     ca2fd
;     ca303
;     ca313
;     ca336
;     ca33a
;     ca37a
;     ca387
;     ca3e1
;     ca3e4
;     ca40c
;     ca43c
;     ca466
;     ca468
;     ca491
;     ca4ae
;     ca4b0
;     ca4b3
;     ca4dc
;     ca53d
;     ca552
;     ca579
;     ca58c
;     ca590
;     ca5b7
;     ca5df
;     ca5e3
;     ca613
;     ca61d
;     ca625
;     ca652
;     ca659
;     ca65c
;     ca66c
;     ca676
;     ca67c
;     ca686
;     ca6bb
;     ca6e7
;     ca6f1
;     ca701
;     ca70a
;     ca724
;     ca726
;     ca73f
;     ca76c
;     ca76e
;     ca787
;     ca7f7
;     ca808
;     ca814
;     ca82a
;     ca82c
;     ca8aa
;     caaa2
;     caaac
;     caab8
;     cab1e
;     cab25
;     cad7e
;     cad83
;     cad89
;     cad93
;     cadaa
;     cade9
;     cadec
;     cae05
;     cae10
;     cae20
;     cae2a
;     cae30
;     cae43
;     cae56
;     cae61
;     cae6d
;     cae8d
;     caea2
;     caeaa
;     caeea
;     cafc2
;     cb32c
;     cb34f
;     cb354
;     cb37f
;     cb384
;     cb3a7
;     cb3ba
;     cb3c0
;     cb4ae
;     cb4c6
;     cb4e0
;     cb4e9
;     cb51e
;     cb536
;     cb542
;     cb556
;     cb558
;     cb565
;     cb567
;     cb571
;     cbc28
;     cbc53
;     cbc55
;     cbc5d
;     cbc66
;     cbc6d
;     cbc7c
;     cbc88
;     cbcd6
;     cbce1
;     cbcea
;     cbdc6
;     cbddc
;     cbe34
;     cbe41
;     cbe5f
;     cbe90
;     cbe9b
;     cbe9e
;     cbfdc
;     l0000
;     l0001
;     l0002
;     l0003
;     l0004
;     l0005
;     l0006
;     l0007
;     l000a
;     l000b
;     l000c
;     l000d
;     l000e
;     l000f
;     l0010
;     l0011
;     l0012
;     l0013
;     l0014
;     l0016
;     l0017
;     l0018
;     l0019
;     l001a
;     l001b
;     l001c
;     l001d
;     l001e
;     l001f
;     l0020
;     l0021
;     l0022
;     l0023
;     l0024
;     l0025
;     l0026
;     l0027
;     l0028
;     l0029
;     l002a
;     l002b
;     l002c
;     l002d
;     l002e
;     l002f
;     l0030
;     l0031
;     l0032
;     l0033
;     l0034
;     l0035
;     l0036
;     l0037
;     l0038
;     l0039
;     l003a
;     l003b
;     l003c
;     l003d
;     l003e
;     l003f
;     l0040
;     l0041
;     l0042
;     l0043
;     l0044
;     l0045
;     l0046
;     l0048
;     l0049
;     l004a
;     l004b
;     l004c
;     l004d
;     l004e
;     l00ff
;     l01ff
;     l0400
;     l0401
;     l0402
;     l0403
;     l043c
;     l043d
;     l0440
;     l0441
;     l047f
;     l05ff
;     l0600
;     l6142
;     l82df
;     l8351
;     l8450
;     l848a
;     l84c4
;     l996b
;     l99b9
;     loop_c84fd
;     loop_c853c
;     loop_c8544
;     loop_c8567
;     loop_c8571
;     loop_c8581
;     loop_c85a5
;     loop_c85d5
;     loop_c85e6
;     loop_c85f5
;     loop_c872f
;     loop_c8864
;     loop_c8867
;     loop_c888d
;     loop_c88ec
;     loop_c8980
;     loop_c89cb
;     loop_c89fe
;     loop_c8b41
;     loop_c8b44
;     loop_c8b47
;     loop_c8b60
;     loop_c8b7d
;     loop_c8b82
;     loop_c8b87
;     loop_c8c97
;     loop_c8ca9
;     loop_c923a
;     loop_c9495
;     loop_c94cf
;     loop_c9507
;     loop_c9527
;     loop_c9533
;     loop_c9595
;     loop_c95d4
;     loop_c96ff
;     loop_c97dd
;     loop_c9821
;     loop_c985a
;     loop_c9929
;     loop_c992e
;     loop_c9948
;     loop_c995a
;     loop_c9980
;     loop_c99f4
;     loop_c9a01
;     loop_c9a39
;     loop_c9a50
;     loop_c9b03
;     loop_c9b2c
;     loop_c9b43
;     loop_c9b4e
;     loop_c9b5e
;     loop_c9b75
;     loop_c9b8a
;     loop_c9c03
;     loop_c9c15
;     loop_c9c2d
;     loop_c9d11
;     loop_c9d20
;     loop_c9d8b
;     loop_c9dcb
;     loop_c9e24
;     loop_c9e6c
;     loop_c9e9a
;     loop_c9eb0
;     loop_ca0f5
;     loop_ca108
;     loop_ca139
;     loop_ca2e6
;     loop_ca3f8
;     loop_ca450
;     loop_ca528
;     loop_ca543
;     loop_ca564
;     loop_ca57f
;     loop_ca629
;     loop_ca63a
;     loop_ca70c
;     loop_ca754
;     loop_ca8b5
;     loop_cad67
;     loop_cad8c
;     loop_cadc9
;     loop_cadcb
;     loop_cadcc
;     loop_cae79
;     loop_cae93
;     loop_caec7
;     loop_cb39d
;     loop_cb3ad
;     loop_cb520
;     loop_cb538
;     loop_cbc9e
;     loop_cbd07
;     loop_cbd33
;     loop_cbdbe
;     loop_cbdd4
;     loop_cbe78
;     loop_cbfd9
;     return_1
;     return_10
;     return_11
;     return_12
;     return_13
;     return_14
;     return_15
;     return_16
;     return_17
;     return_18
;     return_19
;     return_2
;     return_20
;     return_21
;     return_22
;     return_23
;     return_24
;     return_25
;     return_26
;     return_27
;     return_28
;     return_3
;     return_4
;     return_5
;     return_6
;     return_7
;     return_8
;     return_9
;     sub_c834e
;     sub_c83be
;     sub_c847b
;     sub_c85ba
;     sub_c8821
;     sub_c8827
;     sub_c882c
;     sub_c882f
;     sub_c8832
;     sub_c887c
;     sub_c8897
;     sub_c8926
;     sub_c893d
;     sub_c8944
;     sub_c894b
;     sub_c8c1e
;     sub_c9236
;     sub_c92dd
;     sub_c92e3
;     sub_c92fa
;     sub_c92fd
;     sub_c9469
;     sub_c94fc
;     sub_c9531
;     sub_c9582
;     sub_c95c9
;     sub_c95dd
;     sub_c96df
;     sub_c97ba
;     sub_c97df
;     sub_c9841
;     sub_c9857
;     sub_c9859
;     sub_c9890
;     sub_c9905
;     sub_c991f
;     sub_c9970
;     sub_c99be
;     sub_c9a9d
;     sub_c9a9e
;     sub_c9b1d
;     sub_c9b29
;     sub_c9b6b
;     sub_c9b72
;     sub_c9b9c
;     sub_c9c42
;     sub_c9dce
;     sub_c9dd1
;     sub_c9e1d
;     sub_c9e20
;     sub_ca066
;     sub_ca07b
;     sub_ca140
;     sub_ca14b
;     sub_ca178
;     sub_ca197
;     sub_ca1f4
;     sub_ca21e
;     sub_ca23f
;     sub_ca242
;     sub_ca24d
;     sub_ca2a4
;     sub_ca2ed
;     sub_ca34e
;     sub_ca37d
;     sub_ca381
;     sub_ca385
;     sub_ca3b5
;     sub_ca3fe
;     sub_ca453
;     sub_ca46c
;     sub_ca486
;     sub_ca4d0
;     sub_ca4e8
;     sub_ca4fd
;     sub_ca500
;     sub_ca505
;     sub_ca50b
;     sub_ca606
;     sub_ca656
;     sub_ca699
;     sub_ca6a5
;     sub_ca6ad
;     sub_ca7e9
;     sub_ca7ed
;     sub_ca7f1
;     sub_ca7f5
;     sub_ca801
;     sub_ca897
;     sub_caa94
;     sub_caad1
;     sub_caada
;     sub_cab12
;     sub_cad71
;     sub_cae02
;     sub_cae3a
;     sub_caed8
;     sub_caf56
;     sub_cb4b4
;     sub_cb50e
;     sub_cb545
;     sub_cb550
;     sub_cb562
;     sub_cbc02
;     sub_cbc25
;     sub_cbc2d
;     sub_cbc81
;     sub_cbc8d
;     sub_cbd20
;     sub_cbd3a
;     sub_cbd51
;     sub_cbd7e
;     sub_cbd94
;     sub_cbdb2
;     sub_cbdcb
;     sub_cbdea
;     sub_cbdff
;     sub_cbe0b
;     sub_cbe0d
;     sub_cbe2e
;     sub_cbe44
;     sub_cbe56
;     sub_cbe6f
;     sub_cbe92
;     sub_cbe93
;     sub_cbeba
;     sub_cbfcf

; Stats:
;     Total size (Code + Data) = 16384 bytes
;     Code                     = 7799 bytes (48%)
;     Data                     = 8585 bytes (52%)
;
;     Number of instructions   = 3985
;     Number of data bytes     = 7289 bytes
;     Number of data words     = 0 bytes
;     Number of string bytes   = 1296 bytes
;     Number of strings        = 272
