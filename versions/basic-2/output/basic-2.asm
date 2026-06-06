; Constants
osbyte_read_himem                    = &84
osbyte_read_oshwm                    = &83
osword_write_clock                   = &02
osbyte_read_himem_for_mode           = &85
osbyte_read_adc_or_get_buffer_status = &80
osword_read_pixel                    = &09
osbyte_read_text_cursor_pos          = &86
osbyte_check_eof                     = &7f
osword_read_clock                    = &01
osbyte_inkey                         = &81
osbyte_vdu_queue_size                = &da
osbyte_acknowledge_escape            = &7e
osword_envelope                      = &08
osfile_load                          = &ff
osbyte_read_high_order_address       = &82
osfind_close                         = &00

; Memory locations
zp_lomem         = &00
; &00 referenced 6 times by &9274, &aefc, &af56, &bd22, &be20, &be46
l0001            = &01
; &01 referenced 6 times by &927a, &aefe, &af5a, &bd28, &be1b, &be4a
zp_vartop        = &02
; &02 referenced 28 times by &8c2f, &8c4c, &8c61, &8c6f, &90fa, &9108, &9110, &919c, &91a1, &91c8, &91d6, &91eb, &9203, &9276, &93c1, &951a, &9521, &952a, &9534, &953b, &9556, &af5e, &b17d, &b182, &bd24, &be16, &be3c, &be4e
zp_vartop_1      = &03
; &03 referenced 20 times by &8c33, &8c53, &8c64, &8c71, &90ff, &910c, &9112, &91d2, &91e0, &91ed, &927c, &93c4, &9516, &953f, &9541, &af62, &bd2a, &be11, &be36, &be52
zp_stack_ptr     = &04
; &04 referenced 85 times by &8c68, &8ccb, &8cdd, &8ce5, &8cf0, &8cf6, &8d05, &8d0e, &8d13, &8d18, &8d21, &9102, &91e5, &9264, &93ae, &93d1, &9549, &9ab6, &9abd, &9ac4, &9acb, &9add, &9adf, &9af6, &9b08, &9b43, &9b5e, &9b8a, &9c23, &9c5e, &9c65, &9c6c, &9c73, &9c7a, &9c7e, &9cc5, &9ccc, &9cd3, &9cda, &9e5c, &ac03, &ad21, &ad2a, &b19c, &b1a4, &b1ab, &b232, &b238, &b242, &b244, &bd40, &bd51, &bd5d, &bd6c, &bd71, &bd76, &bd7b, &bd7e, &bd85, &bd94, &bda0, &bda5, &bdaa, &bdaf, &bdb3, &bdc1, &bdc8, &bdcd, &bdd4, &bdde, &bde1, &bde3, &bdec, &bdf1, &bdf6, &bdfb, &be00, &be04, &be0f, &be14, &be19, &be1e, &be23, &be27, &be2e
zp_stack_ptr_1   = &05
; &05 referenced 21 times by &8c6b, &9104, &91e7, &926a, &93b4, &93d5, &9543, &9ae3, &9c84, &9e60, &ac05, &ad26, &b248, &bd44, &bd87, &bd8d, &bde7, &be08, &be2b, &be32, &be34
zp_himem         = &06
; &06 referenced 8 times by &8028, &8fcb, &9262, &93b0, &93cf, &af03, &bcbc, &bd3e
l0007            = &07
; &07 referenced 8 times by &802a, &8fcd, &9268, &93b6, &93d3, &af05, &bcc0, &bd42
zp_erl           = &08
; &08 referenced 3 times by &afa1, &b3c7, &b3f4
l0009            = &09
; &09 referenced 3 times by &af9f, &b3c9, &b3ef
zp_text_ptr_off  = &0a
; &0a referenced 92 times by &8512, &8517, &8577, &857e, &85d3, &85d5, &85d7, &8617, &8715, &874e, &8780, &8795, &87cc, &8829, &883c, &883e, &8a97, &8a99, &8b28, &8b60, &8b7f, &8b96, &8ba3, &8ba5, &8be2, &8d2b, &8d78, &8da1, &8df6, &8e6d, &8e78, &8f8b, &8f8d, &905f, &906d, &90df, &9149, &916d, &92b7, &92c0, &930c, &9347, &943e, &95d1, &97dd, &97df, &9801, &980f, &9857, &9879, &98b9, &98ce, &98e1, &98f1, &98fe, &9b25, &b13d, &b1b5, &b1f7, &b200, &b22d, &b25d, &b41f, &b58a, &b5cb, &b5d6, &b60d, &b637, &b65c, &b75a, &b81f, &b875, &b8f9, &b91c, &b927, &b942, &b95a, &b96a, &b978, &b97d, &b995, &b9a7, &b9ca, &b9cf, &b9d6, &b9eb, &ba4f, &ba77, &ba8c, &baf1, &bb52, &bfa9
zp_text_ptr      = &0b
; &0b referenced 75 times by &8567, &8582, &8590, &85d9, &861a, &8840, &8a9b, &8afc, &8b1e, &8b63, &8b76, &8b83, &8b9d, &8ba7, &8bbf, &8e70, &9013, &9016, &901c, &9027, &902d, &9030, &9032, &9062, &9134, &9304, &95c9, &97e1, &97ec, &97f4, &97fc, &9807, &985b, &986f, &9871, &9884, &9891, &989c, &98a0, &98af, &98b1, &98f3, &9b1d, &b102, &b118, &b11c, &b123, &b12f, &b132, &b134, &b145, &b17b, &b1b8, &b1ed, &b22a, &b2bc, &b3d7, &b415, &b59d, &b5f1, &b602, &b607, &b639, &b747, &b83c, &b894, &b8c5, &b8dd, &b8ff, &b944, &b96c, &b980, &bbed, &bd1b, &bfad
l000c            = &0c
; &0c referenced 41 times by &8596, &8af8, &8b22, &8b78, &8b8b, &8bc3, &8e74, &900f, &9036, &9066, &9136, &9308, &95cd, &980b, &9875, &988a, &98b5, &9b21, &b0ff, &b114, &b138, &b147, &b180, &b1bb, &b1f2, &b227, &b2b9, &b3d1, &b3e2, &b3fb, &b419, &b5f5, &b749, &b841, &b899, &b8c7, &b8df, &b903, &bbf2, &bd19, &bfb1
zp_rnd_seed      = &0d
; &0d referenced 4 times by &804d, &8059, &af78, &af91
l000e            = &0e
; &0e referenced 3 times by &804f, &805d, &af93
l000f            = &0f
; &0f referenced 4 times by &8051, &8061, &af89, &af95
l0010            = &10
; &10 referenced 2 times by &8053, &af97
l0011            = &11
; &11 referenced 4 times by &804b, &af46, &af8e, &af99
zp_top           = &12
; &12 referenced 21 times by &8ae5, &8ae9, &8aee, &8af1, &8f92, &93c8, &aee6, &bc3a, &bc57, &bc6f, &bc8a, &bcaa, &bcbe, &bd20, &be75, &be79, &be80, &be86, &be93, &be95, &bef6
l0013            = &13
; &13 referenced 15 times by &8ae1, &8f96, &93cb, &aee8, &bc42, &bc62, &bc6b, &bc84, &bcae, &bcb7, &bcc2, &bd26, &be71, &be99, &befa
zp_print_bytes   = &14
; &14 referenced 8 times by &8d85, &8dbf, &8de3, &8df2, &8dfe, &9925, &9951, &b660
zp_print_flag    = &15
; &15 referenced 9 times by &8d87, &8dc1, &8de6, &8def, &91b8, &91c6, &91f1, &9f05, &b0aa
zp_error_vec     = &16
; &16 referenced 6 times by &8b00, &8b0d, &b40d, &b413, &b8e9, &b901
l0017            = &17
; &17 referenced 6 times by &8b04, &8b11, &b411, &b417, &b8ed, &b905
zp_page          = &18
; &18 referenced 16 times by &8031, &8ab9, &8adf, &8f9a, &900d, &9288, &9974, &aec2, &b112, &b3cb, &baea, &bd17, &bd3a, &be6f, &bee3, &bf06
zp_text_ptr2     = &19
; &19 referenced 48 times by &8a90, &8bc1, &8e72, &8ea8, &8eb5, &9306, &95cb, &95d7, &95ee, &95f9, &9606, &9663, &9809, &9817, &9b1f, &9bc3, &9beb, &9e28, &a09a, &a141, &a14c, &a159, &abfa, &ac08, &ac2a, &ac3b, &ac4a, &adb6, &adcc, &addb, &adf0, &ae79, &aede, &af4b, &b1c2, &b205, &b212, &b250, &b263, &bab4, &bb43, &bb56, &bb7c, &bb82, &bb86, &bb92, &bb94, &bfaf
l001a            = &1a
; &1a referenced 22 times by &8bc5, &8e76, &930a, &95cf, &9608, &980d, &9b23, &abfd, &ac0f, &ac27, &ac3e, &ac4e, &b1c4, &b208, &b20f, &b253, &b260, &bab8, &bb47, &bb5a, &bb98, &bfb3
zp_text_ptr2_off = &1b
; &1b referenced 90 times by &8827, &8a8c, &8a8e, &8bc7, &8bd0, &8de9, &8df4, &8e6b, &8e7a, &8eb3, &8eea, &8f0c, &930e, &9345, &95a8, &95b0, &95d5, &9603, &9617, &965f, &9661, &966e, &9683, &96c1, &96e4, &9705, &9811, &9813, &9815, &984d, &9852, &98cc, &9b27, &9b34, &9bc1, &9bd4, &9bdf, &9be9, &9bfa, &9e24, &9e26, &a0e8, &ac00, &ac18, &ac24, &ac41, &ac46, &ac5e, &ac69, &aceb, &acf9, &ade4, &adec, &adee, &ae20, &ae38, &ae59, &ae77, &aea5, &aedc, &aee4, &af0a, &af49, &afd5, &aff7, &b045, &b051, &b09f, &b1be, &b1dc, &b202, &b215, &b24d, &b25b, &b266, &b758, &b81d, &b873, &b924, &b9a5, &b9d4, &b9e9, &ba8a, &bab0, &bb41, &bb50, &bb5e, &bb7a, &bbae, &bfab
zp_data_ptr      = &1c
; &1c referenced 4 times by &bb0c, &bb45, &bb54, &bd4e
l001d            = &1d
; &1d referenced 4 times by &bb10, &bb4b, &bb58, &bd3c
zp_count         = &1e
; &1e referenced 7 times by &851e, &8dab, &8e4c, &aef7, &b56a, &b572, &bc2a
zp_listo         = &1f
; &1f referenced 3 times by &8035, &b577, &b597
zp_trace_flag    = &20
; &20 referenced 5 times by &8ae7, &92b2, &9895, &b405, &b8d2
zp_trace_max     = &21
; &21 referenced 2 times by &92aa, &9907
l0022            = &22
; &22 referenced 2 times by &92ae, &990b
zp_width         = &23
; &23 referenced 3 times by &803e, &b4a9, &b568
zp_repeat_level  = &24
; &24 referenced 5 times by &bbba, &bbc8, &bbe4, &bbf7, &bd48
zp_gosub_level   = &25
; &25 referenced 5 times by &b88e, &b89e, &b8b9, &b8bd, &bd4c
zp_for_level     = &26
; &26 referenced 15 times by &b69a, &b6a5, &b6c3, &b751, &b756, &b769, &b782, &b7d4, &b7f8, &b821, &b83a, &b84a, &b855, &b877, &bd4a
zp_var_type      = &27
; &27 referenced 41 times by &85b2, &8bf1, &8c01, &8d41, &911c, &92ee, &933c, &99cb, &9a39, &9a56, &9a62, &9b37, &9c94, &9ca1, &9ca7, &9cea, &9cfa, &9d26, &9d34, &9d55, &9dc6, &9def, &9dfb, &9f3b, &9f77, &ac2c, &ac73, &b197, &b1b2, &b24a, &b294, &b2dc, &b2e3, &b4bd, &b4e0, &b784, &b9f9, &b9fe, &ba19, &bade, &bb3b
zp_opt_flag      = &28
; &28 referenced 11 times by &84ff, &8506, &8519, &8632, &8691, &881a, &886a, &8873, &8b15, &ae30, &b42d
zp_asm_opcode    = &29
; &29 referenced 4 times by &8623, &8651, &8832, &8837
zp_iwa           = &2a
; &2a referenced 187 times by &867b, &86a6, &8818, &8c29, &8c46, &8c4a, &8c51, &8c5c, &8c76, &8c7d, &8c82, &8c88, &8c8e, &8c93, &8cac, &8cb4, &8d4d, &8e28, &8e4a, &8e5b, &8ef5, &8f2b, &8f48, &8f5e, &8f87, &8ffa, &9052, &90af, &90cf, &90d1, &90f8, &910a, &919a, &91ca, &91cc, &91db, &9222, &9242, &924b, &9255, &9260, &9272, &92a8, &931f, &937d, &93ba, &93f4, &9456, &94aa, &94e4, &95e7, &968e, &9696, &9698, &96e9, &96f1, &972a, &972e, &9760, &9762, &9786, &9788, &978c, &9790, &9792, &979b, &979f, &97a4, &97a6, &97af, &97b1, &97c4, &97f6, &98d0, &9905, &992e, &993d, &9994, &99ea, &9a14, &9ab8, &9aba, &9ad3, &9b45, &9b48, &9b60, &9b63, &9b8c, &9b8f, &9bb5, &9c60, &9c62, &9cc7, &9cc9, &9d93, &9da6, &9e9a, &a12b, &a2cf, &a3f5, &ab36, &ab50, &ab95, &abd8, &acc6, &acd6, &acda, &acf7, &ad14, &ad1a, &ad4d, &ad59, &ad97, &ad99, &ae6f, &ae94, &aeea, &af1c, &af58, &afb2, &afe3, &b008, &b00f, &b01f, &b04a, &b04f, &b079, &b07d, &b07f, &b08b, &b0d7, &b0db, &b0ef, &b1eb, &b1f0, &b270, &b2ce, &b338, &b33d, &b342, &b346, &b348, &b34f, &b355, &b35a, &b35f, &b364, &b369, &b38a, &b392, &b397, &b3ad, &b3c0, &b451, &b464, &b477, &b487, &b4a6, &b4c8, &b595, &b5b5, &b5db, &b609, &b60f, &b6a9, &b6da, &b6ea, &b6ef, &b6f4, &b6f9, &b6fe, &b703, &b708, &b70d, &b777, &b7fa, &b823, &b93b, &ba24, &bbbe, &bcf9, &bdad, &bdfd, &be44, &bf67, &bf9f, &bfbf
zp_iwa_1         = &2b
; &2b referenced 111 times by &8681, &86c8, &8738, &8809, &8efb, &8f4c, &8f62, &8f83, &904c, &90d5, &90fd, &910e, &918b, &919f, &91d0, &91de, &9226, &9246, &924d, &9257, &9266, &9278, &9286, &92ac, &9422, &942a, &94b0, &94ea, &95b5, &95eb, &968b, &969b, &969d, &96ec, &9730, &9734, &9766, &9768, &9784, &978a, &978e, &9795, &9797, &979d, &97a1, &97aa, &97b5, &97b7, &97ba, &97c9, &97fe, &98d2, &9909, &9934, &993b, &997c, &99ec, &9a19, &9abf, &9ac1, &9ad5, &9bb7, &9c67, &9c69, &9cce, &9cd0, &9d4e, &9d69, &9d97, &9da8, &a12f, &a2d3, &a3f1, &ab53, &ab93, &abda, &acc8, &ad37, &ad5b, &ad9c, &ad9e, &ae71, &ae96, &aeec, &af18, &af5c, &afb4, &b26d, &b2d1, &b34a, &b3a7, &b454, &b468, &b4d0, &b5b9, &b5df, &b604, &b614, &b6b0, &b6df, &b77b, &b7ff, &b828, &b933, &b9a9, &b9ad, &bbc0, &bcf4, &bda8, &bdf8, &be48
zp_iwa_2         = &2c
; &2c referenced 70 times by &8bda, &8c21, &8c31, &8c80, &8c95, &8c9a, &8f01, &90f3, &9116, &918f, &922a, &9330, &958e, &95bb, &95f7, &9601, &964c, &96a0, &96b4, &96c5, &96cc, &96d3, &96e6, &977e, &97be, &98d4, &99ee, &9a1e, &9ac6, &9ac8, &9ad7, &9bb9, &9c6e, &9c70, &9cd5, &9cd7, &9d43, &9d5e, &9d9c, &9daa, &a133, &a2d7, &a3ed, &ab5d, &ab91, &abdc, &acca, &ada1, &ada3, &ae73, &ae98, &aef0, &af16, &af60, &b06f, &b077, &b26a, &b2d4, &b30d, &b32c, &b33f, &b4d5, &b6b7, &b804, &b82d, &b935, &bbc2, &bda3, &bdf3, &be4c
zp_iwa_3         = &2d
; &2d referenced 61 times by &8c35, &8c57, &8c79, &8c90, &90f1, &9118, &9191, &922e, &96fd, &971f, &973e, &97c0, &98d6, &99c2, &99d4, &99e8, &9a23, &9aad, &9ab1, &9ad1, &9bbb, &9c75, &9c77, &9cdc, &9d41, &9d5c, &9d6d, &9d7c, &9da2, &9dac, &a121, &a2c4, &a2db, &a3e9, &ab5a, &ab8f, &ab99, &abe0, &accc, &ad1e, &ad2d, &ad71, &ada6, &ada8, &ae75, &ae9a, &aef2, &af12, &af64, &b296, &b2d8, &b2f9, &b33a, &b4da, &b809, &b832, &b937, &bbc4, &bd9e, &bdee, &be50
zp_fwa_sign      = &2e
; &2e referenced 48 times by &92d0, &9a6c, &9ecc, &a0fd, &a1e6, &a1ed, &a21e, &a2cd, &a2e6, &a2f6, &a2fb, &a394, &a398, &a39e, &a3c8, &a3d3, &a3dd, &a468, &a4a3, &a4a5, &a4de, &a590, &a5da, &a632, &a636, &a688, &a6f1, &a6f5, &a8e2, &a911, &a918, &a9e2, &aa07, &aaa2, &ab66, &ac7f, &ad83, &ad87, &af6e, &b366, &b371, &b37b, &b4f0, &b4f4, &b4fa, &bd60, &bd64, &bd6a
zp_fwa_ovf       = &2f
; &2f referenced 20 times by &a0fb, &a1f1, &a1fd, &a21b, &a222, &a256, &a2c2, &a2ea, &a332, &a34a, &a3d1, &a4e2, &a61a, &a623, &a680, &a68a, &a6fe, &a707, &af70, &b36f
zp_fwa_exp       = &30
; &30 referenced 55 times by &9a76, &9e3f, &9ed1, &9f65, &9f7e, &9f8e, &a0f7, &a1ef, &a1f5, &a1f9, &a217, &a226, &a24e, &a252, &a2e1, &a2e8, &a301, &a311, &a32e, &a346, &a38f, &a3cd, &a3fe, &a40c, &a418, &a44c, &a486, &a49d, &a4e6, &a513, &a555, &a58e, &a614, &a61f, &a629, &a62d, &a68c, &a6a1, &a6f8, &a703, &a7c1, &a7c6, &a7e0, &a820, &a82e, &a91b, &a936, &a9d3, &a9ff, &aa94, &abce, &af76, &b36b, &b4eb, &bd5b
zp_fwa_m1        = &31
; &31 referenced 72 times by &9a7c, &9f2b, &9f61, &9f84, &9f92, &a040, &a049, &a04d, &a07d, &a0b4, &a0dd, &a125, &a190, &a194, &a19a, &a1ac, &a1b5, &a1cb, &a1d6, &a1da, &a20d, &a22a, &a271, &a28d, &a2a2, &a2b6, &a2dd, &a2fd, &a303, &a313, &a31b, &a336, &a342, &a39a, &a3e1, &a3e7, &a432, &a438, &a43c, &a481, &a483, &a49f, &a4c2, &a4ea, &a570, &a574, &a57f, &a596, &a5d4, &a5d6, &a5fc, &a68e, &a69e, &a70e, &a738, &a73c, &a74d, &a756, &a780, &a784, &a78f, &a7a4, &a824, &a9f9, &aa05, &aa9c, &af7a, &b37f, &b4f6, &b5dd, &b612, &bd66
zp_fwa_m2        = &32
; &32 referenced 61 times by &9a82, &9f86, &a07f, &a0d9, &a11f, &a18a, &a18e, &a19d, &a1aa, &a1b3, &a1c6, &a1c8, &a1d3, &a1dc, &a20f, &a22e, &a275, &a291, &a29f, &a2b2, &a2d9, &a307, &a319, &a31f, &a340, &a3a2, &a3c3, &a3d5, &a3eb, &a42e, &a434, &a43e, &a47b, &a47d, &a4be, &a4ee, &a56c, &a572, &a581, &a59c, &a5ce, &a5d0, &a5f6, &a5fa, &a690, &a714, &a732, &a736, &a74b, &a75c, &a77a, &a77e, &a78d, &a7a0, &a9f7, &b361, &b373, &b4ff, &b5e1, &b616, &bd6f
zp_fwa_m3        = &33
; &33 referenced 58 times by &9a88, &9f88, &a081, &a0d5, &a131, &a184, &a188, &a1a0, &a1a8, &a1b1, &a1c1, &a1c3, &a1d1, &a1de, &a211, &a232, &a279, &a295, &a2ae, &a2d5, &a309, &a31d, &a323, &a33e, &a3a7, &a3be, &a3d7, &a3ef, &a42a, &a430, &a440, &a475, &a477, &a4ba, &a4f2, &a568, &a56e, &a583, &a5a2, &a5c8, &a5ca, &a5f0, &a5f4, &a692, &a71a, &a72c, &a730, &a749, &a762, &a774, &a778, &a78b, &a79c, &a9f5, &b35c, &b375, &b504, &bd74
zp_fwa_m4        = &34
; &34 referenced 61 times by &9a8e, &9f8a, &a083, &a0d1, &a12d, &a17e, &a182, &a198, &a1a6, &a1af, &a1bc, &a1be, &a1cf, &a1e0, &a213, &a236, &a27d, &a299, &a2aa, &a2d1, &a30b, &a321, &a327, &a33c, &a3ac, &a3b9, &a3d9, &a3f3, &a426, &a42c, &a442, &a46f, &a471, &a494, &a4b6, &a4f6, &a564, &a56a, &a585, &a5a8, &a5c2, &a5c4, &a5ea, &a5ee, &a676, &a67a, &a694, &a720, &a726, &a72a, &a747, &a768, &a76e, &a772, &a789, &a798, &a9f1, &b357, &b377, &b509, &bd79
zp_fwa_rnd       = &35
; &35 referenced 42 times by &9f39, &9f8c, &a073, &a085, &a097, &a0cb, &a0cd, &a129, &a178, &a17c, &a1a3, &a1b7, &a1b9, &a1cd, &a1e2, &a215, &a23a, &a281, &a2a4, &a2a6, &a2c0, &a30d, &a325, &a329, &a33a, &a3cf, &a4fa, &a566, &a587, &a5ae, &a5bc, &a5be, &a5e4, &a5e8, &a65c, &a67e, &a696, &a787, &a794, &aa03, &af72, &b36d
zp_strbuf_len    = &36
; &36 referenced 52 times by &8534, &864c, &8c2b, &8c37, &8c86, &8c9d, &8d64, &8e01, &8e0e, &8e1b, &9af2, &9afa, &9b13, &9c25, &9c2b, &9c3b, &9f01, &a000, &a00f, &a068, &a06f, &abee, &abf0, &ac34, &aca3, &ad31, &ad3e, &ade2, &aed6, &afc7, &afe5, &afe9, &b005, &b011, &b030, &b069, &b074, &b08f, &b0d3, &b0eb, &b0f3, &b0f8, &b38c, &b39b, &b3ba, &ba05, &baa5, &bdb5, &bdba, &bdc6, &bdcf, &beba
zp_general       = &37
; &37 referenced 142 times by &8529, &862e, &87d2, &87e3, &87f4, &8802, &887f, &888b, &8890, &889e, &88e0, &88ec, &88f9, &8902, &8917, &8942, &8944, &894e, &8957, &89b5, &89d2, &8a03, &8a07, &8a32, &8a41, &8a72, &8abf, &8ac1, &8b20, &8bb5, &8bbc, &8cd0, &8cd7, &8ce9, &8cf9, &8d07, &8d10, &8d15, &8d1a, &8d23, &8fa0, &8fb3, &8fba, &8fec, &8ff2, &8ff7, &9045, &9056, &905b, &9064, &90a0, &90a2, &90a4, &913e, &9162, &91d8, &91ef, &91f6, &91fc, &9415, &945d, &946b, &949a, &94d4, &94ef, &94fe, &9528, &955b, &9610, &961b, &9651, &96b6, &9716, &9721, &9726, &973c, &9751, &9776, &97ad, &97c6, &97cb, &994f, &9955, &99d6, &9af0, &9b19, &9c1f, &9c3d, &9d7e, &9db8, &9e15, &9ee8, &9f14, &9f44, &9f5a, &9faf, &9fc3, &9ff8, &a02b, &ac0a, &ad23, &ad42, &ad5f, &b0b1, &b15c, &b1cc, &b399, &b39e, &b3cf, &b3e0, &b3f9, &b490, &b4ca, &b4d3, &b4d8, &b4dd, &b4ed, &b4fc, &b501, &b506, &b50b, &b50e, &b525, &b6f1, &b710, &b716, &b72a, &b779, &b7da, &bc09, &bc36, &bc48, &bc4b, &bc4d, &bc55, &bc6d, &bc88, &bcb5, &bcd8, &beb4, &bfd0, &bfe1
l0038            = &38
; &38 referenced 66 times by &8524, &8536, &8552, &8639, &8886, &88e6, &8948, &8abb, &8b24, &8bba, &8f9c, &9068, &90a8, &9143, &91d4, &91fa, &9201, &9207, &941a, &9615, &9713, &9719, &974e, &9773, &97b3, &99d2, &9e04, &9efb, &9f42, &9f4e, &9f56, &9f67, &9f98, &9fa9, &9fab, &9fb7, &9ff4, &ac11, &ad28, &ad63, &b1d1, &b394, &b3cd, &b3e4, &b3fd, &b516, &b521, &b52c, &b52e, &b538, &b6fb, &b718, &b71d, &b72c, &b77d, &b7df, &bc0b, &bc40, &bc51, &bc60, &bc69, &bc86, &bcb9, &bcdf, &beb8, &bfd3
zp_fileblk       = &39
; &39 referenced 62 times by &8530, &8630, &8654, &8881, &888e, &88e4, &88ee, &89f2, &89f8, &89ff, &8a0e, &8a19, &8a1d, &8a28, &8a2a, &8a39, &8cc1, &8cd4, &8cdf, &8d0a, &8d1d, &8f4a, &8f5c, &8ff4, &8ffc, &8ffe, &916b, &948e, &949e, &94c8, &94d8, &9523, &952c, &9654, &96a7, &96b1, &96ca, &972c, &975e, &99f7, &9a01, &9af8, &9b11, &9d8d, &9dae, &9e0d, &b160, &b1df, &b4b7, &b4cc, &b51a, &b532, &b705, &b71f, &b724, &b72e, &b7e4, &bc0f, &bcac, &bcd6, &bce3, &bee1
l003a            = &3a
; &3a referenced 45 times by &854c, &8643, &865b, &8888, &88ea, &89f6, &8a21, &8a2e, &8cdb, &8f4e, &8f60, &8ff0, &9002, &9006, &9472, &947f, &9484, &9489, &9496, &94a3, &94a8, &94bb, &9501, &9507, &950d, &950f, &9518, &951d, &9551, &9732, &9764, &99f9, &9a03, &9aff, &9b03, &9d8b, &9db0, &9e0f, &b51c, &b542, &bc13, &bcb0, &bcdd, &bce5, &bee5
zp_fwb_sign      = &3b
; &3b referenced 59 times by &8645, &8953, &8990, &899e, &89c4, &89e5, &8a4d, &8a62, &8a69, &8b26, &8f94, &8fb7, &8fbc, &8fc0, &8fc2, &9049, &9050, &9074, &9078, &9477, &9479, &94ac, &94c0, &9505, &9511, &99fb, &9a05, &9a66, &9a6a, &9a70, &9a94, &9e11, &a066, &a06d, &a220, &a361, &a36c, &a376, &a455, &a4dc, &a592, &a5d8, &a634, &a6f3, &a819, &a948, &a9e4, &ac15, &b5a5, &b629, &b66c, &b672, &b676, &bc17, &bc8d, &bc9a, &bc9f, &bd08, &beec
zp_fwb_ovf       = &3c
; &3c referenced 39 times by &8955, &8992, &89ac, &89c6, &89e7, &8a64, &8a6b, &8a84, &8b17, &8f98, &8fc5, &8fc9, &907c, &9481, &94b9, &94be, &94c3, &94d0, &94dd, &94e2, &9710, &9758, &99fd, &9a07, &9e13, &a224, &a366, &a457, &a4e0, &b14f, &b15a, &b165, &b5a7, &b630, &b67c, &b682, &b686, &bc94, &beee
zp_fwb_exp       = &3d
; &3d referenced 65 times by &85c1, &85e7, &85f3, &87b6, &8899, &88ad, &88b9, &88bb, &88c0, &88ca, &88cc, &88fc, &8905, &8909, &8911, &8a3b, &8a49, &8a5c, &9058, &9486, &94b3, &94e6, &9972, &997a, &9982, &9984, &9986, &9992, &999b, &999d, &99e0, &9a09, &9a12, &9a2f, &9a74, &9db4, &a228, &a36a, &a459, &a4e4, &a515, &a553, &a58c, &a616, &a6fa, &a81e, &a944, &a9e6, &b154, &b466, &b5ef, &b8d9, &bae8, &bb0a, &bc32, &bc38, &bcea, &bcf6, &bcfb, &bd00, &bd0a, &be57, &be59, &be68, &bf00
zp_fwb_m1        = &3e
; &3e referenced 55 times by &85e9, &85fd, &889b, &88ab, &88b0, &88b5, &88be, &88c7, &88d0, &88f5, &890b, &905d, &9976, &998a, &99a1, &99e2, &9a0b, &9a17, &9a2c, &9a7a, &9db6, &a192, &a22c, &a242, &a26f, &a289, &a37a, &a422, &a428, &a444, &a45b, &a4e8, &a534, &a538, &a543, &a598, &a5d2, &a63a, &a710, &a73a, &a758, &a782, &a81b, &a946, &ac88, &b46a, &b5f3, &b8db, &baec, &bb0e, &bc3c, &bc44, &bced, &be5d, &bf04
zp_fwb_m2        = &3f
; &3f referenced 55 times by &8522, &8542, &9147, &915e, &917c, &91bb, &923c, &924f, &9723, &992b, &993f, &994b, &9960, &99e4, &9a0d, &9a1c, &9a29, &9a80, &9d87, &9d9a, &9d9e, &9ea0, &9ea8, &9eb3, &9eb7, &a18c, &a230, &a244, &a273, &a28b, &a35c, &a36e, &a41e, &a424, &a446, &a45d, &a4ec, &a530, &a536, &a545, &a59e, &a5cc, &a5f8, &a63c, &a716, &a734, &a75e, &a77c, &ac8a, &b21a, &b222, &bca6, &bca8, &bcfe, &bf0d
zp_fwb_m3        = &40
; &40 referenced 37 times by &91bf, &923a, &9251, &9728, &99e6, &9a0f, &9a21, &9a27, &9a86, &9d89, &9da0, &9da4, &a186, &a234, &a246, &a277, &a28f, &a357, &a370, &a41a, &a420, &a448, &a45f, &a4f0, &a52c, &a532, &a547, &a5a4, &a5c6, &a5f2, &a63e, &a71c, &a72e, &a764, &a776, &ac8c, &bf0f
zp_fwb_m4        = &41
; &41 referenced 25 times by &9a8c, &a180, &a238, &a248, &a27b, &a293, &a352, &a372, &a41c, &a44a, &a461, &a4f4, &a528, &a52e, &a549, &a5aa, &a5c0, &a5ec, &a640, &a722, &a728, &a76a, &a770, &ac8e, &bf19
zp_fwb_rnd       = &42
; &42 referenced 17 times by &9f79, &a17a, &a23c, &a24a, &a27f, &a297, &a364, &a463, &a4f8, &a52a, &a54b, &a5b0, &a5ba, &a5e6, &a62b, &a642, &bf08
zp_fp_temp       = &43
; &43 referenced 6 times by &a164, &a16d, &a64a, &a745, &a7a2, &bf11
l0044            = &44
; &44 referenced 5 times by &a648, &a743, &a79e, &b489, &bf13
l0045            = &45
; &45 referenced 4 times by &a646, &a741, &a79a, &bef8
l0046            = &46
; &46 referenced 4 times by &a644, &a73f, &a796, &befc
l0047            = &47
; &47 referenced 1 time by &bf15
l0048            = &48
; &48 referenced 9 times by &a087, &a0a0, &a0a4, &a0ba, &a0c2, &a0ec, &a8a2, &a8cf, &bf17
l0049            = &49
; &49 referenced 21 times by &9eda, &9f03, &9f34, &9f4a, &9fa5, &9fb3, &9fbd, &9fdb, &a011, &a01a, &a026, &a031, &a089, &a0be, &a0c6, &a0e4, &a0e6, &a0ea, &a102, &a10b, &a114
l004a            = &4a
; &4a referenced 20 times by &9e50, &9e67, &a156, &a166, &a16a, &a170, &a48c, &a496, &a4a9, &a4ae, &a6c4, &a6cd, &a6d9, &a7ca, &a7e2, &a993, &a99e, &a9aa, &a9f3, &aacc
zp_fp_ptr        = &4b
; &4b referenced 31 times by &9e5e, &a350, &a355, &a35a, &a35f, &a368, &a387, &a391, &a3a0, &a3a5, &a3aa, &a3af, &a3b7, &a3bc, &a3c1, &a3c6, &a3cb, &a7d4, &a7db, &a7f7, &a857, &a8ac, &a8c2, &aa4e, &aac3, &abb8, &b76e, &b789, &b85a, &b87c, &bd81
zp_fp_ptr_1      = &4c
; &4c referenced 14 times by &9e62, &a38b, &a7fb, &a85b, &a8b0, &a8ca, &aa52, &aac7, &abba, &b772, &b78d, &b85e, &b880, &bd89
l004d            = &4d
; &4d referenced 28 times by &a897, &a8a0, &a8a4, &a8aa, &a8bc, &a8c0, &b2ad, &b2b1, &b303, &b622, &b645, &b647, &b651, &b9d8, &b9e1, &b9ee, &b9f4, &ba52, &ba54, &ba6a, &ba6d, &ba79, &ba88, &ba8f, &ba99, &baa7, &baaa, &baac
l004e            = &4e
; &4e referenced 19 times by &8071, &9efd, &9f40, &9fa7, &9fe6, &9feb, &a899, &a8a8, &a8ae, &a8c4, &a8c8, &b2af, &b307, &ba58, &ba66, &ba7c, &ba85, &ba93, &bacb
l0061            = &61
; &61 referenced 1 time by &9083
l0064            = &64
; &64 referenced 1 time by &9087
l00c9            = &c9
; &c9 referenced 1 time by &aa59
l00fd            = &fd
; &fd referenced 3 times by &afa8, &b407, &bfec
l00ff            = &ff
; &ff referenced 1 time by &987b
l0100            = &0100
; &0100 referenced 2 times by &b1a8, &b23a
l0106            = &0106
; &0106 referenced 1 time by &9342
l01ff            = &01ff
; &01ff referenced 2 times by &8b4c, &935b
brkv             = &0202
; &0202 referenced 1 time by &8065
wrchv            = &020e
; &020e referenced 2 times by &9458, &b574
resint_at        = &0400
; &0400 referenced 5 times by &8042, &8da6, &8daf, &8dbc, &946f
l0401            = &0401
; &0401 referenced 3 times by &8046, &9474, &9eea
l0402            = &0402
; &0402 referenced 2 times by &8037, &9edf
l0403            = &0403
; &0403 referenced 2 times by &803a, &b0ac
resint_a         = &0404
; &0404 referenced 1 time by &8f22
resint_b         = &0408
resint_c         = &040c
; &040c referenced 1 time by &8f1e
resint_d         = &0410
resint_e         = &0414
resint_f         = &0418
resint_g         = &041c
resint_h         = &0420
resint_i         = &0424
resint_j         = &0428
resint_k         = &042c
resint_l         = &0430
resint_m         = &0434
resint_n         = &0438
resint_o         = &043c
; &043c referenced 2 times by &863d, &8667
l043d            = &043d
; &043d referenced 2 times by &8640, &866c
resint_p         = &0440
; &0440 referenced 4 times by &862b, &865d, &867d, &ae3a
l0441            = &0441
; &0441 referenced 4 times by &8636, &8662, &8683, &ae3d
resint_q         = &0444
resint_r         = &0448
resint_s         = &044c
resint_t         = &0450
resint_u         = &0454
resint_v         = &0458
resint_w         = &045c
resint_x         = &0460
; &0460 referenced 1 time by &8f25
resint_y         = &0464
; &0464 referenced 1 time by &8f28
resint_z         = &0468
fp_temp1         = &046c
; &046c referenced 2 times by &8d59, &ba30
fp_temp2         = &0471
fp_temp3         = &0476
fp_temp4         = &047b
l047f            = &047f
; &047f referenced 1 time by &bd33
var_ptr_table    = &0480
l04f1            = &04f1
; &04f1 referenced 2 times by &b6ab, &b6d7
l04f2            = &04f2
; &04f2 referenced 2 times by &b6b2, &b6dc
l04f3            = &04f3
; &04f3 referenced 2 times by &b6b9, &b6e1
l04f4            = &04f4
; &04f4 referenced 1 time by &b6ec
l04f5            = &04f5
; &04f5 referenced 2 times by &b6f6, &b794
l04f6            = &04f6
; &04f6 referenced 1 time by &b700
l04f7            = &04f7
; &04f7 referenced 2 times by &b70a, &b733
l04f9            = &04f9
; &04f9 referenced 1 time by &b713
l04fa            = &04fa
; &04fa referenced 1 time by &b71a
l04fb            = &04fb
; &04fb referenced 1 time by &b721
l04fc            = &04fc
; &04fc referenced 2 times by &b727, &b736
l04fe            = &04fe
; &04fe referenced 1 time by &b741
l04ff            = &04ff
; &04ff referenced 1 time by &b744
for_gosub_stack  = &0500
; &0500 referenced 1 time by &b7dc
l0501            = &0501
; &0501 referenced 1 time by &b7e1
l0502            = &0502
; &0502 referenced 1 time by &b7e6
l0503            = &0503
; &0503 referenced 1 time by &b825
l0504            = &0504
; &0504 referenced 1 time by &b82a
l0505            = &0505
; &0505 referenced 1 time by &b82f
l0506            = &0506
; &0506 referenced 1 time by &b834
l0508            = &0508
; &0508 referenced 1 time by &b7fc
l0509            = &0509
; &0509 referenced 1 time by &b801
l050a            = &050a
; &050a referenced 1 time by &b806
l050b            = &050b
; &050b referenced 1 time by &b80b
l050d            = &050d
; &050d referenced 1 time by &b83e
l050e            = &050e
; &050e referenced 1 time by &b843
l05a3            = &05a3
; &05a3 referenced 1 time by &bbcd
l05a4            = &05a4
; &05a4 referenced 1 time by &bbef
l05b7            = &05b7
; &05b7 referenced 1 time by &bbd0
l05b8            = &05b8
; &05b8 referenced 1 time by &bbf4
l05cb            = &05cb
; &05cb referenced 1 time by &b8bf
l05cc            = &05cc
; &05cc referenced 1 time by &b896
l05e5            = &05e5
; &05e5 referenced 1 time by &b8c2
l05e6            = &05e6
; &05e6 referenced 1 time by &b89b
l05ff            = &05ff
; &05ff referenced 8 times by &8d6c, &9b0a, &9c2d, &9c30, &abf4, &ba0d, &bdbe, &bdd6
string_work      = &0600
; &0600 referenced 27 times by &8658, &8c97, &8ca9, &8cb1, &8e14, &8edd, &8ef7, &8efd, &8f03, &8f06, &a003, &a06a, &ac38, &aca7, &ad44, &adb8, &add3, &afc2, &b017, &b01a, &b083, &b086, &b0e1, &b0e4, &b3a0, &b3af, &bebe
l06ff            = &06ff
; &06ff referenced 2 times by &8ee0, &8ef1
line_input_buf   = &0700
l3185            = &3185
; &3185 referenced 1 time by &a5ff
l6142            = &6142
; &6142 referenced 1 time by &bea1
l7461            = &7461
; &7461 referenced 1 time by &9089
osfind           = &ffce
; &ffce referenced 2 times by &bf90, &bfa3
osbput           = &ffd4
; &ffd4 referenced 6 times by &8d43, &8d4f, &8d5c, &8d66, &8d6f, &bf69
osbget           = &ffd7
; &ffd7 referenced 6 times by &b9f6, &ba02, &ba0a, &ba21, &ba2d, &bf72
osargs           = &ffda
; &ffda referenced 2 times by &bf40, &bf52
osfile           = &ffdd
; &ffdd referenced 2 times by &be6c, &bf1e
osrdch           = &ffe0
; &ffe0 referenced 2 times by &afb9, &afbf
osasci           = &ffe3
; &ffe3 referenced 1 time by &bfd9
osnewl           = &ffe7
; &ffe7 referenced 1 time by &bc25
oswrch           = &ffee
; &ffee referenced 12 times by &8e33, &8e37, &8ecc, &9388, &93db, &940b, &940f, &9417, &941c, &9424, &942c, &b55c
osword           = &fff1
; &fff1 referenced 5 times by &92d4, &ab63, &aeba, &b49a, &bc1d
osbyte           = &fff4
; &fff4 referenced 11 times by &8025, &802e, &93be, &ab3a, &ab6f, &ab78, &acbe, &afb6, &b423, &b428, &bee9
oscli            = &fff7
; &fff7 referenced 2 times by &8b7a, &bec9


    org &8000

.pydis_start
; BASIC v&01
; ***************************************************************************************
; Sideways ROM header — language-entry slot (3 bytes)
;
; MOS dispatches JMP &8000 on language startup.
;
; Byte 0 is &c9 — the language entry is inline code, not a JMP abs. This ROM declares
; itself a language (rom_type bit 6 set) and the MOS enters by calling &8000 directly, so
; the bytes are executed in place (e.g. BBC BASIC's CMP #1 / BEQ / RTS).
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
    cmp #1                                                            ; 8000: c9 01       ..    
    beq language_startup                                              ; 8002: f0 1f       ..    
    rts                                                               ; 8004: 60          `     
    equb &ea                                                          ; 8005: ea          .     
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
; ***************************************************************************************
; Language startup
;
; Reached from the language entry when the MOS starts BASIC (A = 1). Reads HIMEM and PAGE
; from the MOS, clears the print and formatting state, seeds the random-number generator
; if it is cold, installs the BASIC error handler in BRKV, and jumps to
; start_new_program, which clears any program and enters the immediate ("> ") loop.
; &8023 referenced 1 time by &8002
.language_startup
    lda #osbyte_read_himem                                            ; 8023: a9 84       ..    
    jsr osbyte                                                        ; 8025: 20 f4 ff     ..      ; Read top of available user RAM (HIMEM)
    stx zp_himem                                                      ; 8028: 86 06       ..       ; X and Y contain the address of HIMEM (low, high)
    sty l0007                                                         ; 802a: 84 07       ..    
    lda #osbyte_read_oshwm                                            ; 802c: a9 83       ..    
    jsr osbyte                                                        ; 802e: 20 f4 ff     ..      ; Read top of operating system RAM address (OSHWM)
    sty zp_page                                                       ; 8031: 84 18       ..       ; X and Y contain the address of OSHWM (low, high)
    ldx #0                                                            ; 8033: a2 00       ..    
    stx zp_listo                                                      ; 8035: 86 1f       ..       ; LISTO = 0: no LIST indentation
    stx l0402                                                         ; 8037: 8e 02 04    ...      ; @% high two bytes = 0
    stx l0403                                                         ; 803a: 8e 03 04    ...   
    dex                                                               ; 803d: ca          .     
    stx zp_width                                                      ; 803e: 86 23       .#       ; WIDTH = &FF: no automatic line wrap
    ldx #&0a                                                          ; 8040: a2 0a       ..    
    stx resint_at                                                     ; 8042: 8e 00 04    ...      ; @% = &0000090A: default PRINT format
    dex                                                               ; 8045: ca          .     
    stx l0401                                                         ; 8046: 8e 01 04    ...   
    lda #1                                                            ; 8049: a9 01       ..    
    and l0011                                                         ; 804b: 25 11       %.       ; OR the RND seed bytes (&0D-&11) together
    ora zp_rnd_seed                                                   ; 804d: 05 0d       ..    
    ora l000e                                                         ; 804f: 05 0e       ..    
    ora l000f                                                         ; 8051: 05 0f       ..    
    ora l0010                                                         ; 8053: 05 10       ..    
    bne c8063                                                         ; 8055: d0 0c       ..       ; Seed already non-zero: leave it
    lda #&41 ; 'A'                                                    ; 8057: a9 41       .A       ; Cold seed: set RND to "ARW" (&575241)
    sta zp_rnd_seed                                                   ; 8059: 85 0d       ..    
    lda #&52 ; 'R'                                                    ; 805b: a9 52       .R    
    sta l000e                                                         ; 805d: 85 0e       ..    
    lda #&57 ; 'W'                                                    ; 805f: a9 57       .W    
    sta l000f                                                         ; 8061: 85 0f       ..    
; &8063 referenced 1 time by &8055
.c8063
    lda #2                                                            ; 8063: a9 02       ..       ; Install brk_handler (&B402) into BRKV
    sta brkv                                                          ; 8065: 8d 02 02    ...   
    lda #&b4                                                          ; 8068: a9 b4       ..    
    sta brkv+1                                                        ; 806a: 8d 03 02    ...   
    cli                                                               ; 806d: 58          X        ; Enable IRQs and enter the immediate loop
    jmp start_new_program                                             ; 806e: 4c dd 8a    L..   
; ***************************************************************************************
; Keyword / tokeniser table
;
; Each entry is the keyword in ASCII, then a token byte (bit 7 set), then a flag byte
; that drives tokenising:
;
; bit 0  conditional: do not tokenise if followed by a letter bit 1  enter "middle of
; statement" mode bit 2  enter "start of statement" mode bit 3  FN/PROC: do not tokenise
; the following name bit 4  start tokenising a line number (after GOTO etc.) bit 5  do
; not tokenise the rest of the line (REM, DATA) bit 6  pseudo-variable: add &40 to the
; token at the start of a statement (so e.g. PTR is &8F as a function and &CF as an
; assignment target)
;
; Entries are ordered so that the first acceptable abbreviation of each keyword is
; unambiguous. The table runs to the action-address tables at action_table_lo.
.keyword_table
    eor (l004e,x)                                                     ; 8071: 41 4e       AN    
    equb &44, &80, &00                                                ; 8073: 44 80 00    D..   
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
    equb &d3, &00                                                     ; 836b: d3 00       ..    
.action_table_lo
    equb <(fn_openin)                                                 ; 836d: 78          x     
    equb <(fn_ptr)                                                    ; 836e: 47          G     
    equb <(fn_page)                                                   ; 836f: c0          .     
    equb <(fn_time)                                                   ; 8370: b4          .     
    equb <(fn_lomem)                                                  ; 8371: fc          .     
    equb <(fn_himem)                                                  ; 8372: 03          .     
    equb <(fn_abs)                                                    ; 8373: 6a          j     
    equb <(fn_acs)                                                    ; 8374: d4          .     
    equb <(fn_adval)                                                  ; 8375: 33          3     
    equb <(fn_asc)                                                    ; 8376: 9e          .     
    equb <(fn_asn)                                                    ; 8377: da          .     
    equb <(fn_atn)                                                    ; 8378: 07          .     
    equb <(fn_bget)                                                   ; 8379: 6f          o     
    equb <(fn_cos)                                                    ; 837a: 8d          .     
    equb <(fn_count)                                                  ; 837b: f7          .     
    equb <(fn_deg)                                                    ; 837c: c2          .     
    equb <(fn_erl)                                                    ; 837d: 9f          .     
    equb <(fn_err)                                                    ; 837e: a6          .     
    equb <(fn_eval)                                                   ; 837f: e9          .     
    equb <(fn_exp)                                                    ; 8380: 91          .     
    equb <(fn_ext)                                                    ; 8381: 46          F     
    equb <(fn_false)                                                  ; 8382: ca          .     
    equb <(fn_fn)                                                     ; 8383: 95          .     
    equb <(fn_get)                                                    ; 8384: b9          .     
    equb <(fn_inkey)                                                  ; 8385: ad          .     
    equb <(fn_instr)                                                  ; 8386: e2          .     
    equb <(fn_int)                                                    ; 8387: 78          x     
    equb <(fn_len)                                                    ; 8388: d1          .     
    equb <(fn_ln)                                                     ; 8389: fe          .     
    equb <(fn_log)                                                    ; 838a: a8          .     
    equb <(fn_not)                                                    ; 838b: d1          .     
    equb <(fn_openup)                                                 ; 838c: 80          .     
    equb <(fn_openout)                                                ; 838d: 7c          |     
    equb <(fn_pi)                                                     ; 838e: cb          .     
    equb <(fn_point)                                                  ; 838f: 41          A     
    equb <(fn_pos)                                                    ; 8390: 6d          m     
    equb <(fn_rad)                                                    ; 8391: b1          .     
    equb <(fn_rnd)                                                    ; 8392: 49          I     
    equb <(fn_sgn)                                                    ; 8393: 88          .     
    equb <(fn_sin)                                                    ; 8394: 98          .     
    equb <(fn_sqr)                                                    ; 8395: b4          .     
    equb <(fn_tan)                                                    ; 8396: be          .     
    equb <(fn_to)                                                     ; 8397: dc          .     
    equb <(fn_true)                                                   ; 8398: c4          .     
    equb <(fn_usr)                                                    ; 8399: d2          .     
    equb <(fn_val)                                                    ; 839a: 2f          /     
    equb <(fn_vpos)                                                   ; 839b: 76          v     
    equb <(fn_chrs)                                                   ; 839c: bd          .     
    equb <(fn_gets)                                                   ; 839d: bf          .     
    equb <(fn_inkeys)                                                 ; 839e: 26          &     
    equb <(fn_lefts)                                                  ; 839f: cc          .     
    equb <(fn_mids)                                                   ; 83a0: 39          9     
    equb <(fn_rights)                                                 ; 83a1: ee          .     
    equb <(fn_strs)                                                   ; 83a2: 94          .     
    equb <(fn_strings)                                                ; 83a3: c2          .     
    equb <(fn_eof)                                                    ; 83a4: b8          .     
    equb <(stmt_auto)                                                 ; 83a5: ac          .     
    equb <(stmt_delete)                                               ; 83a6: 31          1     
    equb <(stmt_load)                                                 ; 83a7: 24          $     
    equb <(stmt_list)                                                 ; 83a8: 9c          .     
    equb <(stmt_new)                                                  ; 83a9: da          .     
    equb <(stmt_old)                                                  ; 83aa: b6          .     
    equb <(stmt_renumber)                                             ; 83ab: a3          .     
    equb <(stmt_save)                                                 ; 83ac: f3          .     
    equb <(c982a)                                                     ; 83ad: 2a          *     
    equb <(stmt_ptr)                                                  ; 83ae: 30          0     
    equb <(stmt_page)                                                 ; 83af: 83          .     
    equb <(stmt_time)                                                 ; 83b0: c9          .     
    equb <(stmt_lomem)                                                ; 83b1: 6f          o     
    equb <(stmt_himem)                                                ; 83b2: 5d          ]     
    equb <(stmt_sound)                                                ; 83b3: 4c          L     
    equb <(stmt_bput)                                                 ; 83b4: 58          X     
    equb <(stmt_call)                                                 ; 83b5: d2          .     
    equb <(stmt_chain)                                                ; 83b6: 2a          *     
    equb <(stmt_clear)                                                ; 83b7: 8d          .     
    equb <(stmt_close)                                                ; 83b8: 99          .     
    equb <(stmt_clg)                                                  ; 83b9: bd          .     
    equb <(stmt_cls)                                                  ; 83ba: c4          .     
    equb <(stmt_data)                                                 ; 83bb: 7d          }     
    equb <(stmt_data)                                                 ; 83bc: 7d          }     
    equb <(stmt_dim)                                                  ; 83bd: 2f          /     
    equb <(stmt_draw)                                                 ; 83be: e8          .     
    equb <(stmt_end)                                                  ; 83bf: c8          .     
    equb <(stmt_endproc)                                              ; 83c0: 56          V     
    equb <(stmt_envelope)                                             ; 83c1: 72          r     
    equb <(stmt_for)                                                  ; 83c2: c4          .     
    equb <(stmt_gosub)                                                ; 83c3: 88          .     
    equb <(stmt_goto)                                                 ; 83c4: cc          .     
    equb <(stmt_gcol)                                                 ; 83c5: 7a          z     
    equb <(stmt_if)                                                   ; 83c6: c2          .     
    equb <(stmt_input)                                                ; 83c7: 44          D     
    equb <(stmt_let)                                                  ; 83c8: e4          .     
    equb <(stmt_local)                                                ; 83c9: 23          #     
    equb <(stmt_mode)                                                 ; 83ca: 9a          .     
    equb <(stmt_move)                                                 ; 83cb: e4          .     
    equb <(stmt_next)                                                 ; 83cc: 95          .     
    equb <(stmt_on)                                                   ; 83cd: 15          .     
    equb <(stmt_vdu)                                                  ; 83ce: 2f          /     
    equb <(stmt_plot)                                                 ; 83cf: f1          .     
    equb <(stmt_print)                                                ; 83d0: 9a          .     
    equb <(stmt_proc)                                                 ; 83d1: 04          .     
    equb <(stmt_read)                                                 ; 83d2: 1f          .     
    equb <(stmt_data)                                                 ; 83d3: 7d          }     
    equb <(stmt_repeat)                                               ; 83d4: e4          .     
    equb <(stmt_report)                                               ; 83d5: e4          .     
    equb <(stmt_restore)                                              ; 83d6: e6          .     
    equb <(stmt_return)                                               ; 83d7: b6          .     
    equb <(stmt_run)                                                  ; 83d8: 11          .     
    equb <(stmt_stop)                                                 ; 83d9: d0          .     
    equb <(stmt_colour)                                               ; 83da: 8e          .     
    equb <(stmt_trace)                                                ; 83db: 95          .     
    equb <(stmt_until)                                                ; 83dc: b1          .     
    equb <(stmt_width)                                                ; 83dd: a0          .     
    equb <(stmt_oscli)                                                ; 83de: c2          .     
.action_table_hi
    equb >(fn_openin)                                                 ; 83df: bf          .     
    equb >(fn_ptr)                                                    ; 83e0: bf          .     
    equb >(fn_page)                                                   ; 83e1: ae          .     
    equb >(fn_time)                                                   ; 83e2: ae          .     
    equb >(fn_lomem)                                                  ; 83e3: ae          .     
    equb >(fn_himem)                                                  ; 83e4: af          .     
    equb >(fn_abs)                                                    ; 83e5: ad          .     
    equb >(fn_acs)                                                    ; 83e6: a8          .     
    equb >(fn_adval)                                                  ; 83e7: ab          .     
    equb >(fn_asc)                                                    ; 83e8: ac          .     
    equb >(fn_asn)                                                    ; 83e9: a8          .     
    equb >(fn_atn)                                                    ; 83ea: a9          .     
    equb >(fn_bget)                                                   ; 83eb: bf          .     
    equb >(fn_cos)                                                    ; 83ec: a9          .     
    equb >(fn_count)                                                  ; 83ed: ae          .     
    equb >(fn_deg)                                                    ; 83ee: ab          .     
    equb >(fn_erl)                                                    ; 83ef: af          .     
    equb >(fn_err)                                                    ; 83f0: af          .     
    equb >(fn_eval)                                                   ; 83f1: ab          .     
    equb >(fn_exp)                                                    ; 83f2: aa          .     
    equb >(fn_ext)                                                    ; 83f3: bf          .     
    equb >(fn_false)                                                  ; 83f4: ae          .     
    equb >(fn_fn)                                                     ; 83f5: b1          .     
    equb >(fn_get)                                                    ; 83f6: af          .     
    equb >(fn_inkey)                                                  ; 83f7: ac          .     
    equb >(fn_instr)                                                  ; 83f8: ac          .     
    equb >(fn_int)                                                    ; 83f9: ac          .     
    equb >(fn_len)                                                    ; 83fa: ae          .     
    equb >(fn_ln)                                                     ; 83fb: a7          .     
    equb >(fn_log)                                                    ; 83fc: ab          .     
    equb >(fn_not)                                                    ; 83fd: ac          .     
    equb >(fn_openup)                                                 ; 83fe: bf          .     
    equb >(fn_openout)                                                ; 83ff: bf          .     
    equb >(fn_pi)                                                     ; 8400: ab          .     
    equb >(fn_point)                                                  ; 8401: ab          .     
    equb >(fn_pos)                                                    ; 8402: ab          .     
    equb >(fn_rad)                                                    ; 8403: ab          .     
    equb >(fn_rnd)                                                    ; 8404: af          .     
    equb >(fn_sgn)                                                    ; 8405: ab          .     
    equb >(fn_sin)                                                    ; 8406: a9          .     
    equb >(fn_sqr)                                                    ; 8407: a7          .     
    equb >(fn_tan)                                                    ; 8408: a6          .     
    equb >(fn_to)                                                     ; 8409: ae          .     
    equb >(fn_true)                                                   ; 840a: ac          .     
    equb >(fn_usr)                                                    ; 840b: ab          .     
    equb >(fn_val)                                                    ; 840c: ac          .     
    equb >(fn_vpos)                                                   ; 840d: ab          .     
    equb >(fn_chrs)                                                   ; 840e: b3          .     
    equb >(fn_gets)                                                   ; 840f: af          .     
    equb >(fn_inkeys)                                                 ; 8410: b0          .     
    equb >(fn_lefts)                                                  ; 8411: af          .     
    equb >(fn_mids)                                                   ; 8412: b0          .     
    equb >(fn_rights)                                                 ; 8413: af          .     
    equb >(fn_strs)                                                   ; 8414: b0          .     
    equb >(fn_strings)                                                ; 8415: b0          .     
    equb >(fn_eof)                                                    ; 8416: ac          .     
    equb >(stmt_auto)                                                 ; 8417: 90          .     
    equb >(stmt_delete)                                               ; 8418: 8f          .     
    equb >(stmt_load)                                                 ; 8419: bf          .     
    equb >(stmt_list)                                                 ; 841a: b5          .     
    equb >(stmt_new)                                                  ; 841b: 8a          .     
    equb >(stmt_old)                                                  ; 841c: 8a          .     
    equb >(stmt_renumber)                                             ; 841d: 8f          .     
    equb >(stmt_save)                                                 ; 841e: be          .     
    equb >(c982a)                                                     ; 841f: 98          .     
    equb >(stmt_ptr)                                                  ; 8420: bf          .     
    equb >(stmt_page)                                                 ; 8421: 92          .     
    equb >(stmt_time)                                                 ; 8422: 92          .     
    equb >(stmt_lomem)                                                ; 8423: 92          .     
    equb >(stmt_himem)                                                ; 8424: 92          .     
    equb >(stmt_sound)                                                ; 8425: b4          .     
    equb >(stmt_bput)                                                 ; 8426: bf          .     
    equb >(stmt_call)                                                 ; 8427: 8e          .     
    equb >(stmt_chain)                                                ; 8428: bf          .     
    equb >(stmt_clear)                                                ; 8429: 92          .     
    equb >(stmt_close)                                                ; 842a: bf          .     
    equb >(stmt_clg)                                                  ; 842b: 8e          .     
    equb >(stmt_cls)                                                  ; 842c: 8e          .     
    equb >(stmt_data)                                                 ; 842d: 8b          .     
    equb >(stmt_data)                                                 ; 842e: 8b          .     
    equb >(stmt_dim)                                                  ; 842f: 91          .     
    equb >(stmt_draw)                                                 ; 8430: 93          .     
    equb >(stmt_end)                                                  ; 8431: 8a          .     
    equb >(stmt_endproc)                                              ; 8432: 93          .     
    equb >(stmt_envelope)                                             ; 8433: b4          .     
    equb >(stmt_for)                                                  ; 8434: b7          .     
    equb >(stmt_gosub)                                                ; 8435: b8          .     
    equb >(stmt_goto)                                                 ; 8436: b8          .     
    equb >(stmt_gcol)                                                 ; 8437: 93          .     
    equb >(stmt_if)                                                   ; 8438: 98          .     
    equb >(stmt_input)                                                ; 8439: ba          .     
    equb >(stmt_let)                                                  ; 843a: 8b          .     
    equb >(stmt_local)                                                ; 843b: 93          .     
    equb >(stmt_mode)                                                 ; 843c: 93          .     
    equb >(stmt_move)                                                 ; 843d: 93          .     
    equb >(stmt_next)                                                 ; 843e: b6          .     
    equb >(stmt_on)                                                   ; 843f: b9          .     
    equb >(stmt_vdu)                                                  ; 8440: 94          .     
    equb >(stmt_plot)                                                 ; 8441: 93          .     
    equb >(stmt_print)                                                ; 8442: 8d          .     
    equb >(stmt_proc)                                                 ; 8443: 93          .     
    equb >(stmt_read)                                                 ; 8444: bb          .     
    equb >(stmt_data)                                                 ; 8445: 8b          .     
    equb >(stmt_repeat)                                               ; 8446: bb          .     
    equb >(stmt_report)                                               ; 8447: bf          .     
    equb >(stmt_restore)                                              ; 8448: ba          .     
    equb >(stmt_return)                                               ; 8449: b8          .     
    equb >(stmt_run)                                                  ; 844a: bd          .     
    equb >(stmt_stop)                                                 ; 844b: 8a          .     
    equb >(stmt_colour)                                               ; 844c: 93          .     
    equb >(stmt_trace)                                                ; 844d: 92          .     
    equb >(stmt_until)                                                ; 844e: bb          .     
    equb >(stmt_width)                                                ; 844f: b4          .     
; &8450 referenced 1 time by &85f5
.l8450
    equb >(stmt_oscli)                                                ; 8450: be          .     
    equb &4b, &83, &84, &89, &96, &b8, &b9, &d8, &d9, &f0, &01, &10   ; 8451: 4b 83 84... K.....
    equb &81, &90, &89, &93, &a3, &a4, &a9                            ; 845d: 81 90 89... ......
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
; ***************************************************************************************
; Finish the inline assembler
;
; Leave the inline 6502 assembler (reached at "]") and resume interpreting BASIC.
; &84fd referenced 1 time by &850d
.assembler_exit
    lda #&ff                                                          ; 84fd: a9 ff       ..    
    sta zp_opt_flag                                                   ; 84ff: 85 28       .(    
    jmp c8ba3                                                         ; 8501: 4c a3 8b    L..   
; &8504 referenced 1 time by &8b44
.c8504
    lda #3                                                            ; 8504: a9 03       ..    
    sta zp_opt_flag                                                   ; 8506: 85 28       .(    
; &8508 referenced 1 time by &85a2
.c8508
    jsr skip_spaces                                                   ; 8508: 20 97 8a     ..   
    cmp #&5d ; ']'                                                    ; 850b: c9 5d       .]    
    beq assembler_exit                                                ; 850d: f0 ee       ..    
    jsr c986d                                                         ; 850f: 20 6d 98     m.   
    dec zp_text_ptr_off                                               ; 8512: c6 0a       ..    
    jsr sub_c85ba                                                     ; 8514: 20 ba 85     ..   
    dec zp_text_ptr_off                                               ; 8517: c6 0a       ..    
    lda zp_opt_flag                                                   ; 8519: a5 28       .(    
    lsr a                                                             ; 851b: 4a          J     
    bcc c857e                                                         ; 851c: 90 60       .`    
    lda zp_count                                                      ; 851e: a5 1e       ..    
    adc #4                                                            ; 8520: 69 04       i.    
    sta zp_fwb_m2                                                     ; 8522: 85 3f       .?    
    lda l0038                                                         ; 8524: a5 38       .8    
    jsr sub_cb545                                                     ; 8526: 20 45 b5     E.   
    lda zp_general                                                    ; 8529: a5 37       .7    
    jsr sub_cb562                                                     ; 852b: 20 62 b5     b.   
    ldx #&fc                                                          ; 852e: a2 fc       ..    
    ldy zp_fileblk                                                    ; 8530: a4 39       .9    
    bpl c8536                                                         ; 8532: 10 02       ..    
    ldy zp_strbuf_len                                                 ; 8534: a4 36       .6    
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
    ldx zp_fwb_m2                                                     ; 8542: a6 3f       .?    
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
    lda (zp_text_ptr),y                                               ; 8567: b1 0b       ..    
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
    cpy zp_text_ptr_off                                               ; 8577: c4 0a       ..    
    bcc loop_c8571                                                    ; 8579: 90 f6       ..    
; &857b referenced 1 time by &856f
.c857b
    jsr sub_cbc25                                                     ; 857b: 20 25 bc     %.   
; &857e referenced 1 time by &851c
.c857e
    ldy zp_text_ptr_off                                               ; 857e: a4 0a       ..    
    dey                                                               ; 8580: 88          .     
; &8581 referenced 1 time by &858a
.loop_c8581
    iny                                                               ; 8581: c8          .     
    lda (zp_text_ptr),y                                               ; 8582: b1 0b       ..    
    cmp #&3a ; ':'                                                    ; 8584: c9 3a       .:    
    beq c858c                                                         ; 8586: f0 04       ..    
    cmp #&0d                                                          ; 8588: c9 0d       ..    
    bne loop_c8581                                                    ; 858a: d0 f5       ..    
; &858c referenced 1 time by &8586
.c858c
    jsr c9859                                                         ; 858c: 20 59 98     Y.   
    dey                                                               ; 858f: 88          .     
    lda (zp_text_ptr),y                                               ; 8590: b1 0b       ..    
    cmp #&3a ; ':'                                                    ; 8592: c9 3a       .:    
    beq c85a2                                                         ; 8594: f0 0c       ..    
    lda l000c                                                         ; 8596: a5 0c       ..    
    cmp #7                                                            ; 8598: c9 07       ..    
    bne c859f                                                         ; 859a: d0 03       ..    
    jmp immediate_loop                                                ; 859c: 4c f6 8a    L..   
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
    jsr stack_integer                                                 ; 85ac: 20 94 bd     ..   
    jsr sub_cae3a                                                     ; 85af: 20 3a ae     :.   
    sta zp_var_type                                                   ; 85b2: 85 27       .'    
    jsr sub_cb4b4                                                     ; 85b4: 20 b4 b4     ..   
    jsr sub_c8827                                                     ; 85b7: 20 27 88     '.   
; &85ba referenced 1 time by &8514
.sub_c85ba
    ldx #3                                                            ; 85ba: a2 03       ..    
    jsr skip_spaces                                                   ; 85bc: 20 97 8a     ..   
    ldy #0                                                            ; 85bf: a0 00       ..    
    sty zp_fwb_exp                                                    ; 85c1: 84 3d       .=    
    cmp #&3a ; ':'                                                    ; 85c3: c9 3a       .:    
    beq c862b                                                         ; 85c5: f0 64       .d    
    cmp #&0d                                                          ; 85c7: c9 0d       ..    
    beq c862b                                                         ; 85c9: f0 60       .`    
    cmp #&5c ; '\'                                                    ; 85cb: c9 5c       .\    
    beq c862b                                                         ; 85cd: f0 5c       .\    
    cmp #&2e ; '.'                                                    ; 85cf: c9 2e       ..    
    beq loop_c85a5                                                    ; 85d1: f0 d2       ..    
    dec zp_text_ptr_off                                               ; 85d3: c6 0a       ..    
; &85d5 referenced 1 time by &85ef
.loop_c85d5
    ldy zp_text_ptr_off                                               ; 85d5: a4 0a       ..    
    inc zp_text_ptr_off                                               ; 85d7: e6 0a       ..    
    lda (zp_text_ptr),y                                               ; 85d9: b1 0b       ..    
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
    rol zp_fwb_exp                                                    ; 85e7: 26 3d       &=    
    rol zp_fwb_m1                                                     ; 85e9: 26 3e       &>    
    dey                                                               ; 85eb: 88          .     
    bne loop_c85e6                                                    ; 85ec: d0 f8       ..    
    dex                                                               ; 85ee: ca          .     
    bne loop_c85d5                                                    ; 85ef: d0 e4       ..    
; &85f1 referenced 1 time by &85df
.c85f1
    ldx #&3a ; ':'                                                    ; 85f1: a2 3a       .:    
    lda zp_fwb_exp                                                    ; 85f3: a5 3d       .=    
; &85f5 referenced 1 time by &8602
.loop_c85f5
    cmp l8450,x                                                       ; 85f5: dd 50 84    .P.   
    bne c8601                                                         ; 85f8: d0 07       ..    
    ldy l848a,x                                                       ; 85fa: bc 8a 84    ...   
    cpy zp_fwb_m1                                                     ; 85fd: c4 3e       .>    
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
    inc zp_text_ptr_off                                               ; 8617: e6 0a       ..    
    iny                                                               ; 8619: c8          .     
    lda (zp_text_ptr),y                                               ; 861a: b1 0b       ..    
    cmp #&41 ; 'A'                                                    ; 861c: c9 41       .A    
    bne c8604                                                         ; 861e: d0 e4       ..    
; &8620 referenced 3 times by &85ff, &860b, &8610
.c8620
    lda l84c4,x                                                       ; 8620: bd c4 84    ...   
    sta zp_asm_opcode                                                 ; 8623: 85 29       .)    
    ldy #1                                                            ; 8625: a0 01       ..    
    cpx #&1a                                                          ; 8627: e0 1a       ..    
    bcs c8673                                                         ; 8629: b0 48       .H    
; &862b referenced 7 times by &85c5, &85c9, &85cd, &86aa, &879c, &881e, &8864
.c862b
    lda resint_p                                                      ; 862b: ad 40 04    .@.   
    sta zp_general                                                    ; 862e: 85 37       .7    
    sty zp_fileblk                                                    ; 8630: 84 39       .9    
    ldx zp_opt_flag                                                   ; 8632: a6 28       .(    
    cpx #4                                                            ; 8634: e0 04       ..    
    ldx l0441                                                         ; 8636: ae 41 04    .A.   
    stx l0038                                                         ; 8639: 86 38       .8    
    bcc c8643                                                         ; 863b: 90 06       ..    
    lda resint_o                                                      ; 863d: ad 3c 04    .<.   
    ldx l043d                                                         ; 8640: ae 3d 04    .=.   
; &8643 referenced 1 time by &863b
.c8643
    sta l003a                                                         ; 8643: 85 3a       .:    
    stx zp_fwb_sign                                                   ; 8645: 86 3b       .;    
    tya                                                               ; 8647: 98          .     
    beq return_1                                                      ; 8648: f0 28       .(    
    bpl c8650                                                         ; 864a: 10 04       ..    
    ldy zp_strbuf_len                                                 ; 864c: a4 36       .6    
    beq return_1                                                      ; 864e: f0 22       ."    
; &8650 referenced 2 times by &864a, &8670
.c8650
    dey                                                               ; 8650: 88          .     
    lda zp_asm_opcode,y                                               ; 8651: b9 29 00    .).   
    bit zp_fileblk                                                    ; 8654: 24 39       $9    
    bpl c865b                                                         ; 8656: 10 03       ..    
    lda string_work,y                                                 ; 8658: b9 00 06    ...   
; &865b referenced 1 time by &8656
.c865b
    sta (l003a),y                                                     ; 865b: 91 3a       .:    
    inc resint_p                                                      ; 865d: ee 40 04    .@.   
    bne c8665                                                         ; 8660: d0 03       ..    
    inc l0441                                                         ; 8662: ee 41 04    .A.   
; &8665 referenced 1 time by &8660
.c8665
    bcc c866f                                                         ; 8665: 90 08       ..    
    inc resint_o                                                      ; 8667: ee 3c 04    .<.   
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
    jsr eval_expr_to_integer                                          ; 8677: 20 21 88     !.   
    clc                                                               ; 867a: 18          .     
    lda zp_iwa                                                        ; 867b: a5 2a       .*    
    sbc resint_p                                                      ; 867d: ed 40 04    .@.   
    tay                                                               ; 8680: a8          .     
    lda zp_iwa_1                                                      ; 8681: a5 2b       .+    
    sbc l0441                                                         ; 8683: ed 41 04    .A.   
    cpy #1                                                            ; 8686: c0 01       ..    
    dey                                                               ; 8688: 88          .     
    sbc #0                                                            ; 8689: e9 00       ..    
    beq c86b2                                                         ; 868b: f0 25       .%    
    cmp #&ff                                                          ; 868d: c9 ff       ..    
    beq c86ad                                                         ; 868f: f0 1c       ..    
; &8691 referenced 2 times by &86b0, &86b5
.c8691
    lda zp_opt_flag                                                   ; 8691: a5 28       .(    
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
    sty zp_iwa                                                        ; 86a6: 84 2a       .*    
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
    jsr skip_spaces                                                   ; 86bb: 20 97 8a     ..   
    cmp #&23 ; '#'                                                    ; 86be: c9 23       .#    
    bne c86da                                                         ; 86c0: d0 18       ..    
    jsr sub_c882f                                                     ; 86c2: 20 2f 88     /.   
; &86c5 referenced 2 times by &877d, &87c9
.c86c5
    jsr eval_expr_to_integer                                          ; 86c5: 20 21 88     !.   
; &86c8 referenced 2 times by &86f9, &870b
.c86c8
    lda zp_iwa_1                                                      ; 86c8: a5 2b       .+    
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
    jsr skip_spaces                                                   ; 86d7: 20 97 8a     ..   
; &86da referenced 1 time by &86c0
.c86da
    cmp #&28 ; '('                                                    ; 86da: c9 28       .(    
    bne c8715                                                         ; 86dc: d0 37       .7    
    jsr eval_expr_to_integer                                          ; 86de: 20 21 88     !.   
    jsr skip_spaces                                                   ; 86e1: 20 97 8a     ..   
    cmp #&29 ; ')'                                                    ; 86e4: c9 29       .)    
    bne c86fb                                                         ; 86e6: d0 13       ..    
    jsr skip_spaces                                                   ; 86e8: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 86eb: c9 2c       .,    
    bne c870d                                                         ; 86ed: d0 1e       ..    
    jsr sub_c882c                                                     ; 86ef: 20 2c 88     ,.   
    jsr skip_spaces                                                   ; 86f2: 20 97 8a     ..   
    cmp #&59 ; 'Y'                                                    ; 86f5: c9 59       .Y    
    bne c870d                                                         ; 86f7: d0 14       ..    
    beq c86c8                                                         ; 86f9: f0 cd       ..    
; &86fb referenced 1 time by &86e6
.c86fb
    cmp #&2c ; ','                                                    ; 86fb: c9 2c       .,    
    bne c870d                                                         ; 86fd: d0 0e       ..    
    jsr skip_spaces                                                   ; 86ff: 20 97 8a     ..   
    cmp #&58 ; 'X'                                                    ; 8702: c9 58       .X    
    bne c870d                                                         ; 8704: d0 07       ..    
    jsr skip_spaces                                                   ; 8706: 20 97 8a     ..   
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
    dec zp_text_ptr_off                                               ; 8715: c6 0a       ..    
    jsr eval_expr_to_integer                                          ; 8717: 20 21 88     !.   
    jsr skip_spaces                                                   ; 871a: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 871d: c9 2c       .,    
    bne c8735                                                         ; 871f: d0 14       ..    
    jsr sub_c882c                                                     ; 8721: 20 2c 88     ,.   
    jsr skip_spaces                                                   ; 8724: 20 97 8a     ..   
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
    lda zp_iwa_1                                                      ; 8738: a5 2b       .+    
    bne loop_c872f                                                    ; 873a: d0 f3       ..    
    jmp c86a8                                                         ; 873c: 4c a8 86    L..   
; &873f referenced 1 time by &86d5
.c873f
    cpx #&2f ; '/'                                                    ; 873f: e0 2f       ./    
    bcs c876e                                                         ; 8741: b0 2b       .+    
    cpx #&2d ; '-'                                                    ; 8743: e0 2d       .-    
    bcs c8750                                                         ; 8745: b0 09       ..    
    jsr skip_spaces                                                   ; 8747: 20 97 8a     ..   
    cmp #&41 ; 'A'                                                    ; 874a: c9 41       .A    
    beq c8767                                                         ; 874c: f0 19       ..    
    dec zp_text_ptr_off                                               ; 874e: c6 0a       ..    
; &8750 referenced 1 time by &8745
.c8750
    jsr eval_expr_to_integer                                          ; 8750: 20 21 88     !.   
    jsr skip_spaces                                                   ; 8753: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 8756: c9 2c       .,    
    bne c8738                                                         ; 8758: d0 de       ..    
    jsr sub_c882c                                                     ; 875a: 20 2c 88     ,.   
    jsr skip_spaces                                                   ; 875d: 20 97 8a     ..   
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
    jsr skip_spaces                                                   ; 8776: 20 97 8a     ..   
    cmp #&23 ; '#'                                                    ; 8779: c9 23       .#    
    bne c8780                                                         ; 877b: d0 03       ..    
    jmp c86c5                                                         ; 877d: 4c c5 86    L..   
; &8780 referenced 1 time by &877b
.c8780
    dec zp_text_ptr_off                                               ; 8780: c6 0a       ..    
; &8782 referenced 1 time by &8774
.c8782
    jsr eval_expr_to_integer                                          ; 8782: 20 21 88     !.   
    jmp c8735                                                         ; 8785: 4c 35 87    L5.   
; &8788 referenced 1 time by &8770
.c8788
    cpx #&33 ; '3'                                                    ; 8788: e0 33       .3    
    beq c8797                                                         ; 878a: f0 0b       ..    
    bcs c87b2                                                         ; 878c: b0 24       .$    
    jsr skip_spaces                                                   ; 878e: 20 97 8a     ..   
    cmp #&28 ; '('                                                    ; 8791: c9 28       .(    
    beq c879f                                                         ; 8793: f0 0a       ..    
    dec zp_text_ptr_off                                               ; 8795: c6 0a       ..    
; &8797 referenced 1 time by &878a
.c8797
    jsr eval_expr_to_integer                                          ; 8797: 20 21 88     !.   
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
    jsr eval_expr_to_integer                                          ; 87a5: 20 21 88     !.   
    jsr skip_spaces                                                   ; 87a8: 20 97 8a     ..   
    cmp #&29 ; ')'                                                    ; 87ab: c9 29       .)    
    beq c879a                                                         ; 87ad: f0 eb       ..    
    jmp c870d                                                         ; 87af: 4c 0d 87    L..   
; &87b2 referenced 1 time by &878c
.c87b2
    cpx #&39 ; '9'                                                    ; 87b2: e0 39       .9    
    bcs c8813                                                         ; 87b4: b0 5d       .]    
    lda zp_fwb_exp                                                    ; 87b6: a5 3d       .=    
    eor #1                                                            ; 87b8: 49 01       I.    
    and #&1f                                                          ; 87ba: 29 1f       ).    
    pha                                                               ; 87bc: 48          H     
    cpx #&37 ; '7'                                                    ; 87bd: e0 37       .7    
    bcs c87f0                                                         ; 87bf: b0 2f       ./    
    jsr skip_spaces                                                   ; 87c1: 20 97 8a     ..   
    cmp #&23 ; '#'                                                    ; 87c4: c9 23       .#    
    bne c87cc                                                         ; 87c6: d0 04       ..    
    pla                                                               ; 87c8: 68          h     
    jmp c86c5                                                         ; 87c9: 4c c5 86    L..   
; &87cc referenced 1 time by &87c6
.c87cc
    dec zp_text_ptr_off                                               ; 87cc: c6 0a       ..    
    jsr eval_expr_to_integer                                          ; 87ce: 20 21 88     !.   
    pla                                                               ; 87d1: 68          h     
    sta zp_general                                                    ; 87d2: 85 37       .7    
    jsr skip_spaces                                                   ; 87d4: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 87d7: c9 2c       .,    
    beq c87de                                                         ; 87d9: f0 03       ..    
    jmp c8735                                                         ; 87db: 4c 35 87    L5.   
; &87de referenced 1 time by &87d9
.c87de
    jsr skip_spaces                                                   ; 87de: 20 97 8a     ..   
    and #&1f                                                          ; 87e1: 29 1f       ).    
    cmp zp_general                                                    ; 87e3: c5 37       .7    
    bne c87ed                                                         ; 87e5: d0 06       ..    
    jsr sub_c882c                                                     ; 87e7: 20 2c 88     ,.   
    jmp c8735                                                         ; 87ea: 4c 35 87    L5.   
; &87ed referenced 2 times by &87e5, &8804
.c87ed
    jmp c870d                                                         ; 87ed: 4c 0d 87    L..   
; &87f0 referenced 1 time by &87bf
.c87f0
    jsr eval_expr_to_integer                                          ; 87f0: 20 21 88     !.   
    pla                                                               ; 87f3: 68          h     
    sta zp_general                                                    ; 87f4: 85 37       .7    
    jsr skip_spaces                                                   ; 87f6: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 87f9: c9 2c       .,    
    bne c8810                                                         ; 87fb: d0 13       ..    
    jsr skip_spaces                                                   ; 87fd: 20 97 8a     ..   
    and #&1f                                                          ; 8800: 29 1f       ).    
    cmp zp_general                                                    ; 8802: c5 37       .7    
    bne c87ed                                                         ; 8804: d0 e7       ..    
    jsr sub_c882c                                                     ; 8806: 20 2c 88     ,.   
    lda zp_iwa_1                                                      ; 8809: a5 2b       .+    
    beq c8810                                                         ; 880b: f0 03       ..    
    jmp c86cc                                                         ; 880d: 4c cc 86    L..   
; &8810 referenced 2 times by &87fb, &880b
.c8810
    jmp c8738                                                         ; 8810: 4c 38 87    L8.   
; &8813 referenced 1 time by &87b4
.c8813
    bne c883a                                                         ; 8813: d0 25       .%    
    jsr eval_expr_to_integer                                          ; 8815: 20 21 88     !.   
    lda zp_iwa                                                        ; 8818: a5 2a       .*    
    sta zp_opt_flag                                                   ; 881a: 85 28       .(    
    ldy #0                                                            ; 881c: a0 00       ..    
    jmp c862b                                                         ; 881e: 4c 2b 86    L+.   
; ***************************************************************************************
; Evaluate an integer expression
;
; Evaluate the expression at the text pointer (eval_expr) and coerce the result to an
; integer (coerce_to_integer), then copy the secondary text offset back to the primary
; pointer. Used wherever a statement needs an integer argument.
;
; On Exit:
;     ZP_IWA (&2A): 4-byte integer result
; &8821 referenced 22 times by &8677, &86c5, &86de, &8717, &8750, &8782, &8797, &87a5, &87ce, &87f0, &8815, &885a, &9188, &92a2, &937a, &9391, &939d, &93f1, &9440, &b44c, &b472, &b4a0
.eval_expr_to_integer
    jsr eval_expr                                                     ; 8821: 20 1d 9b     ..   
    jsr coerce_to_integer                                             ; 8824: 20 f0 92     ..   
; &8827 referenced 3 times by &85b7, &8875, &9121
.sub_c8827
    ldy zp_text_ptr2_off                                              ; 8827: a4 1b       ..    
    sty zp_text_ptr_off                                               ; 8829: 84 0a       ..    
    rts                                                               ; 882b: 60          `     
; &882c referenced 7 times by &86ef, &8721, &875a, &879f, &87a2, &87e7, &8806
.sub_c882c
    jsr sub_c882f                                                     ; 882c: 20 2f 88     /.   
; &882f referenced 3 times by &86c2, &872f, &882c
.sub_c882f
    jsr sub_c8832                                                     ; 882f: 20 32 88     2.   
; &8832 referenced 3 times by &8735, &8767, &882f
.sub_c8832
    lda zp_asm_opcode                                                 ; 8832: a5 29       .)    
    clc                                                               ; 8834: 18          .     
    adc #4                                                            ; 8835: 69 04       i.    
    sta zp_asm_opcode                                                 ; 8837: 85 29       .)    
    rts                                                               ; 8839: 60          `     
; &883a referenced 1 time by &8813
.c883a
    ldx #1                                                            ; 883a: a2 01       ..    
    ldy zp_text_ptr_off                                               ; 883c: a4 0a       ..    
    inc zp_text_ptr_off                                               ; 883e: e6 0a       ..    
    lda (zp_text_ptr),y                                               ; 8840: b1 0b       ..    
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
    jsr eval_expr_to_integer                                          ; 885a: 20 21 88     !.   
    ldx #&29 ; ')'                                                    ; 885d: a2 29       .)    
    jsr iwa_store_zp                                                  ; 885f: 20 44 be     D.   
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
    lda zp_opt_flag                                                   ; 886a: a5 28       .(    
    pha                                                               ; 886c: 48          H     
    jsr eval_expr                                                     ; 886d: 20 1d 9b     ..   
    bne loop_c8867                                                    ; 8870: d0 f5       ..    
    pla                                                               ; 8872: 68          h     
    sta zp_opt_flag                                                   ; 8873: 85 28       .(    
    jsr sub_c8827                                                     ; 8875: 20 27 88     '.   
    ldy #&ff                                                          ; 8878: a0 ff       ..    
    bne loop_c8864                                                    ; 887a: d0 e8       ..    
; &887c referenced 2 times by &88dd, &8a55
.sub_c887c
    pha                                                               ; 887c: 48          H     
    clc                                                               ; 887d: 18          .     
    tya                                                               ; 887e: 98          .     
    adc zp_general                                                    ; 887f: 65 37       e7    
    sta zp_fileblk                                                    ; 8881: 85 39       .9    
    ldy #0                                                            ; 8883: a0 00       ..    
    tya                                                               ; 8885: 98          .     
    adc l0038                                                         ; 8886: 65 38       e8    
    sta l003a                                                         ; 8888: 85 3a       .:    
    pla                                                               ; 888a: 68          h     
    sta (zp_general),y                                                ; 888b: 91 37       .7    
; &888d referenced 1 time by &8894
.loop_c888d
    iny                                                               ; 888d: c8          .     
    lda (zp_fileblk),y                                                ; 888e: b1 39       .9    
    sta (zp_general),y                                                ; 8890: 91 37       .7    
    cmp #&0d                                                          ; 8892: c9 0d       ..    
    bne loop_c888d                                                    ; 8894: d0 f7       ..    
    rts                                                               ; 8896: 60          `     
; &8897 referenced 1 time by &89b0
.sub_c8897
    and #&0f                                                          ; 8897: 29 0f       ).    
    sta zp_fwb_exp                                                    ; 8899: 85 3d       .=    
    sty zp_fwb_m1                                                     ; 889b: 84 3e       .>    
; &889d referenced 2 times by &88ce, &88d2
.c889d
    iny                                                               ; 889d: c8          .     
    lda (zp_general),y                                                ; 889e: b1 37       .7    
    cmp #&3a ; ':'                                                    ; 88a0: c9 3a       .:    
    bcs c88da                                                         ; 88a2: b0 36       .6    
    cmp #&30 ; '0'                                                    ; 88a4: c9 30       .0    
    bcc c88da                                                         ; 88a6: 90 32       .2    
    and #&0f                                                          ; 88a8: 29 0f       ).    
    pha                                                               ; 88aa: 48          H     
    ldx zp_fwb_m1                                                     ; 88ab: a6 3e       .>    
    lda zp_fwb_exp                                                    ; 88ad: a5 3d       .=    
    asl a                                                             ; 88af: 0a          .     
    rol zp_fwb_m1                                                     ; 88b0: 26 3e       &>    
    bmi c88d5                                                         ; 88b2: 30 21       0!    
    asl a                                                             ; 88b4: 0a          .     
    rol zp_fwb_m1                                                     ; 88b5: 26 3e       &>    
    bmi c88d5                                                         ; 88b7: 30 1c       0.    
    adc zp_fwb_exp                                                    ; 88b9: 65 3d       e=    
    sta zp_fwb_exp                                                    ; 88bb: 85 3d       .=    
    txa                                                               ; 88bd: 8a          .     
    adc zp_fwb_m1                                                     ; 88be: 65 3e       e>    
    asl zp_fwb_exp                                                    ; 88c0: 06 3d       .=    
    rol a                                                             ; 88c2: 2a          *     
    bmi c88d5                                                         ; 88c3: 30 10       0.    
    bcs c88d5                                                         ; 88c5: b0 0e       ..    
    sta zp_fwb_m1                                                     ; 88c7: 85 3e       .>    
    pla                                                               ; 88c9: 68          h     
    adc zp_fwb_exp                                                    ; 88ca: 65 3d       e=    
    sta zp_fwb_exp                                                    ; 88cc: 85 3d       .=    
    bcc c889d                                                         ; 88ce: 90 cd       ..    
    inc zp_fwb_m1                                                     ; 88d0: e6 3e       .>    
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
    lda zp_general                                                    ; 88e0: a5 37       .7    
    adc #2                                                            ; 88e2: 69 02       i.    
    sta zp_fileblk                                                    ; 88e4: 85 39       .9    
    lda l0038                                                         ; 88e6: a5 38       .8    
    adc #0                                                            ; 88e8: 69 00       i.    
    sta l003a                                                         ; 88ea: 85 3a       .:    
; &88ec referenced 1 time by &88f1
.loop_c88ec
    lda (zp_general),y                                                ; 88ec: b1 37       .7    
    sta (zp_fileblk),y                                                ; 88ee: 91 39       .9    
    dey                                                               ; 88f0: 88          .     
    bne loop_c88ec                                                    ; 88f1: d0 f9       ..    
    ldy #3                                                            ; 88f3: a0 03       ..    
; &88f5 referenced 1 time by &906a
.sub_c88f5
    lda zp_fwb_m1                                                     ; 88f5: a5 3e       .>    
    ora #&40 ; '@'                                                    ; 88f7: 09 40       .@    
    sta (zp_general),y                                                ; 88f9: 91 37       .7    
    dey                                                               ; 88fb: 88          .     
    lda zp_fwb_exp                                                    ; 88fc: a5 3d       .=    
    and #&3f ; '?'                                                    ; 88fe: 29 3f       )?    
    ora #&40 ; '@'                                                    ; 8900: 09 40       .@    
    sta (zp_general),y                                                ; 8902: 91 37       .7    
    dey                                                               ; 8904: 88          .     
    lda zp_fwb_exp                                                    ; 8905: a5 3d       .=    
    and #&c0                                                          ; 8907: 29 c0       ).    
    sta zp_fwb_exp                                                    ; 8909: 85 3d       .=    
    lda zp_fwb_m1                                                     ; 890b: a5 3e       .>    
    and #&c0                                                          ; 890d: 29 c0       ).    
    lsr a                                                             ; 890f: 4a          J     
    lsr a                                                             ; 8910: 4a          J     
    ora zp_fwb_exp                                                    ; 8911: 05 3d       .=    
    lsr a                                                             ; 8913: 4a          J     
    lsr a                                                             ; 8914: 4a          J     
    eor #&54 ; 'T'                                                    ; 8915: 49 54       IT    
    sta (zp_general),y                                                ; 8917: 91 37       .7    
    jsr inc_ptr_general                                               ; 8919: 20 44 89     D.   
    jsr inc_ptr_general                                               ; 891c: 20 44 89     D.   
    jsr inc_ptr_general                                               ; 891f: 20 44 89     D.   
    ldy #0                                                            ; 8922: a0 00       ..    
; &8924 referenced 3 times by &8928, &8930, &8938
.c8924
    clc                                                               ; 8924: 18          .     
    rts                                                               ; 8925: 60          `     
; &8926 referenced 5 times by &89cb, &89d4, &8a43, &8a74, &b167
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
; ***************************************************************************************
; Read a byte via the general pointer, then advance it
;
; Load the byte at (zp_general),Y and fall through to inc_ptr_general to step the 16-bit
; pointer on by one.
; &8942 referenced 4 times by &b3d9, &b3e8, &b3f1, &b3f6
.read_via_ptr_general
    lda (zp_general),y                                                ; 8942: b1 37       .7    
; ***************************************************************************************
; Increment the general 16-bit pointer
;
; Increment the little-endian pointer held in zp_general (&37/&38) by one, carrying into
; the high byte.
; &8944 referenced 8 times by &8919, &891c, &891f, &894b, &8961, &89bc, &89d9, &8a79
.inc_ptr_general
    inc zp_general                                                    ; 8944: e6 37       .7    
    bne return_3                                                      ; 8946: d0 02       ..    
    inc l0038                                                         ; 8948: e6 38       .8    
; &894a referenced 2 times by &8946, &895b
.return_3
    rts                                                               ; 894a: 60          `     
; &894b referenced 3 times by &896a, &8980, &bfdc
.sub_c894b
    jsr inc_ptr_general                                               ; 894b: 20 44 89     D.   
    lda (zp_general),y                                                ; 894e: b1 37       .7    
    rts                                                               ; 8950: 60          `     
; ***************************************************************************************
; Tokenise a line
;
; Convert the line being entered into its internal form, replacing keywords with tokens
; via the keyword_table while leaving strings, line numbers and names intact. Works
; through the buffer using the general pointer (zp_general, &37).
; &8951 referenced 1 time by &90c3
.tokenise_line
    ldy #0                                                            ; 8951: a0 00       ..       ; Tokeniser state (&3B/&3C): start of statement
    sty zp_fwb_sign                                                   ; 8953: 84 3b       .;    
; &8955 referenced 1 time by &ac1a
.sub_c8955
    sty zp_fwb_ovf                                                    ; 8955: 84 3c       .<    
; &8957 referenced 5 times by &8964, &8974, &897a, &89c8, &8b2a
.c8957
    lda (zp_general),y                                                ; 8957: b1 37       .7       ; Scan the next source character
    cmp #&0d                                                          ; 8959: c9 0d       ..    
    beq return_3                                                      ; 895b: f0 ed       ..       ; Carriage return ends the line
    cmp #&20 ; ' '                                                    ; 895d: c9 20       .     
    bne c8966                                                         ; 895f: d0 05       ..       ; Skip spaces
; &8961 referenced 5 times by &8985, &8994, &8998, &89e9, &8a89
.c8961
    jsr inc_ptr_general                                               ; 8961: 20 44 89     D.   
    bne c8957                                                         ; 8964: d0 f1       ..    
; &8966 referenced 1 time by &895f
.c8966
    cmp #&26 ; '&'                                                    ; 8966: c9 26       .&       ; An "&" introduces a hex constant: copy it unchanged
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
    cmp #&22                                                          ; 897c: c9 22       ."       ; A quote starts a string literal: copy it verbatim
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
    cmp #&3a ; ':'                                                    ; 898c: c9 3a       .:       ; A colon starts a new statement: reset the state
    bne c8996                                                         ; 898e: d0 06       ..    
    sty zp_fwb_sign                                                   ; 8990: 84 3b       .;    
    sty zp_fwb_ovf                                                    ; 8992: 84 3c       .<    
    beq c8961                                                         ; 8994: f0 cb       ..    
; &8996 referenced 1 time by &898e
.c8996
    cmp #&2c ; ','                                                    ; 8996: c9 2c       .,    
    beq c8961                                                         ; 8998: f0 c7       ..    
    cmp #&2a ; '*'                                                    ; 899a: c9 2a       .*       ; A "*" at statement start: rest is a *command
    bne c89a3                                                         ; 899c: d0 05       ..    
    lda zp_fwb_sign                                                   ; 899e: a5 3b       .;    
    bne c89e3                                                         ; 89a0: d0 41       .A    
    rts                                                               ; 89a2: 60          `     
; &89a3 referenced 1 time by &899c
.c89a3
    cmp #&2e ; '.'                                                    ; 89a3: c9 2e       ..    
    beq c89b5                                                         ; 89a5: f0 0e       ..    
    jsr c8936                                                         ; 89a7: 20 36 89     6.   
    bcc c89df                                                         ; 89aa: 90 33       .3    
    ldx zp_fwb_ovf                                                    ; 89ac: a6 3c       .<    
    beq c89b5                                                         ; 89ae: f0 05       ..    
    jsr sub_c8897                                                     ; 89b0: 20 97 88     ..   
    bcc c89e9                                                         ; 89b3: 90 34       .4    
; &89b5 referenced 3 times by &89a5, &89ae, &89bf
.c89b5
    lda (zp_general),y                                                ; 89b5: b1 37       .7    
    jsr sub_c893d                                                     ; 89b7: 20 3d 89     =.   
    bcc c89c2                                                         ; 89ba: 90 06       ..    
    jsr inc_ptr_general                                               ; 89bc: 20 44 89     D.   
    jmp c89b5                                                         ; 89bf: 4c b5 89    L..   
; &89c2 referenced 2 times by &89ba, &89d7
.c89c2
    ldx #&ff                                                          ; 89c2: a2 ff       ..    
    stx zp_fwb_sign                                                   ; 89c4: 86 3b       .;    
    sty zp_fwb_ovf                                                    ; 89c6: 84 3c       .<    
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
    lda (zp_general),y                                                ; 89d2: b1 37       .7    
    jsr sub_c8926                                                     ; 89d4: 20 26 89     &.   
    bcc c89c2                                                         ; 89d7: 90 e9       ..    
    jsr inc_ptr_general                                               ; 89d9: 20 44 89     D.   
    jmp c89d2                                                         ; 89dc: 4c d2 89    L..   
; &89df referenced 1 time by &89aa
.c89df
    cmp #&41 ; 'A'                                                    ; 89df: c9 41       .A    
    bcs c89ec                                                         ; 89e1: b0 09       ..    
; &89e3 referenced 2 times by &89a0, &89ce
.c89e3
    ldx #&ff                                                          ; 89e3: a2 ff       ..    
    stx zp_fwb_sign                                                   ; 89e5: 86 3b       .;    
    sty zp_fwb_ovf                                                    ; 89e7: 84 3c       .<    
; &89e9 referenced 1 time by &89b3
.c89e9
    jmp c8961                                                         ; 89e9: 4c 61 89    La.   
; &89ec referenced 1 time by &89e1
.c89ec
    cmp #&58 ; 'X'                                                    ; 89ec: c9 58       .X    
    bcs loop_c89cb                                                    ; 89ee: b0 db       ..    
    ldx #&71 ; 'q'                                                    ; 89f0: a2 71       .q    
    stx zp_fileblk                                                    ; 89f2: 86 39       .9    
    ldx #&80                                                          ; 89f4: a2 80       ..    
    stx l003a                                                         ; 89f6: 86 3a       .:    
; &89f8 referenced 1 time by &8a34
.c89f8
    cmp (zp_fileblk),y                                                ; 89f8: d1 39       .9    
    bcc c89d2                                                         ; 89fa: 90 d6       ..    
    bne c8a0d                                                         ; 89fc: d0 0f       ..    
; &89fe referenced 1 time by &8a05
.loop_c89fe
    iny                                                               ; 89fe: c8          .     
    lda (zp_fileblk),y                                                ; 89ff: b1 39       .9    
    bmi c8a37                                                         ; 8a01: 30 34       04    
    cmp (zp_general),y                                                ; 8a03: d1 37       .7    
    beq loop_c89fe                                                    ; 8a05: f0 f7       ..    
    lda (zp_general),y                                                ; 8a07: b1 37       .7    
    cmp #&2e ; '.'                                                    ; 8a09: c9 2e       ..    
    beq c8a18                                                         ; 8a0b: f0 0b       ..    
; &8a0d referenced 2 times by &89fc, &8a10
.c8a0d
    iny                                                               ; 8a0d: c8          .     
    lda (zp_fileblk),y                                                ; 8a0e: b1 39       .9    
    bpl c8a0d                                                         ; 8a10: 10 fb       ..    
    cmp #&fe                                                          ; 8a12: c9 fe       ..    
    bne c8a25                                                         ; 8a14: d0 0f       ..    
    bcs c89d0                                                         ; 8a16: b0 b8       ..    
; &8a18 referenced 1 time by &8a0b
.c8a18
    iny                                                               ; 8a18: c8          .     
; &8a19 referenced 2 times by &8a1f, &8a23
.c8a19
    lda (zp_fileblk),y                                                ; 8a19: b1 39       .9    
    bmi c8a37                                                         ; 8a1b: 30 1a       0.    
    inc zp_fileblk                                                    ; 8a1d: e6 39       .9    
    bne c8a19                                                         ; 8a1f: d0 f8       ..    
    inc l003a                                                         ; 8a21: e6 3a       .:    
    bne c8a19                                                         ; 8a23: d0 f4       ..    
; &8a25 referenced 1 time by &8a14
.c8a25
    sec                                                               ; 8a25: 38          8     
    iny                                                               ; 8a26: c8          .     
    tya                                                               ; 8a27: 98          .     
    adc zp_fileblk                                                    ; 8a28: 65 39       e9    
    sta zp_fileblk                                                    ; 8a2a: 85 39       .9    
    bcc c8a30                                                         ; 8a2c: 90 02       ..    
    inc l003a                                                         ; 8a2e: e6 3a       .:    
; &8a30 referenced 1 time by &8a2c
.c8a30
    ldy #0                                                            ; 8a30: a0 00       ..    
    lda (zp_general),y                                                ; 8a32: b1 37       .7    
    jmp c89f8                                                         ; 8a34: 4c f8 89    L..   
; &8a37 referenced 2 times by &8a01, &8a1b
.c8a37
    tax                                                               ; 8a37: aa          .     
    iny                                                               ; 8a38: c8          .     
    lda (zp_fileblk),y                                                ; 8a39: b1 39       .9    
    sta zp_fwb_exp                                                    ; 8a3b: 85 3d       .=    
    dey                                                               ; 8a3d: 88          .     
    lsr a                                                             ; 8a3e: 4a          J     
    bcc c8a48                                                         ; 8a3f: 90 07       ..    
    lda (zp_general),y                                                ; 8a41: b1 37       .7    
    jsr sub_c8926                                                     ; 8a43: 20 26 89     &.   
    bcs c89d0                                                         ; 8a46: b0 88       ..    
; &8a48 referenced 1 time by &8a3f
.c8a48
    txa                                                               ; 8a48: 8a          .     
    bit zp_fwb_exp                                                    ; 8a49: 24 3d       $=    
    bvc c8a54                                                         ; 8a4b: 50 07       P.    
    ldx zp_fwb_sign                                                   ; 8a4d: a6 3b       .;    
    bne c8a54                                                         ; 8a4f: d0 03       ..    
    clc                                                               ; 8a51: 18          .     
    adc #&40 ; '@'                                                    ; 8a52: 69 40       i@    
; &8a54 referenced 2 times by &8a4b, &8a4f
.c8a54
    dey                                                               ; 8a54: 88          .     
    jsr sub_c887c                                                     ; 8a55: 20 7c 88     |.   
    ldy #0                                                            ; 8a58: a0 00       ..    
    ldx #&ff                                                          ; 8a5a: a2 ff       ..    
    lda zp_fwb_exp                                                    ; 8a5c: a5 3d       .=    
    lsr a                                                             ; 8a5e: 4a          J     
    lsr a                                                             ; 8a5f: 4a          J     
    bcc c8a66                                                         ; 8a60: 90 04       ..    
    stx zp_fwb_sign                                                   ; 8a62: 86 3b       .;    
    sty zp_fwb_ovf                                                    ; 8a64: 84 3c       .<    
; &8a66 referenced 1 time by &8a60
.c8a66
    lsr a                                                             ; 8a66: 4a          J     
    bcc c8a6d                                                         ; 8a67: 90 04       ..    
    sty zp_fwb_sign                                                   ; 8a69: 84 3b       .;    
    sty zp_fwb_ovf                                                    ; 8a6b: 84 3c       .<    
; &8a6d referenced 1 time by &8a67
.c8a6d
    lsr a                                                             ; 8a6d: 4a          J     
    bcc c8a81                                                         ; 8a6e: 90 11       ..    
    pha                                                               ; 8a70: 48          H     
    iny                                                               ; 8a71: c8          .     
; &8a72 referenced 1 time by &8a7c
.c8a72
    lda (zp_general),y                                                ; 8a72: b1 37       .7    
    jsr sub_c8926                                                     ; 8a74: 20 26 89     &.   
    bcc c8a7f                                                         ; 8a77: 90 06       ..    
    jsr inc_ptr_general                                               ; 8a79: 20 44 89     D.   
    jmp c8a72                                                         ; 8a7c: 4c 72 8a    Lr.   
; &8a7f referenced 1 time by &8a77
.c8a7f
    dey                                                               ; 8a7f: 88          .     
    pla                                                               ; 8a80: 68          h     
; &8a81 referenced 1 time by &8a6e
.c8a81
    lsr a                                                             ; 8a81: 4a          J     
    bcc c8a86                                                         ; 8a82: 90 02       ..    
    stx zp_fwb_ovf                                                    ; 8a84: 86 3c       .<    
; &8a86 referenced 1 time by &8a82
.c8a86
    lsr a                                                             ; 8a86: 4a          J     
    bcs return_4                                                      ; 8a87: b0 0d       ..    
    jmp c8961                                                         ; 8a89: 4c 61 89    La.   
; ***************************************************************************************
; Skip spaces at the secondary text pointer
;
; As skip_spaces, but works on the secondary text pointer (zp_text_ptr2, &19) and its
; offset (&1B). Used while the primary pointer is preserved, e.g. when scanning ahead
; during assignment.
;
; On Exit:
;     A: first non-space character
;     Y: its offset
;     &1B: advanced past that character
; &8a8c referenced 21 times by &8a94, &8aae, &8d32, &8e43, &8ee3, &9841, &ac50, &ac5b, &ac66, &adad, &ae02, &b094, &b287, &b2a0, &b7ea, &b813, &b866, &babd, &bb60, &bb6f, &bfb5
.skip_spaces_ptr2
    ldy zp_text_ptr2_off                                              ; 8a8c: a4 1b       ..    
    inc zp_text_ptr2_off                                              ; 8a8e: e6 1b       ..    
    lda (zp_text_ptr2),y                                              ; 8a90: b1 19       ..    
    cmp #&20 ; ' '                                                    ; 8a92: c9 20       .        ; Loop while the character is a space
    beq skip_spaces_ptr2                                              ; 8a94: f0 f6       ..    
; &8a96 referenced 1 time by &8a87
.return_4
    rts                                                               ; 8a96: 60          `     
; ***************************************************************************************
; Skip spaces at the text pointer
;
; Advance the primary text pointer past any spaces and return the first non-space
; character. The workhorse of the tokeniser and interpreter: most statements call it
; between syntax elements.
;
; On Entry:
;     ZP_TEXT_PTR (&0B): points at the line being interpreted
;     ZP_TEXT_PTR_OFF (&0A): offset of the next character
;
; On Exit:
;     A: first non-space character
;     Y: its offset within the line
;     ZP_TEXT_PTR_OFF (&0A): advanced past that character
; &8a97 referenced 48 times by &8508, &85bc, &86bb, &86d7, &86e1, &86e8, &86f2, &86ff, &8706, &871a, &8724, &8747, &8753, &875d, &8776, &878e, &87a8, &87c1, &87d4, &87de, &87f6, &87fd, &8a9f, &8b38, &8d89, &8d9a, &8dc3, &8e8a, &8f39, &8f79, &912f, &91a9, &920b, &9349, &942f, &9446, &b13f, &b1f9, &b279, &b5be, &b5cf, &b75c, &b8f2, &b915, &b9da, &ba44, &baee, &bb15
.skip_spaces
    ldy zp_text_ptr_off                                               ; 8a97: a4 0a       ..    
    inc zp_text_ptr_off                                               ; 8a99: e6 0a       ..    
    lda (zp_text_ptr),y                                               ; 8a9b: b1 0b       ..    
    cmp #&20 ; ' '                                                    ; 8a9d: c9 20       .        ; Loop while the character is a space
    beq skip_spaces                                                   ; 8a9f: f0 f6       ..    
    rts                                                               ; 8aa1: 60          `     
; &8aa2 referenced 4 times by &8ab3, &8e21, &ad03, &b036
.c8aa2
    brk                                                               ; 8aa2: 00          .     
    equb &05                                                          ; 8aa3: 05          .     
    equs "Missing ,"                                                  ; 8aa4: 4d 69 73... Mis...
    equb &00                                                          ; 8aad: 00          .     
; ***************************************************************************************
; Skip spaces and require a comma
;
; Call skip_spaces, then check the character is a comma. Raises "Missing ," if it is not.
; Used by statements that take a comma-separated argument list.
; &8aae referenced 5 times by &92da, &93f7, &ab47, &b0c8, &bf5c
.skip_spaces_expect_comma
    jsr skip_spaces_ptr2                                              ; 8aae: 20 8c 8a     ..   
    cmp #&2c ; ','                                                    ; 8ab1: c9 2c       .,    
    bne c8aa2                                                         ; 8ab3: d0 ed       ..    
    rts                                                               ; 8ab5: 60          `     
; ***************************************************************************************
; OLD
;
; Recover the program cleared by NEW, if memory is intact. OLD.
.stmt_old
    jsr check_end_of_statement                                        ; 8ab6: 20 57 98     W.   
    lda zp_page                                                       ; 8ab9: a5 18       ..    
    sta l0038                                                         ; 8abb: 85 38       .8    
    lda #0                                                            ; 8abd: a9 00       ..    
    sta zp_general                                                    ; 8abf: 85 37       .7    
    sta (zp_general),y                                                ; 8ac1: 91 37       .7    
    jsr sub_cbe6f                                                     ; 8ac3: 20 6f be     o.   
    bne c8af3                                                         ; 8ac6: d0 2b       .+    
; ***************************************************************************************
; END
;
; End the program and return to the immediate prompt. END.
.stmt_end
    jsr check_end_of_statement                                        ; 8ac8: 20 57 98     W.   
    jsr sub_cbe6f                                                     ; 8acb: 20 6f be     o.   
    bne immediate_loop                                                ; 8ace: d0 26       .&    
; ***************************************************************************************
; STOP
;
; Stop the program, reporting "STOP at line nnnn". STOP.
.stmt_stop
    jsr check_end_of_statement                                        ; 8ad0: 20 57 98     W.   
    brk                                                               ; 8ad3: 00          .     
    equb &00                                                          ; 8ad4: 00          .     
    equs "STOP"                                                       ; 8ad5: 53 54 4f... STO...
    equb &00                                                          ; 8ad9: 00          .     
; ***************************************************************************************
; NEW
;
; Clear the current program and its variables. NEW.
.stmt_new
    jsr check_end_of_statement                                        ; 8ada: 20 57 98     W.   
; ***************************************************************************************
; Clear program and enter the immediate loop
;
; Entered from language_startup. Sets up an empty program (as the NEW command does) and
; falls through into the immediate loop.
; &8add referenced 1 time by &806e
.start_new_program
    lda #&0d                                                          ; 8add: a9 0d       ..    
    ldy zp_page                                                       ; 8adf: a4 18       ..    
    sty l0013                                                         ; 8ae1: 84 13       ..    
    ldy #0                                                            ; 8ae3: a0 00       ..    
    sty zp_top                                                        ; 8ae5: 84 12       ..    
    sty zp_trace_flag                                                 ; 8ae7: 84 20       .     
    sta (zp_top),y                                                    ; 8ae9: 91 12       ..    
    lda #&ff                                                          ; 8aeb: a9 ff       ..    
    iny                                                               ; 8aed: c8          .     
    sta (zp_top),y                                                    ; 8aee: 91 12       ..    
    iny                                                               ; 8af0: c8          .     
    sty zp_top                                                        ; 8af1: 84 12       ..    
; &8af3 referenced 6 times by &8ac6, &8b35, &8f66, &903a, &90d9, &bf27
.c8af3
    jsr sub_cbd20                                                     ; 8af3: 20 20 bd      .   
; ***************************************************************************************
; Immediate ("> ") loop
;
; Print the prompt, read a line into the input buffer, and tokenise it. A line that
; begins with a line number is inserted into the program; otherwise it is executed
; immediately.
; &8af6 referenced 6 times by &859c, &8ace, &8b41, &98bc, &b599, &b61a
.immediate_loop
    ldy #7                                                            ; 8af6: a0 07       ..    
    sty l000c                                                         ; 8af8: 84 0c       ..    
    ldy #0                                                            ; 8afa: a0 00       ..    
    sty zp_text_ptr                                                   ; 8afc: 84 0b       ..    
    lda #&33 ; '3'                                                    ; 8afe: a9 33       .3    
    sta zp_error_vec                                                  ; 8b00: 85 16       ..    
    lda #&b4                                                          ; 8b02: a9 b4       ..    
    sta l0017                                                         ; 8b04: 85 17       ..    
    lda #&3e ; '>'                                                    ; 8b06: a9 3e       .>    
    jsr sub_cbc02                                                     ; 8b08: 20 02 bc     ..   
; ***************************************************************************************
; Execute the line at the program pointer
;
; Run the tokenised statements on the line addressed by the program pointer (zp_text_ptr,
; &0B), starting at offset zp_text_ptr_off.
; &8b0b referenced 1 time by &bd1d
.execute_line
    lda #&33 ; '3'                                                    ; 8b0b: a9 33       .3       ; Restore the default error handler (ON ERROR OFF)
    sta zp_error_vec                                                  ; 8b0d: 85 16       ..    
    lda #&b4                                                          ; 8b0f: a9 b4       ..    
    sta l0017                                                         ; 8b11: 85 17       ..    
    ldx #&ff                                                          ; 8b13: a2 ff       ..       ; OPT = &FF: not inside the [ ] assembler
    stx zp_opt_flag                                                   ; 8b15: 86 28       .(    
    stx zp_fwb_ovf                                                    ; 8b17: 86 3c       .<    
    txs                                                               ; 8b19: 9a          .        ; Reset the 6502 hardware stack
    jsr sub_cbd3a                                                     ; 8b1a: 20 3a bd     :.      ; Clear the DATA pointer and the BASIC stacks
    tay                                                               ; 8b1d: a8          .     
    lda zp_text_ptr                                                   ; 8b1e: a5 0b       ..       ; Point the general pointer at the line text
    sta zp_general                                                    ; 8b20: 85 37       .7    
    lda l000c                                                         ; 8b22: a5 0c       ..    
    sta l0038                                                         ; 8b24: 85 38       .8    
    sty zp_fwb_sign                                                   ; 8b26: 84 3b       .;    
    sty zp_text_ptr_off                                               ; 8b28: 84 0a       ..    
    jsr c8957                                                         ; 8b2a: 20 57 89     W.   
    jsr sub_c97df                                                     ; 8b2d: 20 df 97     ..      ; Tokenise; carry set if the line starts with a number
    bcc c8b38                                                         ; 8b30: 90 06       ..    
    jsr sub_cbc8d                                                     ; 8b32: 20 8d bc     ..      ; Numbered line: insert it into the program
    jmp c8af3                                                         ; 8b35: 4c f3 8a    L..   
; &8b38 referenced 1 time by &8b30
.c8b38
    jsr skip_spaces                                                   ; 8b38: 20 97 8a     ..   
    cmp #&c6                                                          ; 8b3b: c9 c6       ..       ; Token >= &C6 is a command: dispatch it
    bcs dispatch_token                                                ; 8b3d: b0 72       .r    
    bcc try_variable_assignment                                       ; 8b3f: 90 7e       .~       ; Otherwise treat it as a variable assignment
; &8b41 referenced 1 time by &8b8f
.loop_c8b41
    jmp immediate_loop                                                ; 8b41: 4c f6 8a    L..   
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
    jsr eval_expr                                                     ; 8b53: 20 1d 9b     ..   
    jmp c984c                                                         ; 8b56: 4c 4c 98    LL.   
; &8b59 referenced 2 times by &8b4a, &8b51
.c8b59
    brk                                                               ; 8b59: 00          .     
    equb &07                                                          ; 8b5a: 07          .     
    equs "No "                                                        ; 8b5b: 4e 6f 20    No    
    equb &a4, &00                                                     ; 8b5e: a4 00       ..    
; ***************************************************************************************
; Check for =, * and [ statements
;
; Recognise the statement forms that are not introduced by a token: "=" (return a value
; from FN), "*" (pass the rest of the line to OSCLI), and "[" (enter the inline
; assembler).
; &8b60 referenced 1 time by &8bce
.check_eq_star_bracket
    ldy zp_text_ptr_off                                               ; 8b60: a4 0a       ..    
    dey                                                               ; 8b62: 88          .     
    lda (zp_text_ptr),y                                               ; 8b63: b1 0b       ..    
    cmp #&3d ; '='                                                    ; 8b65: c9 3d       .=       ; "=" returns a value from a function (FN)
    beq loop_c8b47                                                    ; 8b67: f0 de       ..    
    cmp #&2a ; '*'                                                    ; 8b69: c9 2a       .*       ; "*" passes the rest of the line to OSCLI
    beq exec_star_command                                             ; 8b6b: f0 06       ..    
    cmp #&5b ; '['                                                    ; 8b6d: c9 5b       .[       ; "[" enters the inline assembler
    beq loop_c8b44                                                    ; 8b6f: f0 d3       ..    
    bne c8b96                                                         ; 8b71: d0 23       .#    
; &8b73 referenced 1 time by &8b6b
.exec_star_command
    jsr c986d                                                         ; 8b73: 20 6d 98     m.   
    ldx zp_text_ptr                                                   ; 8b76: a6 0b       ..    
    ldy l000c                                                         ; 8b78: a4 0c       ..    
    jsr oscli                                                         ; 8b7a: 20 f7 ff     ..   
; ***************************************************************************************
; DATA / DEF / REM / ELSE
;
; Skip to the end of the line. DATA introduces inline data (read by READ), DEF a PROC/FN
; definition, REM a comment, and ELSE the alternative of a taken IF: none execute inline,
; so all four share this skip-to-end handler.
; &8b7d referenced 2 times by &8b89, &b907
.stmt_data
    lda #&0d                                                          ; 8b7d: a9 0d       ..    
    ldy zp_text_ptr_off                                               ; 8b7f: a4 0a       ..    
    dey                                                               ; 8b81: 88          .     
; &8b82 referenced 1 time by &8b85
.loop_c8b82
    iny                                                               ; 8b82: c8          .     
    cmp (zp_text_ptr),y                                               ; 8b83: d1 0b       ..    
    bne loop_c8b82                                                    ; 8b85: d0 fb       ..    
; &8b87 referenced 2 times by &8ba1, &9902
.c8b87
    cmp #&8b                                                          ; 8b87: c9 8b       ..    
    beq stmt_data                                                     ; 8b89: f0 f2       ..    
    lda l000c                                                         ; 8b8b: a5 0c       ..    
    cmp #7                                                            ; 8b8d: c9 07       ..    
    beq loop_c8b41                                                    ; 8b8f: f0 b0       ..    
    jsr sub_c9890                                                     ; 8b91: 20 90 98     ..   
    bne c8ba3                                                         ; 8b94: d0 0d       ..    
; &8b96 referenced 7 times by &8b71, &8d80, &9212, &9350, &9453, &b7a1, &bb1c
.c8b96
    dec zp_text_ptr_off                                               ; 8b96: c6 0a       ..    
; &8b98 referenced 4 times by &8d7a, &9353, &b9cc, &ba41
.c8b98
    jsr check_end_of_statement                                        ; 8b98: 20 57 98     W.   
; ***************************************************************************************
; Statement execution loop
;
; The main interpreter loop: fetch the next statement's leading token and dispatch it,
; then advance to the next statement (after a colon) or line. Returns here after each
; statement completes.
; &8b9b referenced 23 times by &8bf8, &8c08, &8ecf, &8f18, &926c, &928a, &92b4, &92d7, &9318, &93e1, &9427, &b49d, &b4ab, &b8c9, &b8ef, &bb12, &bbca, &becc, &bf21, &bf43, &bf6c, &bfa6, &bff6
.statement_loop
    ldy #0                                                            ; 8b9b: a0 00       ..       ; Fetch the next character of the statement
    lda (zp_text_ptr),y                                               ; 8b9d: b1 0b       ..    
    cmp #&3a ; ':'                                                    ; 8b9f: c9 3a       .:       ; A colon separates statements on a line
    bne c8b87                                                         ; 8ba1: d0 e4       ..    
; &8ba3 referenced 10 times by &8501, &8b94, &8bab, &98de, &b20b, &b430, &b74e, &b84c, &b8e1, &bbf9
.c8ba3
    ldy zp_text_ptr_off                                               ; 8ba3: a4 0a       ..       ; Skip spaces to the next statement
    inc zp_text_ptr_off                                               ; 8ba5: e6 0a       ..    
    lda (zp_text_ptr),y                                               ; 8ba7: b1 0b       ..    
    cmp #&20 ; ' '                                                    ; 8ba9: c9 20       .     
    beq c8ba3                                                         ; 8bab: f0 f6       ..    
    cmp #&cf                                                          ; 8bad: c9 cf       ..       ; Below &CF: a variable assignment, not a command
    bcc try_variable_assignment                                       ; 8baf: 90 0e       ..    
; ***************************************************************************************
; Dispatch a tokenised function or command
;
; Index the action-address table by (token - &8E): load the handler address into
; zp_general (&37/&38) and JMP (&0037). This is the indirect jump that reaches every fn_*
; / stmt_* handler.
;
; On Entry:
;     A: a command/function token (&8E-&FF)
; &8bb1 referenced 2 times by &8b3d, &ae0d
.dispatch_token
    tax                                                               ; 8bb1: aa          .     
    lda l82df,x                                                       ; 8bb2: bd df 82    ...      ; Handler low byte = action_table_lo[token - &8E]
    sta zp_general                                                    ; 8bb5: 85 37       .7    
    lda l8351,x                                                       ; 8bb7: bd 51 83    .Q.      ; Handler high byte from action_table_hi
    sta l0038                                                         ; 8bba: 85 38       .8    
    jmp (zp_general)                                                  ; 8bbc: 6c 37 00    l7.      ; Jump to the keyword handler
; ***************************************************************************************
; Not a command token: try an assignment
;
; Reached when the statement does not begin with a command token: treat it as an
; implied-LET variable assignment, or one of the =, * (OSCLI) or [ (assembler) special
; statement forms.
; &8bbf referenced 2 times by &8b3f, &8baf
.try_variable_assignment
    ldx zp_text_ptr                                                   ; 8bbf: a6 0b       ..    
    stx zp_text_ptr2                                                  ; 8bc1: 86 19       ..    
    ldx l000c                                                         ; 8bc3: a6 0c       ..    
    stx l001a                                                         ; 8bc5: 86 1a       ..    
    sty zp_text_ptr2_off                                              ; 8bc7: 84 1b       ..    
    jsr sub_c95dd                                                     ; 8bc9: 20 dd 95     ..   
    bne c8be9                                                         ; 8bcc: d0 1b       ..    
    bcs check_eq_star_bracket                                         ; 8bce: b0 90       ..    
    stx zp_text_ptr2_off                                              ; 8bd0: 86 1b       ..    
    jsr sub_c9841                                                     ; 8bd2: 20 41 98     A.   
    jsr sub_c94fc                                                     ; 8bd5: 20 fc 94     ..   
    ldx #5                                                            ; 8bd8: a2 05       ..    
    cpx zp_iwa_2                                                      ; 8bda: e4 2c       .,    
    bne c8bdf                                                         ; 8bdc: d0 01       ..    
    inx                                                               ; 8bde: e8          .     
; &8bdf referenced 1 time by &8bdc
.c8bdf
    jsr sub_c9531                                                     ; 8bdf: 20 31 95     1.   
    dec zp_text_ptr_off                                               ; 8be2: c6 0a       ..    
; ***************************************************************************************
; LET
;
; Assign an expression to a variable; the LET keyword is optional. [LET] var = expr.
.stmt_let
    jsr sub_c9582                                                     ; 8be4: 20 82 95     ..   
    beq c8c0b                                                         ; 8be7: f0 22       ."    
; &8be9 referenced 1 time by &8bcc
.c8be9
    bcc c8bfb                                                         ; 8be9: 90 10       ..    
    jsr stack_integer                                                 ; 8beb: 20 94 bd     ..   
    jsr c9813                                                         ; 8bee: 20 13 98     ..   
    lda zp_var_type                                                   ; 8bf1: a5 27       .'    
    bne c8c0e                                                         ; 8bf3: d0 19       ..    
    jsr sub_c8c1e                                                     ; 8bf5: 20 1e 8c     ..   
    jmp statement_loop                                                ; 8bf8: 4c 9b 8b    L..   
; &8bfb referenced 1 time by &8be9
.c8bfb
    jsr stack_integer                                                 ; 8bfb: 20 94 bd     ..   
    jsr c9813                                                         ; 8bfe: 20 13 98     ..   
    lda zp_var_type                                                   ; 8c01: a5 27       .'    
    beq c8c0e                                                         ; 8c03: f0 09       ..    
    jsr sub_cb4b4                                                     ; 8c05: 20 b4 b4     ..   
    jmp statement_loop                                                ; 8c08: 4c 9b 8b    L..   
; &8c0b referenced 1 time by &8be7
.c8c0b
    jmp c982a                                                         ; 8c0b: 4c 2a 98    L*.   
; &8c0e referenced 18 times by &8867, &8bf3, &8c03, &92f7, &98bf, &9a9a, &9c88, &9d39, &abe6, &ac9b, &ad67, &aece, &b033, &b0bf, &b4ae, &b9c4, &becf, &bf96
.c8c0e
    brk                                                               ; 8c0e: 00          .     
    equb &06                                                          ; 8c0f: 06          .     
    equs "Type mismatch"                                              ; 8c10: 54 79 70... Typ...
    equb &00                                                          ; 8c1d: 00          .     
; &8c1e referenced 3 times by &8bf5, &ba13, &bb3d
.sub_c8c1e
    jsr unstack_integer                                               ; 8c1e: 20 ea bd     ..   
; &8c21 referenced 2 times by &b300, &bae0
.sub_c8c21
    lda zp_iwa_2                                                      ; 8c21: a5 2c       .,    
    cmp #&80                                                          ; 8c23: c9 80       ..    
    beq c8ca2                                                         ; 8c25: f0 7b       .{    
    ldy #2                                                            ; 8c27: a0 02       ..    
    lda (zp_iwa),y                                                    ; 8c29: b1 2a       .*    
    cmp zp_strbuf_len                                                 ; 8c2b: c5 36       .6    
    bcs c8c84                                                         ; 8c2d: b0 55       .U    
    lda zp_vartop                                                     ; 8c2f: a5 02       ..    
    sta zp_iwa_2                                                      ; 8c31: 85 2c       .,    
    lda zp_vartop_1                                                   ; 8c33: a5 03       ..    
    sta zp_iwa_3                                                      ; 8c35: 85 2d       .-    
    lda zp_strbuf_len                                                 ; 8c37: a5 36       .6    
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
    lda (zp_iwa),y                                                    ; 8c46: b1 2a       .*    
    ldy #0                                                            ; 8c48: a0 00       ..    
    adc (zp_iwa),y                                                    ; 8c4a: 71 2a       q*    
    eor zp_vartop                                                     ; 8c4c: 45 02       E.    
    bne c8c5f                                                         ; 8c4e: d0 0f       ..    
    iny                                                               ; 8c50: c8          .     
    adc (zp_iwa),y                                                    ; 8c51: 71 2a       q*    
    eor zp_vartop_1                                                   ; 8c53: 45 03       E.    
    bne c8c5f                                                         ; 8c55: d0 08       ..    
    sta zp_iwa_3                                                      ; 8c57: 85 2d       .-    
    txa                                                               ; 8c59: 8a          .     
    iny                                                               ; 8c5a: c8          .     
    sec                                                               ; 8c5b: 38          8     
    sbc (zp_iwa),y                                                    ; 8c5c: f1 2a       .*    
    tax                                                               ; 8c5e: aa          .     
; &8c5f referenced 2 times by &8c4e, &8c55
.c8c5f
    txa                                                               ; 8c5f: 8a          .     
    clc                                                               ; 8c60: 18          .     
    adc zp_vartop                                                     ; 8c61: 65 02       e.    
    tay                                                               ; 8c63: a8          .     
    lda zp_vartop_1                                                   ; 8c64: a5 03       ..    
    adc #0                                                            ; 8c66: 69 00       i.    
    cpy zp_stack_ptr                                                  ; 8c68: c4 04       ..    
    tax                                                               ; 8c6a: aa          .     
    sbc zp_stack_ptr_1                                                ; 8c6b: e5 05       ..    
    bcs err_no_room                                                   ; 8c6d: b0 48       .H    
    sty zp_vartop                                                     ; 8c6f: 84 02       ..    
    stx zp_vartop_1                                                   ; 8c71: 86 03       ..    
    pla                                                               ; 8c73: 68          h     
    ldy #2                                                            ; 8c74: a0 02       ..    
    sta (zp_iwa),y                                                    ; 8c76: 91 2a       .*    
    dey                                                               ; 8c78: 88          .     
    lda zp_iwa_3                                                      ; 8c79: a5 2d       .-    
    beq c8c84                                                         ; 8c7b: f0 07       ..    
    sta (zp_iwa),y                                                    ; 8c7d: 91 2a       .*    
    dey                                                               ; 8c7f: 88          .     
    lda zp_iwa_2                                                      ; 8c80: a5 2c       .,    
    sta (zp_iwa),y                                                    ; 8c82: 91 2a       .*    
; &8c84 referenced 2 times by &8c2d, &8c7b
.c8c84
    ldy #3                                                            ; 8c84: a0 03       ..    
    lda zp_strbuf_len                                                 ; 8c86: a5 36       .6    
    sta (zp_iwa),y                                                    ; 8c88: 91 2a       .*    
    beq return_5                                                      ; 8c8a: f0 15       ..    
    dey                                                               ; 8c8c: 88          .     
    dey                                                               ; 8c8d: 88          .     
    lda (zp_iwa),y                                                    ; 8c8e: b1 2a       .*    
    sta zp_iwa_3                                                      ; 8c90: 85 2d       .-    
    dey                                                               ; 8c92: 88          .     
    lda (zp_iwa),y                                                    ; 8c93: b1 2a       .*    
    sta zp_iwa_2                                                      ; 8c95: 85 2c       .,    
; &8c97 referenced 1 time by &8c9f
.loop_c8c97
    lda string_work,y                                                 ; 8c97: b9 00 06    ...   
    sta (zp_iwa_2),y                                                  ; 8c9a: 91 2c       .,    
    iny                                                               ; 8c9c: c8          .     
    cpy zp_strbuf_len                                                 ; 8c9d: c4 36       .6    
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
    lda string_work,y                                                 ; 8ca9: b9 00 06    ...   
    sta (zp_iwa),y                                                    ; 8cac: 91 2a       .*    
    dey                                                               ; 8cae: 88          .     
    bne loop_c8ca9                                                    ; 8caf: d0 f8       ..    
    lda string_work                                                   ; 8cb1: ad 00 06    ...   
; &8cb4 referenced 1 time by &8ca7
.c8cb4
    sta (zp_iwa),y                                                    ; 8cb4: 91 2a       .*    
    rts                                                               ; 8cb6: 60          `     
; &8cb7 referenced 3 times by &8c6d, &9553, &be41
.err_no_room
    brk                                                               ; 8cb7: 00          .     
    equb &00                                                          ; 8cb8: 00          .     
    equs "No room"                                                    ; 8cb9: 4e 6f 20... No ...
    equb &00                                                          ; 8cc0: 00          .     
; &8cc1 referenced 1 time by &b21f
.sub_c8cc1
    lda zp_fileblk                                                    ; 8cc1: a5 39       .9    
    cmp #&80                                                          ; 8cc3: c9 80       ..    
    beq c8cee                                                         ; 8cc5: f0 27       .'    
    bcc c8d03                                                         ; 8cc7: 90 3a       .:    
    ldy #0                                                            ; 8cc9: a0 00       ..    
    lda (zp_stack_ptr),y                                              ; 8ccb: b1 04       ..    
    tax                                                               ; 8ccd: aa          .     
    beq c8ce5                                                         ; 8cce: f0 15       ..    
    lda (zp_general),y                                                ; 8cd0: b1 37       .7    
    sbc #1                                                            ; 8cd2: e9 01       ..    
    sta zp_fileblk                                                    ; 8cd4: 85 39       .9    
    iny                                                               ; 8cd6: c8          .     
    lda (zp_general),y                                                ; 8cd7: b1 37       .7    
    sbc #0                                                            ; 8cd9: e9 00       ..    
    sta l003a                                                         ; 8cdb: 85 3a       .:    
; &8cdd referenced 1 time by &8ce3
.loop_c8cdd
    lda (zp_stack_ptr),y                                              ; 8cdd: b1 04       ..    
    sta (zp_fileblk),y                                                ; 8cdf: 91 39       .9    
    iny                                                               ; 8ce1: c8          .     
    dex                                                               ; 8ce2: ca          .     
    bne loop_c8cdd                                                    ; 8ce3: d0 f8       ..    
; &8ce5 referenced 1 time by &8cce
.c8ce5
    lda (zp_stack_ptr,x)                                              ; 8ce5: a1 04       ..    
    ldy #3                                                            ; 8ce7: a0 03       ..    
; &8ce9 referenced 1 time by &8d01
.loop_c8ce9
    sta (zp_general),y                                                ; 8ce9: 91 37       .7    
    jmp cbddc                                                         ; 8ceb: 4c dc bd    L..   
; &8cee referenced 1 time by &8cc5
.c8cee
    ldy #0                                                            ; 8cee: a0 00       ..    
    lda (zp_stack_ptr),y                                              ; 8cf0: b1 04       ..    
    tax                                                               ; 8cf2: aa          .     
    beq c8cff                                                         ; 8cf3: f0 0a       ..    
; &8cf5 referenced 1 time by &8cfd
.loop_c8cf5
    iny                                                               ; 8cf5: c8          .     
    lda (zp_stack_ptr),y                                              ; 8cf6: b1 04       ..    
    dey                                                               ; 8cf8: 88          .     
    sta (zp_general),y                                                ; 8cf9: 91 37       .7    
    iny                                                               ; 8cfb: c8          .     
    dex                                                               ; 8cfc: ca          .     
    bne loop_c8cf5                                                    ; 8cfd: d0 f6       ..    
; &8cff referenced 1 time by &8cf3
.c8cff
    lda #&0d                                                          ; 8cff: a9 0d       ..    
    bne loop_c8ce9                                                    ; 8d01: d0 e6       ..    
; &8d03 referenced 1 time by &8cc7
.c8d03
    ldy #0                                                            ; 8d03: a0 00       ..    
    lda (zp_stack_ptr),y                                              ; 8d05: b1 04       ..    
    sta (zp_general),y                                                ; 8d07: 91 37       .7    
    iny                                                               ; 8d09: c8          .     
    cpy zp_fileblk                                                    ; 8d0a: c4 39       .9    
    bcs c8d26                                                         ; 8d0c: b0 18       ..    
    lda (zp_stack_ptr),y                                              ; 8d0e: b1 04       ..    
    sta (zp_general),y                                                ; 8d10: 91 37       .7    
    iny                                                               ; 8d12: c8          .     
    lda (zp_stack_ptr),y                                              ; 8d13: b1 04       ..    
    sta (zp_general),y                                                ; 8d15: 91 37       .7    
    iny                                                               ; 8d17: c8          .     
    lda (zp_stack_ptr),y                                              ; 8d18: b1 04       ..    
    sta (zp_general),y                                                ; 8d1a: 91 37       .7    
    iny                                                               ; 8d1c: c8          .     
    cpy zp_fileblk                                                    ; 8d1d: c4 39       .9    
    bcs c8d26                                                         ; 8d1f: b0 05       ..    
    lda (zp_stack_ptr),y                                              ; 8d21: b1 04       ..    
    sta (zp_general),y                                                ; 8d23: 91 37       .7    
    iny                                                               ; 8d25: c8          .     
; &8d26 referenced 2 times by &8d0c, &8d1f
.c8d26
    tya                                                               ; 8d26: 98          .     
    clc                                                               ; 8d27: 18          .     
    jmp cbde1                                                         ; 8d28: 4c e1 bd    L..   
; &8d2b referenced 1 time by &8d9f
.loop_c8d2b
    dec zp_text_ptr_off                                               ; 8d2b: c6 0a       ..    
    jsr sub_cbfa9                                                     ; 8d2d: 20 a9 bf     ..   
; &8d30 referenced 4 times by &8d55, &8d62, &8d6a, &8d75
.c8d30
    tya                                                               ; 8d30: 98          .     
    pha                                                               ; 8d31: 48          H     
    jsr skip_spaces_ptr2                                              ; 8d32: 20 8c 8a     ..   
    cmp #&2c ; ','                                                    ; 8d35: c9 2c       .,    
    bne c8d77                                                         ; 8d37: d0 3e       .>    
    jsr sub_c9b29                                                     ; 8d39: 20 29 9b     ).   
    jsr fwa_pack_temp1                                                ; 8d3c: 20 85 a3     ..   
    pla                                                               ; 8d3f: 68          h     
    tay                                                               ; 8d40: a8          .     
    lda zp_var_type                                                   ; 8d41: a5 27       .'    
    jsr osbput                                                        ; 8d43: 20 d4 ff     ..   
    tax                                                               ; 8d46: aa          .     
    beq c8d64                                                         ; 8d47: f0 1b       ..    
    bmi c8d57                                                         ; 8d49: 30 0c       0.    
    ldx #3                                                            ; 8d4b: a2 03       ..    
; &8d4d referenced 1 time by &8d53
.loop_c8d4d
    lda zp_iwa,x                                                      ; 8d4d: b5 2a       .*    
    jsr osbput                                                        ; 8d4f: 20 d4 ff     ..   
    dex                                                               ; 8d52: ca          .     
    bpl loop_c8d4d                                                    ; 8d53: 10 f8       ..    
    bmi c8d30                                                         ; 8d55: 30 d9       0.    
; &8d57 referenced 1 time by &8d49
.c8d57
    ldx #4                                                            ; 8d57: a2 04       ..    
; &8d59 referenced 1 time by &8d60
.loop_c8d59
    lda fp_temp1,x                                                    ; 8d59: bd 6c 04    .l.   
    jsr osbput                                                        ; 8d5c: 20 d4 ff     ..   
    dex                                                               ; 8d5f: ca          .     
    bpl loop_c8d59                                                    ; 8d60: 10 f7       ..    
    bmi c8d30                                                         ; 8d62: 30 cc       0.    
; &8d64 referenced 1 time by &8d47
.c8d64
    lda zp_strbuf_len                                                 ; 8d64: a5 36       .6    
    jsr osbput                                                        ; 8d66: 20 d4 ff     ..   
    tax                                                               ; 8d69: aa          .     
    beq c8d30                                                         ; 8d6a: f0 c4       ..    
; &8d6c referenced 1 time by &8d73
.loop_c8d6c
    lda l05ff,x                                                       ; 8d6c: bd ff 05    ...   
    jsr osbput                                                        ; 8d6f: 20 d4 ff     ..   
    dex                                                               ; 8d72: ca          .     
    bne loop_c8d6c                                                    ; 8d73: d0 f7       ..    
    beq c8d30                                                         ; 8d75: f0 b9       ..    
; &8d77 referenced 1 time by &8d37
.c8d77
    pla                                                               ; 8d77: 68          h     
    sty zp_text_ptr_off                                               ; 8d78: 84 0a       ..    
    jmp c8b98                                                         ; 8d7a: 4c 98 8b    L..   
; &8d7d referenced 3 times by &8dc8, &8dcc, &8dd0
.c8d7d
    jsr sub_cbc25                                                     ; 8d7d: 20 25 bc     %.   
; &8d80 referenced 3 times by &8d8e, &8d92, &8d96
.c8d80
    jmp c8b96                                                         ; 8d80: 4c 96 8b    L..   
; &8d83 referenced 1 time by &8ddc
.loop_c8d83
    lda #0                                                            ; 8d83: a9 00       ..    
    sta zp_print_bytes                                                ; 8d85: 85 14       ..    
    sta zp_print_flag                                                 ; 8d87: 85 15       ..    
    jsr skip_spaces                                                   ; 8d89: 20 97 8a     ..   
    cmp #&3a ; ':'                                                    ; 8d8c: c9 3a       .:    
    beq c8d80                                                         ; 8d8e: f0 f0       ..    
    cmp #&0d                                                          ; 8d90: c9 0d       ..    
    beq c8d80                                                         ; 8d92: f0 ec       ..    
    cmp #&8b                                                          ; 8d94: c9 8b       ..    
    beq c8d80                                                         ; 8d96: f0 e8       ..    
    bne c8dd2                                                         ; 8d98: d0 38       .8    
; ***************************************************************************************
; PRINT
;
; Print expressions to the screen, or a file with #, with formatting controlled by @% and
; separators. PRINT [~][items][;][,].
.stmt_print
    jsr skip_spaces                                                   ; 8d9a: 20 97 8a     ..   
    cmp #&23 ; '#'                                                    ; 8d9d: c9 23       .#    
    beq loop_c8d2b                                                    ; 8d9f: f0 8a       ..    
    dec zp_text_ptr_off                                               ; 8da1: c6 0a       ..    
    jmp c8dbb                                                         ; 8da3: 4c bb 8d    L..   
; &8da6 referenced 1 time by &8dd8
.loop_c8da6
    lda resint_at                                                     ; 8da6: ad 00 04    ...   
    beq c8dbb                                                         ; 8da9: f0 10       ..    
    lda zp_count                                                      ; 8dab: a5 1e       ..    
; &8dad referenced 1 time by &8db2
.loop_c8dad
    beq c8dbb                                                         ; 8dad: f0 0c       ..    
    sbc resint_at                                                     ; 8daf: ed 00 04    ...   
    bcs loop_c8dad                                                    ; 8db2: b0 f9       ..    
    tay                                                               ; 8db4: a8          .     
; &8db5 referenced 1 time by &8db9
.loop_c8db5
    jsr cb565                                                         ; 8db5: 20 65 b5     e.   
    iny                                                               ; 8db8: c8          .     
    bne loop_c8db5                                                    ; 8db9: d0 fa       ..    
; &8dbb referenced 3 times by &8da3, &8da9, &8dad
.c8dbb
    clc                                                               ; 8dbb: 18          .     
    lda resint_at                                                     ; 8dbc: ad 00 04    ...   
    sta zp_print_bytes                                                ; 8dbf: 85 14       ..    
; &8dc1 referenced 1 time by &8dd4
.loop_c8dc1
    ror zp_print_flag                                                 ; 8dc1: 66 15       f.    
; &8dc3 referenced 3 times by &8de1, &8e10, &8e1f
.c8dc3
    jsr skip_spaces                                                   ; 8dc3: 20 97 8a     ..   
    cmp #&3a ; ':'                                                    ; 8dc6: c9 3a       .:    
    beq c8d7d                                                         ; 8dc8: f0 b3       ..    
    cmp #&0d                                                          ; 8dca: c9 0d       ..    
    beq c8d7d                                                         ; 8dcc: f0 af       ..    
    cmp #&8b                                                          ; 8dce: c9 8b       ..    
    beq c8d7d                                                         ; 8dd0: f0 ab       ..    
; &8dd2 referenced 1 time by &8d98
.c8dd2
    cmp #&7e ; '~'                                                    ; 8dd2: c9 7e       .~    
    beq loop_c8dc1                                                    ; 8dd4: f0 eb       ..    
    cmp #&2c ; ','                                                    ; 8dd6: c9 2c       .,    
    beq loop_c8da6                                                    ; 8dd8: f0 cc       ..    
    cmp #&3b ; ';'                                                    ; 8dda: c9 3b       .;    
    beq loop_c8d83                                                    ; 8ddc: f0 a5       ..    
    jsr sub_c8e70                                                     ; 8dde: 20 70 8e     p.   
    bcc c8dc3                                                         ; 8de1: 90 e0       ..    
    lda zp_print_bytes                                                ; 8de3: a5 14       ..    
    pha                                                               ; 8de5: 48          H     
    lda zp_print_flag                                                 ; 8de6: a5 15       ..    
    pha                                                               ; 8de8: 48          H     
    dec zp_text_ptr2_off                                              ; 8de9: c6 1b       ..    
    jsr sub_c9b29                                                     ; 8deb: 20 29 9b     ).   
    pla                                                               ; 8dee: 68          h     
    sta zp_print_flag                                                 ; 8def: 85 15       ..    
    pla                                                               ; 8df1: 68          h     
    sta zp_print_bytes                                                ; 8df2: 85 14       ..    
    lda zp_text_ptr2_off                                              ; 8df4: a5 1b       ..    
    sta zp_text_ptr_off                                               ; 8df6: 85 0a       ..    
    tya                                                               ; 8df8: 98          .     
    beq c8e0e                                                         ; 8df9: f0 13       ..    
    jsr number_to_ascii                                               ; 8dfb: 20 df 9e     ..   
    lda zp_print_bytes                                                ; 8dfe: a5 14       ..    
    sec                                                               ; 8e00: 38          8     
    sbc zp_strbuf_len                                                 ; 8e01: e5 36       .6    
    bcc c8e0e                                                         ; 8e03: 90 09       ..    
    beq c8e0e                                                         ; 8e05: f0 07       ..    
    tay                                                               ; 8e07: a8          .     
; &8e08 referenced 1 time by &8e0c
.loop_c8e08
    jsr cb565                                                         ; 8e08: 20 65 b5     e.   
    dey                                                               ; 8e0b: 88          .     
    bne loop_c8e08                                                    ; 8e0c: d0 fa       ..    
; &8e0e referenced 3 times by &8df9, &8e03, &8e05
.c8e0e
    lda zp_strbuf_len                                                 ; 8e0e: a5 36       .6    
    beq c8dc3                                                         ; 8e10: f0 b1       ..    
    ldy #0                                                            ; 8e12: a0 00       ..    
; &8e14 referenced 1 time by &8e1d
.loop_c8e14
    lda string_work,y                                                 ; 8e14: b9 00 06    ...   
    jsr cb558                                                         ; 8e17: 20 58 b5     X.   
    iny                                                               ; 8e1a: c8          .     
    cpy zp_strbuf_len                                                 ; 8e1b: c4 36       .6    
    bne loop_c8e14                                                    ; 8e1d: d0 f5       ..    
    beq c8dc3                                                         ; 8e1f: f0 a2       ..    
; &8e21 referenced 1 time by &8e26
.loop_c8e21
    jmp c8aa2                                                         ; 8e21: 4c a2 8a    L..   
; &8e24 referenced 1 time by &8e48
.loop_c8e24
    cmp #&2c ; ','                                                    ; 8e24: c9 2c       .,    
    bne loop_c8e21                                                    ; 8e26: d0 f9       ..    
    lda zp_iwa                                                        ; 8e28: a5 2a       .*    
    pha                                                               ; 8e2a: 48          H     
    jsr cae56                                                         ; 8e2b: 20 56 ae     V.   
    jsr coerce_to_integer                                             ; 8e2e: 20 f0 92     ..   
    lda #&1f                                                          ; 8e31: a9 1f       ..    
    jsr oswrch                                                        ; 8e33: 20 ee ff     ..   
    pla                                                               ; 8e36: 68          h     
    jsr oswrch                                                        ; 8e37: 20 ee ff     ..   
    jsr sub_c9456                                                     ; 8e3a: 20 56 94     V.   
    jmp c8e6a                                                         ; 8e3d: 4c 6a 8e    Lj.   
; &8e40 referenced 1 time by &8e82
.loop_c8e40
    jsr sub_c92dd                                                     ; 8e40: 20 dd 92     ..   
    jsr skip_spaces_ptr2                                              ; 8e43: 20 8c 8a     ..   
    cmp #&29 ; ')'                                                    ; 8e46: c9 29       .)    
    bne loop_c8e24                                                    ; 8e48: d0 da       ..    
    lda zp_iwa                                                        ; 8e4a: a5 2a       .*    
    sbc zp_count                                                      ; 8e4c: e5 1e       ..    
    beq c8e6a                                                         ; 8e4e: f0 1a       ..    
    tay                                                               ; 8e50: a8          .     
    bcs c8e5f                                                         ; 8e51: b0 0c       ..    
    jsr sub_cbc25                                                     ; 8e53: 20 25 bc     %.   
    beq c8e5b                                                         ; 8e56: f0 03       ..    
; &8e58 referenced 1 time by &8e86
.loop_c8e58
    jsr sub_c92e3                                                     ; 8e58: 20 e3 92     ..   
; &8e5b referenced 1 time by &8e56
.c8e5b
    ldy zp_iwa                                                        ; 8e5b: a4 2a       .*    
    beq c8e6a                                                         ; 8e5d: f0 0b       ..    
; &8e5f referenced 2 times by &8e51, &8e63
.c8e5f
    jsr cb565                                                         ; 8e5f: 20 65 b5     e.   
    dey                                                               ; 8e62: 88          .     
    bne c8e5f                                                         ; 8e63: d0 fa       ..    
    beq c8e6a                                                         ; 8e65: f0 03       ..    
; &8e67 referenced 1 time by &8e7e
.loop_c8e67
    jsr sub_cbc25                                                     ; 8e67: 20 25 bc     %.   
; &8e6a referenced 5 times by &8e3d, &8e4e, &8e5d, &8e65, &8eb9
.c8e6a
    clc                                                               ; 8e6a: 18          .     
    ldy zp_text_ptr2_off                                              ; 8e6b: a4 1b       ..    
    sty zp_text_ptr_off                                               ; 8e6d: 84 0a       ..    
    rts                                                               ; 8e6f: 60          `     
; &8e70 referenced 2 times by &8dde, &8e8d
.sub_c8e70
    ldx zp_text_ptr                                                   ; 8e70: a6 0b       ..    
    stx zp_text_ptr2                                                  ; 8e72: 86 19       ..    
    ldx l000c                                                         ; 8e74: a6 0c       ..    
    stx l001a                                                         ; 8e76: 86 1a       ..    
    ldx zp_text_ptr_off                                               ; 8e78: a6 0a       ..    
    stx zp_text_ptr2_off                                              ; 8e7a: 86 1b       ..    
    cmp #&27                                                          ; 8e7c: c9 27       .'    
    beq loop_c8e67                                                    ; 8e7e: f0 e7       ..    
    cmp #&8a                                                          ; 8e80: c9 8a       ..    
    beq loop_c8e40                                                    ; 8e82: f0 bc       ..    
    cmp #&89                                                          ; 8e84: c9 89       ..    
    beq loop_c8e58                                                    ; 8e86: f0 d0       ..    
    sec                                                               ; 8e88: 38          8     
; &8e89 referenced 1 time by &8e90
.return_6
    rts                                                               ; 8e89: 60          `     
; &8e8a referenced 2 times by &ba5a, &ba5f
.sub_c8e8a
    jsr skip_spaces                                                   ; 8e8a: 20 97 8a     ..   
    jsr sub_c8e70                                                     ; 8e8d: 20 70 8e     p.   
    bcc return_6                                                      ; 8e90: 90 f7       ..    
    cmp #&22                                                          ; 8e92: c9 22       ."    
    beq c8ea7                                                         ; 8e94: f0 11       ..    
    sec                                                               ; 8e96: 38          8     
    rts                                                               ; 8e97: 60          `     
; &8e98 referenced 2 times by &8eac, &ade9
.c8e98
    brk                                                               ; 8e98: 00          .     
    equb &09                                                          ; 8e99: 09          .     
    equs "Missing ", &22                                              ; 8e9a: 4d 69 73... Mis...
    equb &00                                                          ; 8ea3: 00          .     
; &8ea4 referenced 2 times by &8eb0, &8ebb
.c8ea4
    jsr cb558                                                         ; 8ea4: 20 58 b5     X.   
; &8ea7 referenced 1 time by &8e94
.c8ea7
    iny                                                               ; 8ea7: c8          .     
    lda (zp_text_ptr2),y                                              ; 8ea8: b1 19       ..    
    cmp #&0d                                                          ; 8eaa: c9 0d       ..    
    beq c8e98                                                         ; 8eac: f0 ea       ..    
    cmp #&22                                                          ; 8eae: c9 22       ."    
    bne c8ea4                                                         ; 8eb0: d0 f2       ..    
    iny                                                               ; 8eb2: c8          .     
    sty zp_text_ptr2_off                                              ; 8eb3: 84 1b       ..    
    lda (zp_text_ptr2),y                                              ; 8eb5: b1 19       ..    
    cmp #&22                                                          ; 8eb7: c9 22       ."    
    bne c8e6a                                                         ; 8eb9: d0 af       ..    
    beq c8ea4                                                         ; 8ebb: f0 e7       ..    
; ***************************************************************************************
; CLG
;
; Clear the graphics window to the graphics background colour. CLG.
.stmt_clg
    jsr check_end_of_statement                                        ; 8ebd: 20 57 98     W.   
    lda #&10                                                          ; 8ec0: a9 10       ..    
    bne c8ecc                                                         ; 8ec2: d0 08       ..    
; ***************************************************************************************
; CLS
;
; Clear the text window to the text background colour. CLS.
.stmt_cls
    jsr check_end_of_statement                                        ; 8ec4: 20 57 98     W.   
    jsr cbc28                                                         ; 8ec7: 20 28 bc     (.   
    lda #&0c                                                          ; 8eca: a9 0c       ..    
; &8ecc referenced 1 time by &8ec2
.c8ecc
    jsr oswrch                                                        ; 8ecc: 20 ee ff     ..   
    jmp statement_loop                                                ; 8ecf: 4c 9b 8b    L..   
; ***************************************************************************************
; CALL
;
; Call machine code, passing the resident integer variables and an optional parameter
; block. CALL address [,params...].
.stmt_call
    jsr eval_expr                                                     ; 8ed2: 20 1d 9b     ..   
    jsr sub_c92ee                                                     ; 8ed5: 20 ee 92     ..   
    jsr stack_integer                                                 ; 8ed8: 20 94 bd     ..   
    ldy #0                                                            ; 8edb: a0 00       ..    
    sty string_work                                                   ; 8edd: 8c 00 06    ...   
; &8ee0 referenced 1 time by &8f09
.c8ee0
    sty l06ff                                                         ; 8ee0: 8c ff 06    ...   
    jsr skip_spaces_ptr2                                              ; 8ee3: 20 8c 8a     ..   
    cmp #&2c ; ','                                                    ; 8ee6: c9 2c       .,    
    bne c8f0c                                                         ; 8ee8: d0 22       ."    
    ldy zp_text_ptr2_off                                              ; 8eea: a4 1b       ..    
    jsr sub_c95d5                                                     ; 8eec: 20 d5 95     ..   
    beq c8f1b                                                         ; 8eef: f0 2a       .*    
    ldy l06ff                                                         ; 8ef1: ac ff 06    ...   
    iny                                                               ; 8ef4: c8          .     
    lda zp_iwa                                                        ; 8ef5: a5 2a       .*    
    sta string_work,y                                                 ; 8ef7: 99 00 06    ...   
    iny                                                               ; 8efa: c8          .     
    lda zp_iwa_1                                                      ; 8efb: a5 2b       .+    
    sta string_work,y                                                 ; 8efd: 99 00 06    ...   
    iny                                                               ; 8f00: c8          .     
    lda zp_iwa_2                                                      ; 8f01: a5 2c       .,    
    sta string_work,y                                                 ; 8f03: 99 00 06    ...   
    inc string_work                                                   ; 8f06: ee 00 06    ...   
    jmp c8ee0                                                         ; 8f09: 4c e0 8e    L..   
; &8f0c referenced 1 time by &8ee8
.c8f0c
    dec zp_text_ptr2_off                                              ; 8f0c: c6 1b       ..    
    jsr sub_c9852                                                     ; 8f0e: 20 52 98     R.   
    jsr unstack_integer                                               ; 8f11: 20 ea bd     ..   
    jsr sub_c8f1e                                                     ; 8f14: 20 1e 8f     ..   
    cld                                                               ; 8f17: d8          .     
    jmp statement_loop                                                ; 8f18: 4c 9b 8b    L..   
; &8f1b referenced 1 time by &8eef
.c8f1b
    jmp cae43                                                         ; 8f1b: 4c 43 ae    LC.   
; &8f1e referenced 2 times by &8f14, &abd5
.sub_c8f1e
    lda resint_c                                                      ; 8f1e: ad 0c 04    ...   
    lsr a                                                             ; 8f21: 4a          J     
    lda resint_a                                                      ; 8f22: ad 04 04    ...   
    ldx resint_x                                                      ; 8f25: ae 60 04    .`.   
    ldy resint_y                                                      ; 8f28: ac 64 04    .d.   
    jmp (zp_iwa)                                                      ; 8f2b: 6c 2a 00    l*.   
; &8f2e referenced 3 times by &8f34, &8f3e, &8f43
.c8f2e
    jmp c982a                                                         ; 8f2e: 4c 2a 98    L*.   
; ***************************************************************************************
; DELETE
;
; Delete a range of program lines. DELETE start, end.
.stmt_delete
    jsr sub_c97df                                                     ; 8f31: 20 df 97     ..   
    bcc c8f2e                                                         ; 8f34: 90 f8       ..    
    jsr stack_integer                                                 ; 8f36: 20 94 bd     ..   
    jsr skip_spaces                                                   ; 8f39: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 8f3c: c9 2c       .,    
    bne c8f2e                                                         ; 8f3e: d0 ee       ..    
    jsr sub_c97df                                                     ; 8f40: 20 df 97     ..   
    bcc c8f2e                                                         ; 8f43: 90 e9       ..    
    jsr check_end_of_statement                                        ; 8f45: 20 57 98     W.   
    lda zp_iwa                                                        ; 8f48: a5 2a       .*    
    sta zp_fileblk                                                    ; 8f4a: 85 39       .9    
    lda zp_iwa_1                                                      ; 8f4c: a5 2b       .+    
    sta l003a                                                         ; 8f4e: 85 3a       .:    
    jsr unstack_integer                                               ; 8f50: 20 ea bd     ..   
; &8f53 referenced 1 time by &8f64
.loop_c8f53
    jsr sub_cbc2d                                                     ; 8f53: 20 2d bc     -.   
    jsr sub_c987b                                                     ; 8f56: 20 7b 98     {.   
    jsr sub_c9222                                                     ; 8f59: 20 22 92     ".   
    lda zp_fileblk                                                    ; 8f5c: a5 39       .9    
    cmp zp_iwa                                                        ; 8f5e: c5 2a       .*    
    lda l003a                                                         ; 8f60: a5 3a       .:    
    sbc zp_iwa_1                                                      ; 8f62: e5 2b       .+    
    bcs loop_c8f53                                                    ; 8f64: b0 ed       ..    
    jmp c8af3                                                         ; 8f66: 4c f3 8a    L..   
; &8f69 referenced 2 times by &8fa3, &90ac
.sub_c8f69
    lda #&0a                                                          ; 8f69: a9 0a       ..    
    jsr caed8                                                         ; 8f6b: 20 d8 ae     ..   
    jsr sub_c97df                                                     ; 8f6e: 20 df 97     ..   
    jsr stack_integer                                                 ; 8f71: 20 94 bd     ..   
    lda #&0a                                                          ; 8f74: a9 0a       ..    
    jsr caed8                                                         ; 8f76: 20 d8 ae     ..   
    jsr skip_spaces                                                   ; 8f79: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 8f7c: c9 2c       .,    
    bne c8f8d                                                         ; 8f7e: d0 0d       ..    
    jsr sub_c97df                                                     ; 8f80: 20 df 97     ..   
    lda zp_iwa_1                                                      ; 8f83: a5 2b       .+    
    bne c8fdf                                                         ; 8f85: d0 58       .X    
    lda zp_iwa                                                        ; 8f87: a5 2a       .*    
    beq c8fdf                                                         ; 8f89: f0 54       .T    
    inc zp_text_ptr_off                                               ; 8f8b: e6 0a       ..    
; &8f8d referenced 1 time by &8f7e
.c8f8d
    dec zp_text_ptr_off                                               ; 8f8d: c6 0a       ..    
    jmp check_end_of_statement                                        ; 8f8f: 4c 57 98    LW.   
; &8f92 referenced 2 times by &8fae, &9040
.sub_c8f92
    lda zp_top                                                        ; 8f92: a5 12       ..    
    sta zp_fwb_sign                                                   ; 8f94: 85 3b       .;    
    lda l0013                                                         ; 8f96: a5 13       ..    
    sta zp_fwb_ovf                                                    ; 8f98: 85 3c       .<    
; &8f9a referenced 1 time by &8fe7
.sub_c8f9a
    lda zp_page                                                       ; 8f9a: a5 18       ..    
    sta l0038                                                         ; 8f9c: 85 38       .8    
    lda #1                                                            ; 8f9e: a9 01       ..    
    sta zp_general                                                    ; 8fa0: 85 37       .7    
    rts                                                               ; 8fa2: 60          `     
; ***************************************************************************************
; RENUMBER
;
; Renumber program lines and fix up line references. RENUMBER [start[,step]].
.stmt_renumber
    jsr sub_c8f69                                                     ; 8fa3: 20 69 8f     i.   
    ldx #&39 ; '9'                                                    ; 8fa6: a2 39       .9    
    jsr sub_cbe0d                                                     ; 8fa8: 20 0d be     ..   
    jsr sub_cbe6f                                                     ; 8fab: 20 6f be     o.   
    jsr sub_c8f92                                                     ; 8fae: 20 92 8f     ..   
; &8fb1 referenced 1 time by &8fd4
.loop_c8fb1
    ldy #0                                                            ; 8fb1: a0 00       ..    
    lda (zp_general),y                                                ; 8fb3: b1 37       .7    
    bmi c8fe7                                                         ; 8fb5: 30 30       00    
    sta (zp_fwb_sign),y                                               ; 8fb7: 91 3b       .;    
    iny                                                               ; 8fb9: c8          .     
    lda (zp_general),y                                                ; 8fba: b1 37       .7    
    sta (zp_fwb_sign),y                                               ; 8fbc: 91 3b       .;    
    sec                                                               ; 8fbe: 38          8     
    tya                                                               ; 8fbf: 98          .     
    adc zp_fwb_sign                                                   ; 8fc0: 65 3b       e;    
    sta zp_fwb_sign                                                   ; 8fc2: 85 3b       .;    
    tax                                                               ; 8fc4: aa          .     
    lda zp_fwb_ovf                                                    ; 8fc5: a5 3c       .<    
    adc #0                                                            ; 8fc7: 69 00       i.    
    sta zp_fwb_ovf                                                    ; 8fc9: 85 3c       .<    
    cpx zp_himem                                                      ; 8fcb: e4 06       ..    
    sbc l0007                                                         ; 8fcd: e5 07       ..    
    bcs c8fd6                                                         ; 8fcf: b0 05       ..    
    jsr sub_c909f                                                     ; 8fd1: 20 9f 90     ..   
    bcc loop_c8fb1                                                    ; 8fd4: 90 db       ..    
; &8fd6 referenced 1 time by &8fcf
.c8fd6
    brk                                                               ; 8fd6: 00          .     
    equb &00, &cc                                                     ; 8fd7: 00 cc       ..    
    equs " space"                                                     ; 8fd9: 20 73 70...  sp...
; &8fdf referenced 2 times by &8f85, &8f89
.c8fdf
    brk                                                               ; 8fdf: 00          .     
    equb &00                                                          ; 8fe0: 00          .     
    equs "Silly"                                                      ; 8fe1: 53 69 6c... Sil...
    equb &00                                                          ; 8fe6: 00          .     
; &8fe7 referenced 1 time by &8fb5
.c8fe7
    jsr sub_c8f9a                                                     ; 8fe7: 20 9a 8f     ..   
; &8fea referenced 1 time by &900b
.loop_c8fea
    ldy #0                                                            ; 8fea: a0 00       ..    
    lda (zp_general),y                                                ; 8fec: b1 37       .7    
    bmi c900d                                                         ; 8fee: 30 1d       0.    
    lda l003a                                                         ; 8ff0: a5 3a       .:    
    sta (zp_general),y                                                ; 8ff2: 91 37       .7    
    lda zp_fileblk                                                    ; 8ff4: a5 39       .9    
    iny                                                               ; 8ff6: c8          .     
    sta (zp_general),y                                                ; 8ff7: 91 37       .7    
    clc                                                               ; 8ff9: 18          .     
    lda zp_iwa                                                        ; 8ffa: a5 2a       .*    
    adc zp_fileblk                                                    ; 8ffc: 65 39       e9    
    sta zp_fileblk                                                    ; 8ffe: 85 39       .9    
    lda #0                                                            ; 9000: a9 00       ..    
    adc l003a                                                         ; 9002: 65 3a       e:    
    and #&7f                                                          ; 9004: 29 7f       ).    
    sta l003a                                                         ; 9006: 85 3a       .:    
    jsr sub_c909f                                                     ; 9008: 20 9f 90     ..   
    bcc loop_c8fea                                                    ; 900b: 90 dd       ..    
; &900d referenced 1 time by &8fee
.c900d
    lda zp_page                                                       ; 900d: a5 18       ..    
    sta l000c                                                         ; 900f: 85 0c       ..    
    ldy #0                                                            ; 9011: a0 00       ..    
    sty zp_text_ptr                                                   ; 9013: 84 0b       ..    
    iny                                                               ; 9015: c8          .     
    lda (zp_text_ptr),y                                               ; 9016: b1 0b       ..    
    bmi c903a                                                         ; 9018: 30 20       0     
; &901a referenced 2 times by &9034, &9038
.c901a
    ldy #4                                                            ; 901a: a0 04       ..    
; &901c referenced 2 times by &9025, &906f
.c901c
    lda (zp_text_ptr),y                                               ; 901c: b1 0b       ..    
    cmp #&8d                                                          ; 901e: c9 8d       ..    
    beq c903d                                                         ; 9020: f0 1b       ..    
    iny                                                               ; 9022: c8          .     
    cmp #&0d                                                          ; 9023: c9 0d       ..    
    bne c901c                                                         ; 9025: d0 f5       ..    
    lda (zp_text_ptr),y                                               ; 9027: b1 0b       ..    
    bmi c903a                                                         ; 9029: 30 0f       0.    
    ldy #3                                                            ; 902b: a0 03       ..    
    lda (zp_text_ptr),y                                               ; 902d: b1 0b       ..    
    clc                                                               ; 902f: 18          .     
    adc zp_text_ptr                                                   ; 9030: 65 0b       e.    
    sta zp_text_ptr                                                   ; 9032: 85 0b       ..    
    bcc c901a                                                         ; 9034: 90 e4       ..    
    inc l000c                                                         ; 9036: e6 0c       ..    
    bcs c901a                                                         ; 9038: b0 e0       ..    
; &903a referenced 2 times by &9018, &9029
.c903a
    jmp c8af3                                                         ; 903a: 4c f3 8a    L..   
; &903d referenced 1 time by &9020
.c903d
    jsr sub_c97eb                                                     ; 903d: 20 eb 97     ..   
    jsr sub_c8f92                                                     ; 9040: 20 92 8f     ..   
; &9043 referenced 2 times by &907a, &907e
.c9043
    ldy #0                                                            ; 9043: a0 00       ..    
    lda (zp_general),y                                                ; 9045: b1 37       .7    
    bmi c9080                                                         ; 9047: 30 37       07    
    lda (zp_fwb_sign),y                                               ; 9049: b1 3b       .;    
    iny                                                               ; 904b: c8          .     
    cmp zp_iwa_1                                                      ; 904c: c5 2b       .+    
    bne c9071                                                         ; 904e: d0 21       .!    
    lda (zp_fwb_sign),y                                               ; 9050: b1 3b       .;    
    cmp zp_iwa                                                        ; 9052: c5 2a       .*    
    bne c9071                                                         ; 9054: d0 1b       ..    
    lda (zp_general),y                                                ; 9056: b1 37       .7    
    sta zp_fwb_exp                                                    ; 9058: 85 3d       .=    
    dey                                                               ; 905a: 88          .     
    lda (zp_general),y                                                ; 905b: b1 37       .7    
    sta zp_fwb_m1                                                     ; 905d: 85 3e       .>    
    ldy zp_text_ptr_off                                               ; 905f: a4 0a       ..    
    dey                                                               ; 9061: 88          .     
    lda zp_text_ptr                                                   ; 9062: a5 0b       ..    
    sta zp_general                                                    ; 9064: 85 37       .7    
    lda l000c                                                         ; 9066: a5 0c       ..    
    sta l0038                                                         ; 9068: 85 38       .8    
    jsr sub_c88f5                                                     ; 906a: 20 f5 88     ..   
    ldy zp_text_ptr_off                                               ; 906d: a4 0a       ..    
    bne c901c                                                         ; 906f: d0 ab       ..    
; &9071 referenced 2 times by &904e, &9054
.c9071
    jsr sub_c909f                                                     ; 9071: 20 9f 90     ..   
    lda zp_fwb_sign                                                   ; 9074: a5 3b       .;    
    adc #2                                                            ; 9076: 69 02       i.    
    sta zp_fwb_sign                                                   ; 9078: 85 3b       .;    
    bcc c9043                                                         ; 907a: 90 c7       ..    
    inc zp_fwb_ovf                                                    ; 907c: e6 3c       .<    
    bcs c9043                                                         ; 907e: b0 c3       ..    
; &9080 referenced 1 time by &9047
.c9080
    jsr sub_cbfcf                                                     ; 9080: 20 cf bf     ..   
    lsr l0061                                                         ; 9083: 46 61       Fa    
    adc #&6c ; 'l'                                                    ; 9085: 69 6c       il    
    adc l0064                                                         ; 9087: 65 64       ed    
    jsr l7461                                                         ; 9089: 20 61 74     at   
    jsr sub_cb1c8                                                     ; 908c: 20 c8 b1     ..   
    equb &0b, &85, &2b, &c8, &b1, &0b, &85, &2a, &20, &1f, &99, &20   ; 908f: 0b 85 2b... ..+...
    equb &25, &bc, &f0, &ce                                           ; 909b: 25 bc f0... %.....
; &909f referenced 3 times by &8fd1, &9008, &9071
.sub_c909f
    iny                                                               ; 909f: c8          .     
    lda (zp_general),y                                                ; 90a0: b1 37       .7    
    adc zp_general                                                    ; 90a2: 65 37       e7    
    sta zp_general                                                    ; 90a4: 85 37       .7    
    bcc return_7                                                      ; 90a6: 90 03       ..    
    inc l0038                                                         ; 90a8: e6 38       .8    
    clc                                                               ; 90aa: 18          .     
; &90ab referenced 1 time by &90a6
.return_7
    rts                                                               ; 90ab: 60          `     
; ***************************************************************************************
; AUTO
;
; Generate line numbers automatically during program entry until Escape. AUTO
; [start[,step]].
.stmt_auto
    jsr sub_c8f69                                                     ; 90ac: 20 69 8f     i.   
    lda zp_iwa                                                        ; 90af: a5 2a       .*    
    pha                                                               ; 90b1: 48          H     
    jsr unstack_integer                                               ; 90b2: 20 ea bd     ..   
; &90b5 referenced 2 times by &90d3, &90d7
.c90b5
    jsr stack_integer                                                 ; 90b5: 20 94 bd     ..   
    jsr sub_c9923                                                     ; 90b8: 20 23 99     #.   
    lda #&20 ; ' '                                                    ; 90bb: a9 20       .     
    jsr sub_cbc02                                                     ; 90bd: 20 02 bc     ..   
    jsr unstack_integer                                               ; 90c0: 20 ea bd     ..   
    jsr tokenise_line                                                 ; 90c3: 20 51 89     Q.   
    jsr sub_cbc8d                                                     ; 90c6: 20 8d bc     ..   
    jsr sub_cbd20                                                     ; 90c9: 20 20 bd      .   
    pla                                                               ; 90cc: 68          h     
    pha                                                               ; 90cd: 48          H     
    clc                                                               ; 90ce: 18          .     
    adc zp_iwa                                                        ; 90cf: 65 2a       e*    
    sta zp_iwa                                                        ; 90d1: 85 2a       .*    
    bcc c90b5                                                         ; 90d3: 90 e0       ..    
    inc zp_iwa_1                                                      ; 90d5: e6 2b       .+    
    bpl c90b5                                                         ; 90d7: 10 dc       ..    
    jmp c8af3                                                         ; 90d9: 4c f3 8a    L..   
; &90dc referenced 1 time by &9106
.loop_c90dc
    jmp c9218                                                         ; 90dc: 4c 18 92    L..   
; &90df referenced 1 time by &9168
.c90df
    dec zp_text_ptr_off                                               ; 90df: c6 0a       ..    
    jsr sub_c9582                                                     ; 90e1: 20 82 95     ..   
    beq c9127                                                         ; 90e4: f0 41       .A    
    bcs c9127                                                         ; 90e6: b0 3f       .?    
    jsr stack_integer                                                 ; 90e8: 20 94 bd     ..   
    jsr sub_c92dd                                                     ; 90eb: 20 dd 92     ..   
    jsr sub_c9222                                                     ; 90ee: 20 22 92     ".   
    lda zp_iwa_3                                                      ; 90f1: a5 2d       .-    
    ora zp_iwa_2                                                      ; 90f3: 05 2c       .,    
    bne c9127                                                         ; 90f5: d0 30       .0    
    clc                                                               ; 90f7: 18          .     
    lda zp_iwa                                                        ; 90f8: a5 2a       .*    
    adc zp_vartop                                                     ; 90fa: 65 02       e.    
    tay                                                               ; 90fc: a8          .     
    lda zp_iwa_1                                                      ; 90fd: a5 2b       .+    
    adc zp_vartop_1                                                   ; 90ff: 65 03       e.    
    tax                                                               ; 9101: aa          .     
    cpy zp_stack_ptr                                                  ; 9102: c4 04       ..    
    sbc zp_stack_ptr_1                                                ; 9104: e5 05       ..    
    bcs loop_c90dc                                                    ; 9106: b0 d4       ..    
    lda zp_vartop                                                     ; 9108: a5 02       ..    
    sta zp_iwa                                                        ; 910a: 85 2a       .*    
    lda zp_vartop_1                                                   ; 910c: a5 03       ..    
    sta zp_iwa_1                                                      ; 910e: 85 2b       .+    
    sty zp_vartop                                                     ; 9110: 84 02       ..    
    stx zp_vartop_1                                                   ; 9112: 86 03       ..    
    lda #0                                                            ; 9114: a9 00       ..    
    sta zp_iwa_2                                                      ; 9116: 85 2c       .,    
    sta zp_iwa_3                                                      ; 9118: 85 2d       .-    
    lda #&40 ; '@'                                                    ; 911a: a9 40       .@    
    sta zp_var_type                                                   ; 911c: 85 27       .'    
    jsr sub_cb4b4                                                     ; 911e: 20 b4 b4     ..   
    jsr sub_c8827                                                     ; 9121: 20 27 88     '.   
    jmp c920b                                                         ; 9124: 4c 0b 92    L..   
; &9127 referenced 8 times by &90e4, &90e6, &90f5, &9150, &9172, &9193, &91b4, &925a
.c9127
    brk                                                               ; 9127: 00          .     
    equb &0a                                                          ; 9128: 0a          .     
    equs "Bad "                                                       ; 9129: 42 61 64... Bad...
    equb &de, &00                                                     ; 912d: de 00       ..    
; ***************************************************************************************
; DIM
;
; Dimension an array, or reserve a block of bytes. DIM var(subscripts) | DIM var size.
; &912f referenced 1 time by &9215
.stmt_dim
    jsr skip_spaces                                                   ; 912f: 20 97 8a     ..   
    tya                                                               ; 9132: 98          .     
    clc                                                               ; 9133: 18          .     
    adc zp_text_ptr                                                   ; 9134: 65 0b       e.    
    ldx l000c                                                         ; 9136: a6 0c       ..    
    bcc c913c                                                         ; 9138: 90 02       ..    
    inx                                                               ; 913a: e8          .     
    clc                                                               ; 913b: 18          .     
; &913c referenced 1 time by &9138
.c913c
    sbc #0                                                            ; 913c: e9 00       ..    
    sta zp_general                                                    ; 913e: 85 37       .7    
    txa                                                               ; 9140: 8a          .     
    sbc #0                                                            ; 9141: e9 00       ..    
    sta l0038                                                         ; 9143: 85 38       .8    
    ldx #5                                                            ; 9145: a2 05       ..    
    stx zp_fwb_m2                                                     ; 9147: 86 3f       .?    
    ldx zp_text_ptr_off                                               ; 9149: a6 0a       ..    
    jsr sub_c9559                                                     ; 914b: 20 59 95     Y.   
    cpy #1                                                            ; 914e: c0 01       ..    
    beq c9127                                                         ; 9150: f0 d5       ..    
    cmp #&28 ; '('                                                    ; 9152: c9 28       .(    
    beq c916b                                                         ; 9154: f0 15       ..    
    cmp #&24 ; '$'                                                    ; 9156: c9 24       .$    
    beq c915e                                                         ; 9158: f0 04       ..    
    cmp #&25 ; '%'                                                    ; 915a: c9 25       .%    
    bne c9168                                                         ; 915c: d0 0a       ..    
; &915e referenced 1 time by &9158
.c915e
    dec zp_fwb_m2                                                     ; 915e: c6 3f       .?    
    iny                                                               ; 9160: c8          .     
    inx                                                               ; 9161: e8          .     
    lda (zp_general),y                                                ; 9162: b1 37       .7    
    cmp #&28 ; '('                                                    ; 9164: c9 28       .(    
    beq c916b                                                         ; 9166: f0 03       ..    
; &9168 referenced 1 time by &915c
.c9168
    jmp c90df                                                         ; 9168: 4c df 90    L..   
; &916b referenced 2 times by &9154, &9166
.c916b
    sty zp_fileblk                                                    ; 916b: 84 39       .9    
    stx zp_text_ptr_off                                               ; 916d: 86 0a       ..    
    jsr find_variable                                                 ; 916f: 20 69 94     i.   
    bne c9127                                                         ; 9172: d0 b3       ..    
    jsr sub_c94fc                                                     ; 9174: 20 fc 94     ..   
    ldx #1                                                            ; 9177: a2 01       ..    
    jsr sub_c9531                                                     ; 9179: 20 31 95     1.   
    lda zp_fwb_m2                                                     ; 917c: a5 3f       .?    
    pha                                                               ; 917e: 48          H     
    lda #1                                                            ; 917f: a9 01       ..    
    pha                                                               ; 9181: 48          H     
    jsr caed8                                                         ; 9182: 20 d8 ae     ..   
; &9185 referenced 1 time by &91ae
.loop_c9185
    jsr stack_integer                                                 ; 9185: 20 94 bd     ..   
    jsr eval_expr_to_integer                                          ; 9188: 20 21 88     !.   
    lda zp_iwa_1                                                      ; 918b: a5 2b       .+    
    and #&c0                                                          ; 918d: 29 c0       ).    
    ora zp_iwa_2                                                      ; 918f: 05 2c       .,    
    ora zp_iwa_3                                                      ; 9191: 05 2d       .-    
    bne c9127                                                         ; 9193: d0 92       ..    
    jsr sub_c9222                                                     ; 9195: 20 22 92     ".   
    pla                                                               ; 9198: 68          h     
    tay                                                               ; 9199: a8          .     
    lda zp_iwa                                                        ; 919a: a5 2a       .*    
    sta (zp_vartop),y                                                 ; 919c: 91 02       ..    
    iny                                                               ; 919e: c8          .     
    lda zp_iwa_1                                                      ; 919f: a5 2b       .+    
    sta (zp_vartop),y                                                 ; 91a1: 91 02       ..    
    iny                                                               ; 91a3: c8          .     
    tya                                                               ; 91a4: 98          .     
    pha                                                               ; 91a5: 48          H     
    jsr sub_c9231                                                     ; 91a6: 20 31 92     1.   
    jsr skip_spaces                                                   ; 91a9: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 91ac: c9 2c       .,    
    beq loop_c9185                                                    ; 91ae: f0 d5       ..    
    cmp #&29 ; ')'                                                    ; 91b0: c9 29       .)    
    beq c91b7                                                         ; 91b2: f0 03       ..    
    jmp c9127                                                         ; 91b4: 4c 27 91    L'.   
; &91b7 referenced 1 time by &91b2
.c91b7
    pla                                                               ; 91b7: 68          h     
    sta zp_print_flag                                                 ; 91b8: 85 15       ..    
    pla                                                               ; 91ba: 68          h     
    sta zp_fwb_m2                                                     ; 91bb: 85 3f       .?    
    lda #0                                                            ; 91bd: a9 00       ..    
    sta zp_fwb_m3                                                     ; 91bf: 85 40       .@    
    jsr sub_c9236                                                     ; 91c1: 20 36 92     6.   
    ldy #0                                                            ; 91c4: a0 00       ..    
    lda zp_print_flag                                                 ; 91c6: a5 15       ..    
    sta (zp_vartop),y                                                 ; 91c8: 91 02       ..    
    adc zp_iwa                                                        ; 91ca: 65 2a       e*    
    sta zp_iwa                                                        ; 91cc: 85 2a       .*    
    bcc c91d2                                                         ; 91ce: 90 02       ..    
    inc zp_iwa_1                                                      ; 91d0: e6 2b       .+    
; &91d2 referenced 1 time by &91ce
.c91d2
    lda zp_vartop_1                                                   ; 91d2: a5 03       ..    
    sta l0038                                                         ; 91d4: 85 38       .8    
    lda zp_vartop                                                     ; 91d6: a5 02       ..    
    sta zp_general                                                    ; 91d8: 85 37       .7    
    clc                                                               ; 91da: 18          .     
    adc zp_iwa                                                        ; 91db: 65 2a       e*    
    tay                                                               ; 91dd: a8          .     
    lda zp_iwa_1                                                      ; 91de: a5 2b       .+    
    adc zp_vartop_1                                                   ; 91e0: 65 03       e.    
    bcs c9218                                                         ; 91e2: b0 34       .4    
    tax                                                               ; 91e4: aa          .     
    cpy zp_stack_ptr                                                  ; 91e5: c4 04       ..    
    sbc zp_stack_ptr_1                                                ; 91e7: e5 05       ..    
    bcs c9218                                                         ; 91e9: b0 2d       .-    
    sty zp_vartop                                                     ; 91eb: 84 02       ..    
    stx zp_vartop_1                                                   ; 91ed: 86 03       ..    
    lda zp_general                                                    ; 91ef: a5 37       .7    
    adc zp_print_flag                                                 ; 91f1: 65 15       e.    
    tay                                                               ; 91f3: a8          .     
    lda #0                                                            ; 91f4: a9 00       ..    
    sta zp_general                                                    ; 91f6: 85 37       .7    
    bcc c91fc                                                         ; 91f8: 90 02       ..    
    inc l0038                                                         ; 91fa: e6 38       .8    
; &91fc referenced 3 times by &91f8, &9205, &9209
.c91fc
    sta (zp_general),y                                                ; 91fc: 91 37       .7    
    iny                                                               ; 91fe: c8          .     
    bne c9203                                                         ; 91ff: d0 02       ..    
    inc l0038                                                         ; 9201: e6 38       .8    
; &9203 referenced 1 time by &91ff
.c9203
    cpy zp_vartop                                                     ; 9203: c4 02       ..    
    bne c91fc                                                         ; 9205: d0 f5       ..    
    cpx l0038                                                         ; 9207: e4 38       .8    
    bne c91fc                                                         ; 9209: d0 f1       ..    
; &920b referenced 1 time by &9124
.c920b
    jsr skip_spaces                                                   ; 920b: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 920e: c9 2c       .,    
    beq c9215                                                         ; 9210: f0 03       ..    
    jmp c8b96                                                         ; 9212: 4c 96 8b    L..   
; &9215 referenced 1 time by &9210
.c9215
    jmp stmt_dim                                                      ; 9215: 4c 2f 91    L/.   
; &9218 referenced 3 times by &90dc, &91e2, &91e9
.c9218
    brk                                                               ; 9218: 00          .     
    equb &0b, &de                                                     ; 9219: 0b de       ..    
    equs " space"                                                     ; 921b: 20 73 70...  sp...
    equb &00                                                          ; 9221: 00          .     
; &9222 referenced 4 times by &8f59, &90ee, &9195, &af39
.sub_c9222
    inc zp_iwa                                                        ; 9222: e6 2a       .*    
    bne return_8                                                      ; 9224: d0 0a       ..    
    inc zp_iwa_1                                                      ; 9226: e6 2b       .+    
    bne return_8                                                      ; 9228: d0 06       ..    
    inc zp_iwa_2                                                      ; 922a: e6 2c       .,    
    bne return_8                                                      ; 922c: d0 02       ..    
    inc zp_iwa_3                                                      ; 922e: e6 2d       .-    
; &9230 referenced 3 times by &9224, &9228, &922c
.return_8
    rts                                                               ; 9230: 60          `     
; &9231 referenced 1 time by &91a6
.sub_c9231
    ldx #&3f ; '?'                                                    ; 9231: a2 3f       .?    
    jsr sub_cbe0d                                                     ; 9233: 20 0d be     ..   
; &9236 referenced 2 times by &91c1, &9736
.sub_c9236
    ldx #0                                                            ; 9236: a2 00       ..    
    ldy #0                                                            ; 9238: a0 00       ..    
; &923a referenced 1 time by &9253
.loop_c923a
    lsr zp_fwb_m3                                                     ; 923a: 46 40       F@    
    ror zp_fwb_m2                                                     ; 923c: 66 3f       f?    
    bcc c924b                                                         ; 923e: 90 0b       ..    
    clc                                                               ; 9240: 18          .     
    tya                                                               ; 9241: 98          .     
    adc zp_iwa                                                        ; 9242: 65 2a       e*    
    tay                                                               ; 9244: a8          .     
    txa                                                               ; 9245: 8a          .     
    adc zp_iwa_1                                                      ; 9246: 65 2b       e+    
    tax                                                               ; 9248: aa          .     
    bcs c925a                                                         ; 9249: b0 0f       ..    
; &924b referenced 1 time by &923e
.c924b
    asl zp_iwa                                                        ; 924b: 06 2a       .*    
    rol zp_iwa_1                                                      ; 924d: 26 2b       &+    
    lda zp_fwb_m2                                                     ; 924f: a5 3f       .?    
    ora zp_fwb_m3                                                     ; 9251: 05 40       .@    
    bne loop_c923a                                                    ; 9253: d0 e5       ..    
    sty zp_iwa                                                        ; 9255: 84 2a       .*    
    stx zp_iwa_1                                                      ; 9257: 86 2b       .+    
    rts                                                               ; 9259: 60          `     
; &925a referenced 1 time by &9249
.c925a
    jmp c9127                                                         ; 925a: 4c 27 91    L'.   
; ***************************************************************************************
; HIMEM=
;
; Set HIMEM, the top of memory available to BASIC. HIMEM = address.
.stmt_himem
    jsr sub_c92eb                                                     ; 925d: 20 eb 92     ..   
    lda zp_iwa                                                        ; 9260: a5 2a       .*    
    sta zp_himem                                                      ; 9262: 85 06       ..    
    sta zp_stack_ptr                                                  ; 9264: 85 04       ..    
    lda zp_iwa_1                                                      ; 9266: a5 2b       .+    
    sta l0007                                                         ; 9268: 85 07       ..    
    sta zp_stack_ptr_1                                                ; 926a: 85 05       ..    
    jmp statement_loop                                                ; 926c: 4c 9b 8b    L..   
; ***************************************************************************************
; LOMEM=
;
; Set LOMEM, the start of variable storage. LOMEM = address.
.stmt_lomem
    jsr sub_c92eb                                                     ; 926f: 20 eb 92     ..   
    lda zp_iwa                                                        ; 9272: a5 2a       .*    
    sta zp_lomem                                                      ; 9274: 85 00       ..    
    sta zp_vartop                                                     ; 9276: 85 02       ..    
    lda zp_iwa_1                                                      ; 9278: a5 2b       .+    
    sta l0001                                                         ; 927a: 85 01       ..    
    sta zp_vartop_1                                                   ; 927c: 85 03       ..    
    jsr sub_cbd2f                                                     ; 927e: 20 2f bd     /.   
    beq c928a                                                         ; 9281: f0 07       ..    
; ***************************************************************************************
; PAGE=
;
; Set PAGE, the start of the BASIC program. PAGE = address.
.stmt_page
    jsr sub_c92eb                                                     ; 9283: 20 eb 92     ..   
    lda zp_iwa_1                                                      ; 9286: a5 2b       .+    
    sta zp_page                                                       ; 9288: 85 18       ..    
; &928a referenced 2 times by &9281, &9293
.c928a
    jmp statement_loop                                                ; 928a: 4c 9b 8b    L..   
; ***************************************************************************************
; CLEAR
;
; Discard all variables and the stack. CLEAR.
.stmt_clear
    jsr check_end_of_statement                                        ; 928d: 20 57 98     W.   
    jsr sub_cbd20                                                     ; 9290: 20 20 bd      .   
    beq c928a                                                         ; 9293: f0 f5       ..    
; ***************************************************************************************
; TRACE
;
; Trace executed line numbers for debugging. TRACE ON | OFF | line.
.stmt_trace
    jsr sub_c97df                                                     ; 9295: 20 df 97     ..   
    bcs c92a5                                                         ; 9298: b0 0b       ..    
    cmp #&ee                                                          ; 929a: c9 ee       ..    
    beq c92b7                                                         ; 929c: f0 19       ..    
    cmp #&87                                                          ; 929e: c9 87       ..    
    beq c92c0                                                         ; 92a0: f0 1e       ..    
    jsr eval_expr_to_integer                                          ; 92a2: 20 21 88     !.   
; &92a5 referenced 1 time by &9298
.c92a5
    jsr check_end_of_statement                                        ; 92a5: 20 57 98     W.   
    lda zp_iwa                                                        ; 92a8: a5 2a       .*    
    sta zp_trace_max                                                  ; 92aa: 85 21       .!    
    lda zp_iwa_1                                                      ; 92ac: a5 2b       .+    
; &92ae referenced 1 time by &92be
.loop_c92ae
    sta l0022                                                         ; 92ae: 85 22       ."    
    lda #&ff                                                          ; 92b0: a9 ff       ..    
; &92b2 referenced 1 time by &92c7
.loop_c92b2
    sta zp_trace_flag                                                 ; 92b2: 85 20       .     
    jmp statement_loop                                                ; 92b4: 4c 9b 8b    L..   
; &92b7 referenced 1 time by &929c
.c92b7
    inc zp_text_ptr_off                                               ; 92b7: e6 0a       ..    
    jsr check_end_of_statement                                        ; 92b9: 20 57 98     W.   
    lda #&ff                                                          ; 92bc: a9 ff       ..    
    bne loop_c92ae                                                    ; 92be: d0 ee       ..    
; &92c0 referenced 1 time by &92a0
.c92c0
    inc zp_text_ptr_off                                               ; 92c0: e6 0a       ..    
    jsr check_end_of_statement                                        ; 92c2: 20 57 98     W.   
    lda #0                                                            ; 92c5: a9 00       ..    
    beq loop_c92b2                                                    ; 92c7: f0 e9       ..    
; ***************************************************************************************
; TIME=
;
; Set the centisecond elapsed-time clock. TIME = value.
.stmt_time
    jsr sub_c92eb                                                     ; 92c9: 20 eb 92     ..   
    ldx #<(zp_iwa)                                                    ; 92cc: a2 2a       .*    
    ldy #>(zp_iwa)                                                    ; 92ce: a0 00       ..    
    sty zp_fwa_sign                                                   ; 92d0: 84 2e       ..    
    lda #osword_write_clock                                           ; 92d2: a9 02       ..    
    jsr osword                                                        ; 92d4: 20 f1 ff     ..      ; Write system clock
    jmp statement_loop                                                ; 92d7: 4c 9b 8b    L..   
; &92da referenced 4 times by &9380, &9403, &b459, &b47c
.sub_c92da
    jsr skip_spaces_expect_comma                                      ; 92da: 20 ae 8a     ..   
; &92dd referenced 8 times by &8e40, &90eb, &9702, &ab41, &b047, &b0c2, &b7f5, &b81a
.sub_c92dd
    jsr sub_c9b29                                                     ; 92dd: 20 29 9b     ).   
    jmp coerce_to_integer                                             ; 92e0: 4c f0 92    L..   
; &92e3 referenced 10 times by &8e58, &95aa, &95b2, &9691, &ab33, &abd2, &acd1, &afad, &b3bd, &bfbc
.sub_c92e3
    jsr eval_factor                                                   ; 92e3: 20 ec ad     ..   
    beq c92f7                                                         ; 92e6: f0 0f       ..    
    bmi c92f4                                                         ; 92e8: 30 0a       0.    
; &92ea referenced 2 times by &92f2, &92ff
.return_9
    rts                                                               ; 92ea: 60          `     
; &92eb referenced 4 times by &925d, &926f, &9283, &92c9
.sub_c92eb
    jsr sub_c9807                                                     ; 92eb: 20 07 98     ..   
; &92ee referenced 6 times by &8ed5, &93fd, &b592, &bbb7, &bf37, &bf62
.sub_c92ee
    lda zp_var_type                                                   ; 92ee: a5 27       .'    
; ***************************************************************************************
; Coerce the current value to an integer
;
; Check the type of the last evaluated value (in A from zp_var_type): a string raises
; "Type mismatch", an integer returns unchanged, and a real is converted to a 4-byte
; integer in the integer accumulator.
;
; On Entry:
;     A: value type from zp_var_type (&27)
; &92f0 referenced 21 times by &8824, &8e2e, &92e0, &9688, &974a, &976f, &99bf, &99ce, &9b3e, &9b59, &9b6c, &9b7b, &9b85, &ab4d, &ad0c, &af0f, &afdd, &afff, &b05e, &b921, &b9a2
.coerce_to_integer
    beq c92f7                                                         ; 92f0: f0 05       ..    
    bpl return_9                                                      ; 92f2: 10 f6       ..    
; &92f4 referenced 1 time by &92e8
.c92f4
    jmp fwa_to_int                                                    ; 92f4: 4c e4 a3    L..   
; &92f7 referenced 3 times by &92e6, &92f0, &92fd
.c92f7
    jmp c8c0e                                                         ; 92f7: 4c 0e 8c    L..   
; &92fa referenced 11 times by &9e3c, &a6be, &a7b4, &a7fe, &a8da, &a907, &a98d, &a998, &aa91, &abb1, &abc2
.sub_c92fa
    jsr eval_factor                                                   ; 92fa: 20 ec ad     ..   
; &92fd referenced 7 times by &9a59, &9d29, &9de6, &9df2, &9e36, &b852, &b870
.sub_c92fd
    beq c92f7                                                         ; 92fd: f0 f8       ..    
    bmi return_9                                                      ; 92ff: 30 e9       0.    
    jmp int_to_fwa                                                    ; 9301: 4c be a2    L..   
; ***************************************************************************************
; PROC
;
; Call a named procedure, stacking parameters and the return position.
; PROCname[(params)].
.stmt_proc
    lda zp_text_ptr                                                   ; 9304: a5 0b       ..    
    sta zp_text_ptr2                                                  ; 9306: 85 19       ..    
    lda l000c                                                         ; 9308: a5 0c       ..    
    sta l001a                                                         ; 930a: 85 1a       ..    
    lda zp_text_ptr_off                                               ; 930c: a5 0a       ..    
    sta zp_text_ptr2_off                                              ; 930e: 85 1b       ..    
    lda #&f2                                                          ; 9310: a9 f2       ..    
    jsr sub_cb197                                                     ; 9312: 20 97 b1     ..   
    jsr sub_c9852                                                     ; 9315: 20 52 98     R.   
    jmp statement_loop                                                ; 9318: 4c 9b 8b    L..   
; &931b referenced 1 time by &9332
.loop_c931b
    ldy #3                                                            ; 931b: a0 03       ..    
    lda #0                                                            ; 931d: a9 00       ..    
    sta (zp_iwa),y                                                    ; 931f: 91 2a       .*    
    beq c9341                                                         ; 9321: f0 1e       ..    
; ***************************************************************************************
; LOCAL
;
; Make variables local to the current PROC/FN, stacking their old values. LOCAL var,...
; &9323 referenced 1 time by &934e
.stmt_local
    tsx                                                               ; 9323: ba          .     
    cpx #&fc                                                          ; 9324: e0 fc       ..    
    bcs c936b                                                         ; 9326: b0 43       .C    
    jsr sub_c9582                                                     ; 9328: 20 82 95     ..   
    beq c9353                                                         ; 932b: f0 26       .&    
    jsr sub_cb30d                                                     ; 932d: 20 0d b3     ..   
    ldy zp_iwa_2                                                      ; 9330: a4 2c       .,    
    bmi loop_c931b                                                    ; 9332: 30 e7       0.    
    jsr stack_integer                                                 ; 9334: 20 94 bd     ..   
    lda #0                                                            ; 9337: a9 00       ..    
    jsr caed8                                                         ; 9339: 20 d8 ae     ..   
    sta zp_var_type                                                   ; 933c: 85 27       .'    
    jsr sub_cb4b4                                                     ; 933e: 20 b4 b4     ..   
; &9341 referenced 1 time by &9321
.c9341
    tsx                                                               ; 9341: ba          .     
    inc l0106,x                                                       ; 9342: fe 06 01    ...   
    ldy zp_text_ptr2_off                                              ; 9345: a4 1b       ..    
    sty zp_text_ptr_off                                               ; 9347: 84 0a       ..    
    jsr skip_spaces                                                   ; 9349: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 934c: c9 2c       .,    
    beq stmt_local                                                    ; 934e: f0 d3       ..    
    jmp c8b96                                                         ; 9350: 4c 96 8b    L..   
; &9353 referenced 1 time by &932b
.c9353
    jmp c8b98                                                         ; 9353: 4c 98 8b    L..   
; ***************************************************************************************
; ENDPROC
;
; Return from a procedure, restoring LOCAL values and the caller's text pointer. ENDPROC.
.stmt_endproc
    tsx                                                               ; 9356: ba          .     
    cpx #&fc                                                          ; 9357: e0 fc       ..    
    bcs c9365                                                         ; 9359: b0 0a       ..    
    lda l01ff                                                         ; 935b: ad ff 01    ...   
    cmp #&f2                                                          ; 935e: c9 f2       ..    
    bne c9365                                                         ; 9360: d0 03       ..    
    jmp check_end_of_statement                                        ; 9362: 4c 57 98    LW.   
; &9365 referenced 2 times by &9359, &9360
.c9365
    brk                                                               ; 9365: 00          .     
    equb &0d                                                          ; 9366: 0d          .     
    equs "No "                                                        ; 9367: 4e 6f 20    No    
    equb &f2                                                          ; 936a: f2          .     
; &936b referenced 1 time by &9326
.c936b
    brk                                                               ; 936b: 00          .     
    equb &0c                                                          ; 936c: 0c          .     
    equs "Not "                                                       ; 936d: 4e 6f 74... Not...
    equb &ea                                                          ; 9371: ea          .     
; &9372 referenced 4 times by &93b2, &93b8, &93c6, &93cd
.c9372
    brk                                                               ; 9372: 00          .     
    equb &19                                                          ; 9373: 19          .     
    equs "Bad "                                                       ; 9374: 42 61 64... Bad...
    equb &eb, &00                                                     ; 9378: eb 00       ..    
; ***************************************************************************************
; GCOL
;
; Set the graphics colour and plotting action. GCOL action, colour.
.stmt_gcol
    jsr eval_expr_to_integer                                          ; 937a: 20 21 88     !.   
    lda zp_iwa                                                        ; 937d: a5 2a       .*    
    pha                                                               ; 937f: 48          H     
    jsr sub_c92da                                                     ; 9380: 20 da 92     ..   
    jsr sub_c9852                                                     ; 9383: 20 52 98     R.   
    lda #&12                                                          ; 9386: a9 12       ..    
    jsr oswrch                                                        ; 9388: 20 ee ff     ..   
    jmp c93da                                                         ; 938b: 4c da 93    L..   
; ***************************************************************************************
; COLOUR
;
; Select the text colour or redefine a logical colour. COLOUR n.
.stmt_colour
    lda #&11                                                          ; 938e: a9 11       ..    
    pha                                                               ; 9390: 48          H     
    jsr eval_expr_to_integer                                          ; 9391: 20 21 88     !.   
    jsr check_end_of_statement                                        ; 9394: 20 57 98     W.   
    jmp c93da                                                         ; 9397: 4c da 93    L..   
; ***************************************************************************************
; MODE
;
; Select a screen mode, resetting the display. MODE n.
.stmt_mode
    lda #&16                                                          ; 939a: a9 16       ..    
    pha                                                               ; 939c: 48          H     
    jsr eval_expr_to_integer                                          ; 939d: 20 21 88     !.   
    jsr check_end_of_statement                                        ; 93a0: 20 57 98     W.   
    jsr sub_cbee7                                                     ; 93a3: 20 e7 be     ..   
    cpx #&ff                                                          ; 93a6: e0 ff       ..    
    bne c93d7                                                         ; 93a8: d0 2d       .-    
    cpy #&ff                                                          ; 93aa: c0 ff       ..    
    bne c93d7                                                         ; 93ac: d0 29       .)    
    lda zp_stack_ptr                                                  ; 93ae: a5 04       ..    
    cmp zp_himem                                                      ; 93b0: c5 06       ..    
    bne c9372                                                         ; 93b2: d0 be       ..    
    lda zp_stack_ptr_1                                                ; 93b4: a5 05       ..    
    cmp l0007                                                         ; 93b6: c5 07       ..    
    bne c9372                                                         ; 93b8: d0 b8       ..    
    ldx zp_iwa                                                        ; 93ba: a6 2a       .*    
    lda #osbyte_read_himem_for_mode                                   ; 93bc: a9 85       ..    
    jsr osbyte                                                        ; 93be: 20 f4 ff     ..      ; Read top of user RAM for given screen mode
    cpx zp_vartop                                                     ; 93c1: e4 02       ..    
    tya                                                               ; 93c3: 98          .     
    sbc zp_vartop_1                                                   ; 93c4: e5 03       ..    
    bcc c9372                                                         ; 93c6: 90 aa       ..    
    cpx zp_top                                                        ; 93c8: e4 12       ..    
    tya                                                               ; 93ca: 98          .     
    sbc l0013                                                         ; 93cb: e5 13       ..    
    bcc c9372                                                         ; 93cd: 90 a3       ..    
    stx zp_himem                                                      ; 93cf: 86 06       ..    
    stx zp_stack_ptr                                                  ; 93d1: 86 04       ..    
    sty l0007                                                         ; 93d3: 84 07       ..    
    sty zp_stack_ptr_1                                                ; 93d5: 84 05       ..    
; &93d7 referenced 2 times by &93a8, &93ac
.c93d7
    jsr cbc28                                                         ; 93d7: 20 28 bc     (.   
; &93da referenced 2 times by &938b, &9397
.c93da
    pla                                                               ; 93da: 68          h     
    jsr oswrch                                                        ; 93db: 20 ee ff     ..   
    jsr sub_c9456                                                     ; 93de: 20 56 94     V.   
    jmp statement_loop                                                ; 93e1: 4c 9b 8b    L..   
; ***************************************************************************************
; MOVE
;
; Move the graphics cursor without drawing (PLOT 4). MOVE x, y.
.stmt_move
    lda #4                                                            ; 93e4: a9 04       ..    
    bne c93ea                                                         ; 93e6: d0 02       ..    
; ***************************************************************************************
; DRAW
;
; Draw a line from the graphics cursor to a point (PLOT 5). DRAW x, y.
.stmt_draw
    lda #5                                                            ; 93e8: a9 05       ..    
; &93ea referenced 1 time by &93e6
.c93ea
    pha                                                               ; 93ea: 48          H     
    jsr eval_expr                                                     ; 93eb: 20 1d 9b     ..   
    jmp c93fd                                                         ; 93ee: 4c fd 93    L..   
; ***************************************************************************************
; PLOT
;
; Plot a point, line or shape with a given mode. PLOT mode, x, y.
.stmt_plot
    jsr eval_expr_to_integer                                          ; 93f1: 20 21 88     !.   
    lda zp_iwa                                                        ; 93f4: a5 2a       .*    
    pha                                                               ; 93f6: 48          H     
    jsr skip_spaces_expect_comma                                      ; 93f7: 20 ae 8a     ..   
    jsr sub_c9b29                                                     ; 93fa: 20 29 9b     ).   
; &93fd referenced 1 time by &93ee
.c93fd
    jsr sub_c92ee                                                     ; 93fd: 20 ee 92     ..   
    jsr stack_integer                                                 ; 9400: 20 94 bd     ..   
    jsr sub_c92da                                                     ; 9403: 20 da 92     ..   
    jsr sub_c9852                                                     ; 9406: 20 52 98     R.   
    lda #&19                                                          ; 9409: a9 19       ..    
    jsr oswrch                                                        ; 940b: 20 ee ff     ..   
    pla                                                               ; 940e: 68          h     
    jsr oswrch                                                        ; 940f: 20 ee ff     ..   
    jsr sub_cbe0b                                                     ; 9412: 20 0b be     ..   
    lda zp_general                                                    ; 9415: a5 37       .7    
    jsr oswrch                                                        ; 9417: 20 ee ff     ..   
    lda l0038                                                         ; 941a: a5 38       .8    
    jsr oswrch                                                        ; 941c: 20 ee ff     ..   
    jsr sub_c9456                                                     ; 941f: 20 56 94     V.   
    lda zp_iwa_1                                                      ; 9422: a5 2b       .+    
    jsr oswrch                                                        ; 9424: 20 ee ff     ..   
    jmp statement_loop                                                ; 9427: 4c 9b 8b    L..   
; &942a referenced 1 time by &9451
.loop_c942a
    lda zp_iwa_1                                                      ; 942a: a5 2b       .+    
    jsr oswrch                                                        ; 942c: 20 ee ff     ..   
; ***************************************************************************************
; VDU
;
; Send bytes to the VDU drivers; ";" sends a 16-bit word. VDU n[,|;]...
; &942f referenced 1 time by &944b
.stmt_vdu
    jsr skip_spaces                                                   ; 942f: 20 97 8a     ..   
; &9432 referenced 1 time by &944f
.loop_c9432
    cmp #&3a ; ':'                                                    ; 9432: c9 3a       .:    
    beq c9453                                                         ; 9434: f0 1d       ..    
    cmp #&0d                                                          ; 9436: c9 0d       ..    
    beq c9453                                                         ; 9438: f0 19       ..    
    cmp #&8b                                                          ; 943a: c9 8b       ..    
    beq c9453                                                         ; 943c: f0 15       ..    
    dec zp_text_ptr_off                                               ; 943e: c6 0a       ..    
    jsr eval_expr_to_integer                                          ; 9440: 20 21 88     !.   
    jsr sub_c9456                                                     ; 9443: 20 56 94     V.   
    jsr skip_spaces                                                   ; 9446: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; 9449: c9 2c       .,    
    beq stmt_vdu                                                      ; 944b: f0 e2       ..    
    cmp #&3b ; ';'                                                    ; 944d: c9 3b       .;    
    bne loop_c9432                                                    ; 944f: d0 e1       ..    
    beq loop_c942a                                                    ; 9451: f0 d7       ..    
; &9453 referenced 3 times by &9434, &9438, &943c
.c9453
    jmp c8b96                                                         ; 9453: 4c 96 8b    L..   
; &9456 referenced 4 times by &8e3a, &93de, &941f, &9443
.sub_c9456
    lda zp_iwa                                                        ; 9456: a5 2a       .*    
    jmp (wrchv)                                                       ; 9458: 6c 0e 02    l..   
; ***************************************************************************************
; Find a PROC or FN definition by name
;
; Search the PROC (token &F2) or FN linked list for a definition whose name starts at
; (zp_general)+1. Shares the chain walk with find_variable; returns a pointer to the
; body, or "not found".
; &945b referenced 1 time by &b1e1
.find_proc_fn
    ldy #1                                                            ; 945b: a0 01       ..    
    lda (zp_general),y                                                ; 945d: b1 37       .7    
    ldy #&f6                                                          ; 945f: a0 f6       ..       ; Index the PROC / FN entries of the variable table
    cmp #&f2                                                          ; 9461: c9 f2       ..    
    beq c946f                                                         ; 9463: f0 0a       ..    
    ldy #&f8                                                          ; 9465: a0 f8       ..    
    bne c946f                                                         ; 9467: d0 06       ..    
; ***************************************************************************************
; Find a variable by name
;
; Search the heap for a variable whose name starts at (zp_general)+1. The initial
; character selects one of the per-letter linked lists via the variable table; the chain
; is walked comparing the rest of the name. On a match, returns a pointer to the value in
; zp_iwa/zp_iwa_1; otherwise reports it is not present.
; &9469 referenced 4 times by &916f, &965a, &96bc, &96df
.find_variable
    ldy #1                                                            ; 9469: a0 01       ..    
    lda (zp_general),y                                                ; 946b: b1 37       .7    
    asl a                                                             ; 946d: 0a          .        ; Two bytes per entry: double the initial letter
    tay                                                               ; 946e: a8          .     
; &946f referenced 2 times by &9463, &9467
.c946f
    lda resint_at,y                                                   ; 946f: b9 00 04    ...      ; Head of the chain from the variable table (&0400+2*ch)
    sta l003a                                                         ; 9472: 85 3a       .:    
    lda l0401,y                                                       ; 9474: b9 01 04    ...   
    sta zp_fwb_sign                                                   ; 9477: 85 3b       .;    
; &9479 referenced 4 times by &94ca, &94d2, &94d6, &94df
.c9479
    lda zp_fwb_sign                                                   ; 9479: a5 3b       .;       ; End of the chain: variable not found
    beq return_10                                                     ; 947b: f0 35       .5    
    ldy #0                                                            ; 947d: a0 00       ..    
    lda (l003a),y                                                     ; 947f: b1 3a       .:    
    sta zp_fwb_ovf                                                    ; 9481: 85 3c       .<    
    iny                                                               ; 9483: c8          .     
    lda (l003a),y                                                     ; 9484: b1 3a       .:    
    sta zp_fwb_exp                                                    ; 9486: 85 3d       .=    
    iny                                                               ; 9488: c8          .     
    lda (l003a),y                                                     ; 9489: b1 3a       .:    
    bne c949a                                                         ; 948b: d0 0d       ..    
    dey                                                               ; 948d: 88          .     
    cpy zp_fileblk                                                    ; 948e: c4 39       .9    
    bne c94b3                                                         ; 9490: d0 21       .!    
    iny                                                               ; 9492: c8          .     
    bcs c94a7                                                         ; 9493: b0 12       ..    
; &9495 referenced 1 time by &94a0
.loop_c9495
    iny                                                               ; 9495: c8          .        ; Compare the rest of the name against this entry
    lda (l003a),y                                                     ; 9496: b1 3a       .:    
    beq c94b3                                                         ; 9498: f0 19       ..    
; &949a referenced 1 time by &948b
.c949a
    cmp (zp_general),y                                                ; 949a: d1 37       .7    
    bne c94b3                                                         ; 949c: d0 15       ..    
    cpy zp_fileblk                                                    ; 949e: c4 39       .9    
    bne loop_c9495                                                    ; 94a0: d0 f3       ..    
    iny                                                               ; 94a2: c8          .     
    lda (l003a),y                                                     ; 94a3: b1 3a       .:    
    bne c94b3                                                         ; 94a5: d0 0c       ..    
; &94a7 referenced 1 time by &9493
.c94a7
    tya                                                               ; 94a7: 98          .        ; Match: return a pointer to the value
    adc l003a                                                         ; 94a8: 65 3a       e:    
    sta zp_iwa                                                        ; 94aa: 85 2a       .*    
    lda zp_fwb_sign                                                   ; 94ac: a5 3b       .;    
    adc #0                                                            ; 94ae: 69 00       i.    
    sta zp_iwa_1                                                      ; 94b0: 85 2b       .+    
; &94b2 referenced 2 times by &947b, &94b5
.return_10
    rts                                                               ; 94b2: 60          `     
; &94b3 referenced 4 times by &9490, &9498, &949c, &94a5
.c94b3
    lda zp_fwb_exp                                                    ; 94b3: a5 3d       .=       ; No match: follow the link to the next entry
    beq return_10                                                     ; 94b5: f0 fb       ..    
    ldy #0                                                            ; 94b7: a0 00       ..    
    lda (zp_fwb_ovf),y                                                ; 94b9: b1 3c       .<    
    sta l003a                                                         ; 94bb: 85 3a       .:    
    iny                                                               ; 94bd: c8          .     
    lda (zp_fwb_ovf),y                                                ; 94be: b1 3c       .<    
    sta zp_fwb_sign                                                   ; 94c0: 85 3b       .;    
    iny                                                               ; 94c2: c8          .     
    lda (zp_fwb_ovf),y                                                ; 94c3: b1 3c       .<    
    bne c94d4                                                         ; 94c5: d0 0d       ..    
    dey                                                               ; 94c7: 88          .     
    cpy zp_fileblk                                                    ; 94c8: c4 39       .9    
    bne c9479                                                         ; 94ca: d0 ad       ..    
    iny                                                               ; 94cc: c8          .     
    bcs c94e1                                                         ; 94cd: b0 12       ..    
; &94cf referenced 1 time by &94da
.loop_c94cf
    iny                                                               ; 94cf: c8          .     
    lda (zp_fwb_ovf),y                                                ; 94d0: b1 3c       .<    
    beq c9479                                                         ; 94d2: f0 a5       ..    
; &94d4 referenced 1 time by &94c5
.c94d4
    cmp (zp_general),y                                                ; 94d4: d1 37       .7    
    bne c9479                                                         ; 94d6: d0 a1       ..    
    cpy zp_fileblk                                                    ; 94d8: c4 39       .9    
    bne loop_c94cf                                                    ; 94da: d0 f3       ..    
    iny                                                               ; 94dc: c8          .     
    lda (zp_fwb_ovf),y                                                ; 94dd: b1 3c       .<    
    bne c9479                                                         ; 94df: d0 98       ..    
; &94e1 referenced 1 time by &94cd
.c94e1
    tya                                                               ; 94e1: 98          .     
    adc zp_fwb_ovf                                                    ; 94e2: 65 3c       e<    
    sta zp_iwa                                                        ; 94e4: 85 2a       .*    
    lda zp_fwb_exp                                                    ; 94e6: a5 3d       .=    
    adc #0                                                            ; 94e8: 69 00       i.    
    sta zp_iwa_1                                                      ; 94ea: 85 2b       .+    
    rts                                                               ; 94ec: 60          `     
; &94ed referenced 1 time by &b171
.sub_c94ed
    ldy #1                                                            ; 94ed: a0 01       ..    
    lda (zp_general),y                                                ; 94ef: b1 37       .7    
    tax                                                               ; 94f1: aa          .     
    lda #&f6                                                          ; 94f2: a9 f6       ..    
    cpx #&f2                                                          ; 94f4: e0 f2       ..    
    beq c9501                                                         ; 94f6: f0 09       ..    
    lda #&f8                                                          ; 94f8: a9 f8       ..    
    bne c9501                                                         ; 94fa: d0 05       ..    
; &94fc referenced 3 times by &8bd5, &9174, &9589
.sub_c94fc
    ldy #1                                                            ; 94fc: a0 01       ..    
    lda (zp_general),y                                                ; 94fe: b1 37       .7    
    asl a                                                             ; 9500: 0a          .     
; &9501 referenced 2 times by &94f6, &94fa
.c9501
    sta l003a                                                         ; 9501: 85 3a       .:    
    lda #4                                                            ; 9503: a9 04       ..    
    sta zp_fwb_sign                                                   ; 9505: 85 3b       .;    
; &9507 referenced 1 time by &9514
.loop_c9507
    lda (l003a),y                                                     ; 9507: b1 3a       .:    
    beq c9516                                                         ; 9509: f0 0b       ..    
    tax                                                               ; 950b: aa          .     
    dey                                                               ; 950c: 88          .     
    lda (l003a),y                                                     ; 950d: b1 3a       .:    
    sta l003a                                                         ; 950f: 85 3a       .:    
    stx zp_fwb_sign                                                   ; 9511: 86 3b       .;    
    iny                                                               ; 9513: c8          .     
    bpl loop_c9507                                                    ; 9514: 10 f1       ..    
; &9516 referenced 1 time by &9509
.c9516
    lda zp_vartop_1                                                   ; 9516: a5 03       ..    
    sta (l003a),y                                                     ; 9518: 91 3a       .:    
    lda zp_vartop                                                     ; 951a: a5 02       ..    
    dey                                                               ; 951c: 88          .     
    sta (l003a),y                                                     ; 951d: 91 3a       .:    
    tya                                                               ; 951f: 98          .     
    iny                                                               ; 9520: c8          .     
    sta (zp_vartop),y                                                 ; 9521: 91 02       ..    
    cpy zp_fileblk                                                    ; 9523: c4 39       .9    
    beq return_11                                                     ; 9525: f0 31       .1    
; &9527 referenced 1 time by &952e
.loop_c9527
    iny                                                               ; 9527: c8          .     
    lda (zp_general),y                                                ; 9528: b1 37       .7    
    sta (zp_vartop),y                                                 ; 952a: 91 02       ..    
    cpy zp_fileblk                                                    ; 952c: c4 39       .9    
    bne loop_c9527                                                    ; 952e: d0 f7       ..    
    rts                                                               ; 9530: 60          `     
; &9531 referenced 4 times by &8bdf, &9179, &957f, &b176
.sub_c9531
    lda #0                                                            ; 9531: a9 00       ..    
; &9533 referenced 1 time by &9537
.loop_c9533
    iny                                                               ; 9533: c8          .     
    sta (zp_vartop),y                                                 ; 9534: 91 02       ..    
    dex                                                               ; 9536: ca          .     
    bne loop_c9533                                                    ; 9537: d0 fa       ..    
; &9539 referenced 1 time by &b184
.sub_c9539
    sec                                                               ; 9539: 38          8     
    tya                                                               ; 953a: 98          .     
    adc zp_vartop                                                     ; 953b: 65 02       e.    
    bcc c9541                                                         ; 953d: 90 02       ..    
    inc zp_vartop_1                                                   ; 953f: e6 03       ..    
; &9541 referenced 1 time by &953d
.c9541
    ldy zp_vartop_1                                                   ; 9541: a4 03       ..    
    cpy zp_stack_ptr_1                                                ; 9543: c4 05       ..    
    bcc c9556                                                         ; 9545: 90 0f       ..    
    bne c954d                                                         ; 9547: d0 04       ..    
    cmp zp_stack_ptr                                                  ; 9549: c5 04       ..    
    bcc c9556                                                         ; 954b: 90 09       ..    
; &954d referenced 1 time by &9547
.c954d
    lda #0                                                            ; 954d: a9 00       ..    
    ldy #1                                                            ; 954f: a0 01       ..    
    sta (l003a),y                                                     ; 9551: 91 3a       .:    
    jmp err_no_room                                                   ; 9553: 4c b7 8c    L..   
; &9556 referenced 2 times by &9545, &954b
.c9556
    sta zp_vartop                                                     ; 9556: 85 02       ..    
; &9558 referenced 1 time by &9525
.return_11
    rts                                                               ; 9558: 60          `     
; &9559 referenced 1 time by &914b
.sub_c9559
    ldy #1                                                            ; 9559: a0 01       ..    
; &955b referenced 2 times by &956f, &b1d5
.c955b
    lda (zp_general),y                                                ; 955b: b1 37       .7    
    cmp #&30 ; '0'                                                    ; 955d: c9 30       .0    
    bcc return_12                                                     ; 955f: 90 18       ..    
    cmp #&40 ; '@'                                                    ; 9561: c9 40       .@    
    bcs c9571                                                         ; 9563: b0 0c       ..    
    cmp #&3a ; ':'                                                    ; 9565: c9 3a       .:    
    bcs return_12                                                     ; 9567: b0 10       ..    
    cpy #1                                                            ; 9569: c0 01       ..    
    beq return_12                                                     ; 956b: f0 0c       ..    
; &956d referenced 2 times by &9577, &957c
.c956d
    inx                                                               ; 956d: e8          .     
    iny                                                               ; 956e: c8          .     
    bne c955b                                                         ; 956f: d0 ea       ..    
; &9571 referenced 1 time by &9563
.c9571
    cmp #&5f ; '_'                                                    ; 9571: c9 5f       ._    
    bcs c957a                                                         ; 9573: b0 05       ..    
    cmp #&5b ; '['                                                    ; 9575: c9 5b       .[    
    bcc c956d                                                         ; 9577: 90 f4       ..    
; &9579 referenced 3 times by &955f, &9567, &956b
.return_12
    rts                                                               ; 9579: 60          `     
; &957a referenced 1 time by &9573
.c957a
    cmp #&7b ; '{'                                                    ; 957a: c9 7b       .{    
    bcc c956d                                                         ; 957c: 90 ef       ..    
    rts                                                               ; 957e: 60          `     
; &957f referenced 2 times by &9590, &9593
.c957f
    jsr sub_c9531                                                     ; 957f: 20 31 95     1.   
; &9582 referenced 9 times by &85a5, &8be4, &90e1, &9328, &b256, &b7c4, &b9e4, &ba7f, &bb1f
.sub_c9582
    jsr sub_c95c9                                                     ; 9582: 20 c9 95     ..   
    bne return_13                                                     ; 9585: d0 1d       ..    
    bcs return_13                                                     ; 9587: b0 1b       ..    
    jsr sub_c94fc                                                     ; 9589: 20 fc 94     ..   
    ldx #5                                                            ; 958c: a2 05       ..    
    cpx zp_iwa_2                                                      ; 958e: e4 2c       .,    
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
.return_13
    rts                                                               ; 95a4: 60          `     
; &95a5 referenced 1 time by &9597
.c95a5
    lda #4                                                            ; 95a5: a9 04       ..    
; &95a7 referenced 1 time by &959f
.c95a7
    pha                                                               ; 95a7: 48          H     
    inc zp_text_ptr2_off                                              ; 95a8: e6 1b       ..    
    jsr sub_c92e3                                                     ; 95aa: 20 e3 92     ..   
    jmp c969f                                                         ; 95ad: 4c 9f 96    L..   
; &95b0 referenced 1 time by &959b
.c95b0
    inc zp_text_ptr2_off                                              ; 95b0: e6 1b       ..    
    jsr sub_c92e3                                                     ; 95b2: 20 e3 92     ..   
    lda zp_iwa_1                                                      ; 95b5: a5 2b       .+    
    beq c95bf                                                         ; 95b7: f0 06       ..    
    lda #&80                                                          ; 95b9: a9 80       ..    
    sta zp_iwa_2                                                      ; 95bb: 85 2c       .,    
    sec                                                               ; 95bd: 38          8     
    rts                                                               ; 95be: 60          `     
; &95bf referenced 1 time by &95b7
.c95bf
    brk                                                               ; 95bf: 00          .     
    equb &08                                                          ; 95c0: 08          .     
    equs "$ range"                                                    ; 95c1: 24 20 72... $ r...
    equb &00                                                          ; 95c8: 00          .     
; &95c9 referenced 2 times by &9582, &b695
.sub_c95c9
    lda zp_text_ptr                                                   ; 95c9: a5 0b       ..    
    sta zp_text_ptr2                                                  ; 95cb: 85 19       ..    
    lda l000c                                                         ; 95cd: a5 0c       ..    
    sta l001a                                                         ; 95cf: 85 1a       ..    
    ldy zp_text_ptr_off                                               ; 95d1: a4 0a       ..    
    dey                                                               ; 95d3: 88          .     
; &95d4 referenced 1 time by &95db
.loop_c95d4
    iny                                                               ; 95d4: c8          .     
; &95d5 referenced 1 time by &8eec
.sub_c95d5
    sty zp_text_ptr2_off                                              ; 95d5: 84 1b       ..    
    lda (zp_text_ptr2),y                                              ; 95d7: b1 19       ..    
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
    sta zp_iwa                                                        ; 95e7: 85 2a       .*    
    lda #4                                                            ; 95e9: a9 04       ..    
    sta zp_iwa_1                                                      ; 95eb: 85 2b       .+    
    iny                                                               ; 95ed: c8          .     
    lda (zp_text_ptr2),y                                              ; 95ee: b1 19       ..    
    iny                                                               ; 95f0: c8          .     
    cmp #&25 ; '%'                                                    ; 95f1: c9 25       .%    
    bne c95ff                                                         ; 95f3: d0 0a       ..    
    ldx #4                                                            ; 95f5: a2 04       ..    
    stx zp_iwa_2                                                      ; 95f7: 86 2c       .,    
    lda (zp_text_ptr2),y                                              ; 95f9: b1 19       ..    
    cmp #&28 ; '('                                                    ; 95fb: c9 28       .(    
    bne c9665                                                         ; 95fd: d0 66       .f    
; &95ff referenced 2 times by &95e3, &95f3
.c95ff
    ldx #5                                                            ; 95ff: a2 05       ..    
    stx zp_iwa_2                                                      ; 9601: 86 2c       .,    
    lda zp_text_ptr2_off                                              ; 9603: a5 1b       ..    
    clc                                                               ; 9605: 18          .     
    adc zp_text_ptr2                                                  ; 9606: 65 19       e.    
    ldx l001a                                                         ; 9608: a6 1a       ..    
    bcc c960e                                                         ; 960a: 90 02       ..    
    inx                                                               ; 960c: e8          .     
    clc                                                               ; 960d: 18          .     
; &960e referenced 1 time by &960a
.c960e
    sbc #0                                                            ; 960e: e9 00       ..    
    sta zp_general                                                    ; 9610: 85 37       .7    
    bcs c9615                                                         ; 9612: b0 01       ..    
    dex                                                               ; 9614: ca          .     
; &9615 referenced 1 time by &9612
.c9615
    stx l0038                                                         ; 9615: 86 38       .8    
    ldx zp_text_ptr2_off                                              ; 9617: a6 1b       ..    
    ldy #1                                                            ; 9619: a0 01       ..    
; &961b referenced 3 times by &962b, &9633, &963f
.c961b
    lda (zp_general),y                                                ; 961b: b1 37       .7    
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
    dec zp_iwa_2                                                      ; 964c: c6 2c       .,    
    iny                                                               ; 964e: c8          .     
    inx                                                               ; 964f: e8          .     
    iny                                                               ; 9650: c8          .     
    lda (zp_general),y                                                ; 9651: b1 37       .7    
    dey                                                               ; 9653: 88          .     
; &9654 referenced 1 time by &964a
.c9654
    sty zp_fileblk                                                    ; 9654: 84 39       .9    
    cmp #&28 ; '('                                                    ; 9656: c9 28       .(    
    beq c96a6                                                         ; 9658: f0 4c       .L    
    jsr find_variable                                                 ; 965a: 20 69 94     i.   
    beq c9677                                                         ; 965d: f0 18       ..    
    stx zp_text_ptr2_off                                              ; 965f: 86 1b       ..    
; &9661 referenced 1 time by &96ac
.c9661
    ldy zp_text_ptr2_off                                              ; 9661: a4 1b       ..    
    lda (zp_text_ptr2),y                                              ; 9663: b1 19       ..    
; &9665 referenced 1 time by &95fd
.c9665
    cmp #&21 ; '!'                                                    ; 9665: c9 21       .!    
    beq c967f                                                         ; 9667: f0 16       ..    
    cmp #&3f ; '?'                                                    ; 9669: c9 3f       .?    
    beq c967b                                                         ; 966b: f0 0e       ..    
    clc                                                               ; 966d: 18          .     
    sty zp_text_ptr2_off                                              ; 966e: 84 1b       ..    
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
    sty zp_text_ptr2_off                                              ; 9683: 84 1b       ..    
    jsr cb32c                                                         ; 9685: 20 2c b3     ,.   
    jsr coerce_to_integer                                             ; 9688: 20 f0 92     ..   
    lda zp_iwa_1                                                      ; 968b: a5 2b       .+    
    pha                                                               ; 968d: 48          H     
    lda zp_iwa                                                        ; 968e: a5 2a       .*    
    pha                                                               ; 9690: 48          H     
    jsr sub_c92e3                                                     ; 9691: 20 e3 92     ..   
    clc                                                               ; 9694: 18          .     
    pla                                                               ; 9695: 68          h     
    adc zp_iwa                                                        ; 9696: 65 2a       e*    
    sta zp_iwa                                                        ; 9698: 85 2a       .*    
    pla                                                               ; 969a: 68          h     
    adc zp_iwa_1                                                      ; 969b: 65 2b       e+    
    sta zp_iwa_1                                                      ; 969d: 85 2b       .+    
; &969f referenced 1 time by &95ad
.c969f
    pla                                                               ; 969f: 68          h     
    sta zp_iwa_2                                                      ; 96a0: 85 2c       .,    
    clc                                                               ; 96a2: 18          .     
    lda #&ff                                                          ; 96a3: a9 ff       ..    
    rts                                                               ; 96a5: 60          `     
; &96a6 referenced 1 time by &9658
.c96a6
    inx                                                               ; 96a6: e8          .     
    inc zp_fileblk                                                    ; 96a7: e6 39       .9    
    jsr sub_c96df                                                     ; 96a9: 20 df 96     ..   
    jmp c9661                                                         ; 96ac: 4c 61 96    La.   
; &96af referenced 1 time by &9646
.c96af
    inx                                                               ; 96af: e8          .     
    iny                                                               ; 96b0: c8          .     
    sty zp_fileblk                                                    ; 96b1: 84 39       .9    
    iny                                                               ; 96b3: c8          .     
    dec zp_iwa_2                                                      ; 96b4: c6 2c       .,    
    lda (zp_general),y                                                ; 96b6: b1 37       .7    
    cmp #&28 ; '('                                                    ; 96b8: c9 28       .(    
    beq c96c9                                                         ; 96ba: f0 0d       ..    
    jsr find_variable                                                 ; 96bc: 20 69 94     i.   
    beq c9677                                                         ; 96bf: f0 b6       ..    
    stx zp_text_ptr2_off                                              ; 96c1: 86 1b       ..    
    lda #&81                                                          ; 96c3: a9 81       ..    
    sta zp_iwa_2                                                      ; 96c5: 85 2c       .,    
    sec                                                               ; 96c7: 38          8     
    rts                                                               ; 96c8: 60          `     
; &96c9 referenced 1 time by &96ba
.c96c9
    inx                                                               ; 96c9: e8          .     
    sty zp_fileblk                                                    ; 96ca: 84 39       .9    
    dec zp_iwa_2                                                      ; 96cc: c6 2c       .,    
    jsr sub_c96df                                                     ; 96ce: 20 df 96     ..   
    lda #&81                                                          ; 96d1: a9 81       ..    
    sta zp_iwa_2                                                      ; 96d3: 85 2c       .,    
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
    jsr find_variable                                                 ; 96df: 20 69 94     i.   
    beq c96d7                                                         ; 96e2: f0 f3       ..    
    stx zp_text_ptr2_off                                              ; 96e4: 86 1b       ..    
    lda zp_iwa_2                                                      ; 96e6: a5 2c       .,    
    pha                                                               ; 96e8: 48          H     
    lda zp_iwa                                                        ; 96e9: a5 2a       .*    
    pha                                                               ; 96eb: 48          H     
    lda zp_iwa_1                                                      ; 96ec: a5 2b       .+    
    pha                                                               ; 96ee: 48          H     
    ldy #0                                                            ; 96ef: a0 00       ..    
    lda (zp_iwa),y                                                    ; 96f1: b1 2a       .*    
    cmp #4                                                            ; 96f3: c9 04       ..    
    bcc c976c                                                         ; 96f5: 90 75       .u    
    tya                                                               ; 96f7: 98          .     
    jsr caed8                                                         ; 96f8: 20 d8 ae     ..   
    lda #1                                                            ; 96fb: a9 01       ..    
    sta zp_iwa_3                                                      ; 96fd: 85 2d       .-    
; &96ff referenced 1 time by &9742
.loop_c96ff
    jsr stack_integer                                                 ; 96ff: 20 94 bd     ..   
    jsr sub_c92dd                                                     ; 9702: 20 dd 92     ..   
    inc zp_text_ptr2_off                                              ; 9705: e6 1b       ..    
    cpx #&2c ; ','                                                    ; 9707: e0 2c       .,    
    bne c96d7                                                         ; 9709: d0 cc       ..    
    ldx #&39 ; '9'                                                    ; 970b: a2 39       .9    
    jsr sub_cbe0d                                                     ; 970d: 20 0d be     ..   
    ldy zp_fwb_ovf                                                    ; 9710: a4 3c       .<    
    pla                                                               ; 9712: 68          h     
    sta l0038                                                         ; 9713: 85 38       .8    
    pla                                                               ; 9715: 68          h     
    sta zp_general                                                    ; 9716: 85 37       .7    
    pha                                                               ; 9718: 48          H     
    lda l0038                                                         ; 9719: a5 38       .8    
    pha                                                               ; 971b: 48          H     
    jsr sub_c97ba                                                     ; 971c: 20 ba 97     ..   
    sty zp_iwa_3                                                      ; 971f: 84 2d       .-    
    lda (zp_general),y                                                ; 9721: b1 37       .7    
    sta zp_fwb_m2                                                     ; 9723: 85 3f       .?    
    iny                                                               ; 9725: c8          .     
    lda (zp_general),y                                                ; 9726: b1 37       .7    
    sta zp_fwb_m3                                                     ; 9728: 85 40       .@    
    lda zp_iwa                                                        ; 972a: a5 2a       .*    
    adc zp_fileblk                                                    ; 972c: 65 39       e9    
    sta zp_iwa                                                        ; 972e: 85 2a       .*    
    lda zp_iwa_1                                                      ; 9730: a5 2b       .+    
    adc l003a                                                         ; 9732: 65 3a       e:    
    sta zp_iwa_1                                                      ; 9734: 85 2b       .+    
    jsr sub_c9236                                                     ; 9736: 20 36 92     6.   
    ldy #0                                                            ; 9739: a0 00       ..    
    sec                                                               ; 973b: 38          8     
    lda (zp_general),y                                                ; 973c: b1 37       .7    
    sbc zp_iwa_3                                                      ; 973e: e5 2d       .-    
    cmp #3                                                            ; 9740: c9 03       ..    
    bcs loop_c96ff                                                    ; 9742: b0 bb       ..    
    jsr stack_integer                                                 ; 9744: 20 94 bd     ..   
    jsr cae56                                                         ; 9747: 20 56 ae     V.   
    jsr coerce_to_integer                                             ; 974a: 20 f0 92     ..   
    pla                                                               ; 974d: 68          h     
    sta l0038                                                         ; 974e: 85 38       .8    
    pla                                                               ; 9750: 68          h     
    sta zp_general                                                    ; 9751: 85 37       .7    
    ldx #&39 ; '9'                                                    ; 9753: a2 39       .9    
    jsr sub_cbe0d                                                     ; 9755: 20 0d be     ..   
    ldy zp_fwb_ovf                                                    ; 9758: a4 3c       .<    
    jsr sub_c97ba                                                     ; 975a: 20 ba 97     ..   
    clc                                                               ; 975d: 18          .     
    lda zp_fileblk                                                    ; 975e: a5 39       .9    
    adc zp_iwa                                                        ; 9760: 65 2a       e*    
    sta zp_iwa                                                        ; 9762: 85 2a       .*    
    lda l003a                                                         ; 9764: a5 3a       .:    
    adc zp_iwa_1                                                      ; 9766: 65 2b       e+    
    sta zp_iwa_1                                                      ; 9768: 85 2b       .+    
    bcc c977d                                                         ; 976a: 90 11       ..    
; &976c referenced 1 time by &96f5
.c976c
    jsr cae56                                                         ; 976c: 20 56 ae     V.   
    jsr coerce_to_integer                                             ; 976f: 20 f0 92     ..   
    pla                                                               ; 9772: 68          h     
    sta l0038                                                         ; 9773: 85 38       .8    
    pla                                                               ; 9775: 68          h     
    sta zp_general                                                    ; 9776: 85 37       .7    
    ldy #1                                                            ; 9778: a0 01       ..    
    jsr sub_c97ba                                                     ; 977a: 20 ba 97     ..   
; &977d referenced 1 time by &976a
.c977d
    pla                                                               ; 977d: 68          h     
    sta zp_iwa_2                                                      ; 977e: 85 2c       .,    
    cmp #5                                                            ; 9780: c9 05       ..    
    bne c979b                                                         ; 9782: d0 17       ..    
    ldx zp_iwa_1                                                      ; 9784: a6 2b       .+    
    lda zp_iwa                                                        ; 9786: a5 2a       .*    
    asl zp_iwa                                                        ; 9788: 06 2a       .*    
    rol zp_iwa_1                                                      ; 978a: 26 2b       &+    
    asl zp_iwa                                                        ; 978c: 06 2a       .*    
    rol zp_iwa_1                                                      ; 978e: 26 2b       &+    
    adc zp_iwa                                                        ; 9790: 65 2a       e*    
    sta zp_iwa                                                        ; 9792: 85 2a       .*    
    txa                                                               ; 9794: 8a          .     
    adc zp_iwa_1                                                      ; 9795: 65 2b       e+    
    sta zp_iwa_1                                                      ; 9797: 85 2b       .+    
    bcc c97a3                                                         ; 9799: 90 08       ..    
; &979b referenced 1 time by &9782
.c979b
    asl zp_iwa                                                        ; 979b: 06 2a       .*    
    rol zp_iwa_1                                                      ; 979d: 26 2b       &+    
    asl zp_iwa                                                        ; 979f: 06 2a       .*    
    rol zp_iwa_1                                                      ; 97a1: 26 2b       &+    
; &97a3 referenced 1 time by &9799
.c97a3
    tya                                                               ; 97a3: 98          .     
    adc zp_iwa                                                        ; 97a4: 65 2a       e*    
    sta zp_iwa                                                        ; 97a6: 85 2a       .*    
    bcc c97ad                                                         ; 97a8: 90 03       ..    
    inc zp_iwa_1                                                      ; 97aa: e6 2b       .+    
    clc                                                               ; 97ac: 18          .     
; &97ad referenced 1 time by &97a8
.c97ad
    lda zp_general                                                    ; 97ad: a5 37       .7    
    adc zp_iwa                                                        ; 97af: 65 2a       e*    
    sta zp_iwa                                                        ; 97b1: 85 2a       .*    
    lda l0038                                                         ; 97b3: a5 38       .8    
    adc zp_iwa_1                                                      ; 97b5: 65 2b       e+    
    sta zp_iwa_1                                                      ; 97b7: 85 2b       .+    
    rts                                                               ; 97b9: 60          `     
; &97ba referenced 3 times by &971c, &975a, &977a
.sub_c97ba
    lda zp_iwa_1                                                      ; 97ba: a5 2b       .+    
    and #&c0                                                          ; 97bc: 29 c0       ).    
    ora zp_iwa_2                                                      ; 97be: 05 2c       .,    
    ora zp_iwa_3                                                      ; 97c0: 05 2d       .-    
    bne c97d1                                                         ; 97c2: d0 0d       ..    
    lda zp_iwa                                                        ; 97c4: a5 2a       .*    
    cmp (zp_general),y                                                ; 97c6: d1 37       .7    
    iny                                                               ; 97c8: c8          .     
    lda zp_iwa_1                                                      ; 97c9: a5 2b       .+    
    sbc (zp_general),y                                                ; 97cb: f1 37       .7    
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
    inc zp_text_ptr_off                                               ; 97dd: e6 0a       ..    
; &97df referenced 10 times by &8b2d, &8f31, &8f40, &8f6e, &8f80, &9295, &98e3, &b5ac, &b5d8, &b99a
.sub_c97df
    ldy zp_text_ptr_off                                               ; 97df: a4 0a       ..    
    lda (zp_text_ptr),y                                               ; 97e1: b1 0b       ..    
    cmp #&20 ; ' '                                                    ; 97e3: c9 20       .     
    beq loop_c97dd                                                    ; 97e5: f0 f6       ..    
    cmp #&8d                                                          ; 97e7: c9 8d       ..    
    bne c9805                                                         ; 97e9: d0 1a       ..    
; &97eb referenced 2 times by &903d, &b659
.sub_c97eb
    iny                                                               ; 97eb: c8          .     
    lda (zp_text_ptr),y                                               ; 97ec: b1 0b       ..    
    asl a                                                             ; 97ee: 0a          .     
    asl a                                                             ; 97ef: 0a          .     
    tax                                                               ; 97f0: aa          .     
    and #&c0                                                          ; 97f1: 29 c0       ).    
    iny                                                               ; 97f3: c8          .     
    eor (zp_text_ptr),y                                               ; 97f4: 51 0b       Q.    
    sta zp_iwa                                                        ; 97f6: 85 2a       .*    
    txa                                                               ; 97f8: 8a          .     
    asl a                                                             ; 97f9: 0a          .     
    asl a                                                             ; 97fa: 0a          .     
    iny                                                               ; 97fb: c8          .     
    eor (zp_text_ptr),y                                               ; 97fc: 51 0b       Q.    
    sta zp_iwa_1                                                      ; 97fe: 85 2b       .+    
    iny                                                               ; 9800: c8          .     
    sty zp_text_ptr_off                                               ; 9801: 84 0a       ..    
    sec                                                               ; 9803: 38          8     
    rts                                                               ; 9804: 60          `     
; &9805 referenced 1 time by &97e9
.c9805
    clc                                                               ; 9805: 18          .     
    rts                                                               ; 9806: 60          `     
; &9807 referenced 1 time by &92eb
.sub_c9807
    lda zp_text_ptr                                                   ; 9807: a5 0b       ..    
    sta zp_text_ptr2                                                  ; 9809: 85 19       ..    
    lda l000c                                                         ; 980b: a5 0c       ..    
    sta l001a                                                         ; 980d: 85 1a       ..    
    lda zp_text_ptr_off                                               ; 980f: a5 0a       ..    
    sta zp_text_ptr2_off                                              ; 9811: 85 1b       ..    
; &9813 referenced 4 times by &8bee, &8bfe, &981b, &bf34
.c9813
    ldy zp_text_ptr2_off                                              ; 9813: a4 1b       ..    
    inc zp_text_ptr2_off                                              ; 9815: e6 1b       ..    
    lda (zp_text_ptr2),y                                              ; 9817: b1 19       ..    
    cmp #&20 ; ' '                                                    ; 9819: c9 20       .     
    beq c9813                                                         ; 981b: f0 f6       ..    
    cmp #&3d ; '='                                                    ; 981d: c9 3d       .=    
    beq c9849                                                         ; 981f: f0 28       .(    
; &9821 referenced 1 time by &9846
.loop_c9821
    brk                                                               ; 9821: 00          .     
    equb &04                                                          ; 9822: 04          .     
    equs "Mistake"                                                    ; 9823: 4d 69 73... Mis...
; &982a referenced 7 times by &8604, &8855, &8c0b, &8f2e, &986b, &b6a0, &b9c7
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
; &9841 referenced 2 times by &8bd2, &b7ce
.sub_c9841
    jsr skip_spaces_ptr2                                              ; 9841: 20 8c 8a     ..   
    cmp #&3d ; '='                                                    ; 9844: c9 3d       .=    
    bne loop_c9821                                                    ; 9846: d0 d9       ..    
    rts                                                               ; 9848: 60          `     
; &9849 referenced 2 times by &981f, &bf5f
.c9849
    jsr sub_c9b29                                                     ; 9849: 20 29 9b     ).   
; &984c referenced 4 times by &8b56, &b58f, &bbb4, &beda
.c984c
    txa                                                               ; 984c: 8a          .     
    ldy zp_text_ptr2_off                                              ; 984d: a4 1b       ..    
    jmp c9861                                                         ; 984f: 4c 61 98    La.   
; &9852 referenced 8 times by &8f0e, &9315, &9383, &9406, &b461, &b484, &b4a3, &bf9c
.sub_c9852
    ldy zp_text_ptr2_off                                              ; 9852: a4 1b       ..    
    jmp c9859                                                         ; 9854: 4c 59 98    LY.   
; ***************************************************************************************
; Check for end of statement
;
; Skip spaces and require the statement to end here: a colon, an end-of-line (&0D), or
; ELSE. Anything else raises "Syntax error". Also polls for Escape.
; &9857 referenced 25 times by &8ab6, &8ac8, &8ad0, &8ada, &8b98, &8ebd, &8ec4, &8f45, &8f8f, &928d, &92a5, &92b9, &92c2, &9362, &9394, &93a0, &9880, &b5e3, &b88b, &b8b6, &b8cf, &b8e4, &bb07, &bd11, &bfe4
.check_end_of_statement
    ldy zp_text_ptr_off                                               ; 9857: a4 0a       ..    
; &9859 referenced 2 times by &858c, &9854
.c9859
    dey                                                               ; 9859: 88          .     
; &985a referenced 1 time by &985f
.loop_c985a
    iny                                                               ; 985a: c8          .     
    lda (zp_text_ptr),y                                               ; 985b: b1 0b       ..    
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
; &986d referenced 8 times by &850f, &8b73, &9863, &9867, &b16e, &b5ff, &b8fc, &bbea
.c986d
    clc                                                               ; 986d: 18          .     
    tya                                                               ; 986e: 98          .     
    adc zp_text_ptr                                                   ; 986f: 65 0b       e.    
    sta zp_text_ptr                                                   ; 9871: 85 0b       ..    
    bcc c9877                                                         ; 9873: 90 02       ..    
    inc l000c                                                         ; 9875: e6 0c       ..    
; &9877 referenced 4 times by &9873, &98eb, &b74b, &b964
.c9877
    ldy #1                                                            ; 9877: a0 01       ..    
    sty zp_text_ptr_off                                               ; 9879: 84 0a       ..    
; &987b referenced 1 time by &8f56
.sub_c987b
    bit l00ff                                                         ; 987b: 24 ff       $.    
    bmi c9838                                                         ; 987d: 30 b9       0.    
; &987f referenced 1 time by &9888
.return_14
    rts                                                               ; 987f: 60          `     
; &9880 referenced 1 time by &b837
.sub_c9880
    jsr check_end_of_statement                                        ; 9880: 20 57 98     W.   
    dey                                                               ; 9883: 88          .     
    lda (zp_text_ptr),y                                               ; 9884: b1 0b       ..    
    cmp #&3a ; ':'                                                    ; 9886: c9 3a       .:    
    beq return_14                                                     ; 9888: f0 f5       ..    
    lda l000c                                                         ; 988a: a5 0c       ..    
    cmp #7                                                            ; 988c: c9 07       ..    
    beq c98bc                                                         ; 988e: f0 2c       .,    
; &9890 referenced 2 times by &859f, &8b91
.sub_c9890
    iny                                                               ; 9890: c8          .     
    lda (zp_text_ptr),y                                               ; 9891: b1 0b       ..    
    bmi c98bc                                                         ; 9893: 30 27       0'    
    lda zp_trace_flag                                                 ; 9895: a5 20       .     
    beq c98ac                                                         ; 9897: f0 13       ..    
    tya                                                               ; 9899: 98          .     
    pha                                                               ; 989a: 48          H     
    iny                                                               ; 989b: c8          .     
    lda (zp_text_ptr),y                                               ; 989c: b1 0b       ..    
    pha                                                               ; 989e: 48          H     
    dey                                                               ; 989f: 88          .     
    lda (zp_text_ptr),y                                               ; 98a0: b1 0b       ..    
    tay                                                               ; 98a2: a8          .     
    pla                                                               ; 98a3: 68          h     
    jsr iwa_from_ya                                                   ; 98a4: 20 ea ae     ..   
    jsr sub_c9905                                                     ; 98a7: 20 05 99     ..   
    pla                                                               ; 98aa: 68          h     
    tay                                                               ; 98ab: a8          .     
; &98ac referenced 1 time by &9897
.c98ac
    iny                                                               ; 98ac: c8          .     
    sec                                                               ; 98ad: 38          8     
    tya                                                               ; 98ae: 98          .     
    adc zp_text_ptr                                                   ; 98af: 65 0b       e.    
    sta zp_text_ptr                                                   ; 98b1: 85 0b       ..    
    bcc c98b7                                                         ; 98b3: 90 02       ..    
    inc l000c                                                         ; 98b5: e6 0c       ..    
; &98b7 referenced 1 time by &98b3
.c98b7
    ldy #1                                                            ; 98b7: a0 01       ..    
    sty zp_text_ptr_off                                               ; 98b9: 84 0a       ..    
; &98bb referenced 1 time by &990d
.return_15
    rts                                                               ; 98bb: 60          `     
; &98bc referenced 2 times by &988e, &9893
.c98bc
    jmp immediate_loop                                                ; 98bc: 4c f6 8a    L..   
; &98bf referenced 1 time by &98c5
.loop_c98bf
    jmp c8c0e                                                         ; 98bf: 4c 0e 8c    L..   
; ***************************************************************************************
; IF
;
; Conditional execution: evaluate the expression and run the THEN part, else skip to ELSE
; or the end of the line. IF expr [THEN] ... [ELSE ...].
.stmt_if
    jsr eval_expr                                                     ; 98c2: 20 1d 9b     ..   
    beq loop_c98bf                                                    ; 98c5: f0 f8       ..    
    bpl c98cc                                                         ; 98c7: 10 03       ..    
    jsr fwa_to_int                                                    ; 98c9: 20 e4 a3     ..   
; &98cc referenced 1 time by &98c7
.c98cc
    ldy zp_text_ptr2_off                                              ; 98cc: a4 1b       ..    
    sty zp_text_ptr_off                                               ; 98ce: 84 0a       ..    
    lda zp_iwa                                                        ; 98d0: a5 2a       .*    
    ora zp_iwa_1                                                      ; 98d2: 05 2b       .+    
    ora zp_iwa_2                                                      ; 98d4: 05 2c       .,    
    ora zp_iwa_3                                                      ; 98d6: 05 2d       .-    
    beq c98f1                                                         ; 98d8: f0 17       ..    
    cpx #&8c                                                          ; 98da: e0 8c       ..    
    beq c98e1                                                         ; 98dc: f0 03       ..    
; &98de referenced 1 time by &98e6
.loop_c98de
    jmp c8ba3                                                         ; 98de: 4c a3 8b    L..   
; &98e1 referenced 1 time by &98dc
.c98e1
    inc zp_text_ptr_off                                               ; 98e1: e6 0a       ..    
; &98e3 referenced 2 times by &9900, &b997
.c98e3
    jsr sub_c97df                                                     ; 98e3: 20 df 97     ..   
    bcc loop_c98de                                                    ; 98e6: 90 f6       ..    
    jsr cb9af                                                         ; 98e8: 20 af b9     ..   
    jsr c9877                                                         ; 98eb: 20 77 98     w.   
    jmp cb8d2                                                         ; 98ee: 4c d2 b8    L..   
; &98f1 referenced 1 time by &98d8
.c98f1
    ldy zp_text_ptr_off                                               ; 98f1: a4 0a       ..    
; &98f3 referenced 1 time by &98fc
.loop_c98f3
    lda (zp_text_ptr),y                                               ; 98f3: b1 0b       ..    
    cmp #&0d                                                          ; 98f5: c9 0d       ..    
    beq c9902                                                         ; 98f7: f0 09       ..    
    iny                                                               ; 98f9: c8          .     
    cmp #&8b                                                          ; 98fa: c9 8b       ..    
    bne loop_c98f3                                                    ; 98fc: d0 f5       ..    
    sty zp_text_ptr_off                                               ; 98fe: 84 0a       ..    
    beq c98e3                                                         ; 9900: f0 e1       ..    
; &9902 referenced 1 time by &98f7
.c9902
    jmp c8b87                                                         ; 9902: 4c 87 8b    L..   
; &9905 referenced 2 times by &98a7, &b8d6
.sub_c9905
    lda zp_iwa                                                        ; 9905: a5 2a       .*    
    cmp zp_trace_max                                                  ; 9907: c5 21       .!    
    lda zp_iwa_1                                                      ; 9909: a5 2b       .+    
    sbc l0022                                                         ; 990b: e5 22       ."    
    bcs return_15                                                     ; 990d: b0 ac       ..    
    lda #&5b ; '['                                                    ; 990f: a9 5b       .[    
    jsr cb558                                                         ; 9911: 20 58 b5     X.   
    jsr sub_c991f                                                     ; 9914: 20 1f 99     ..   
    lda #&5d ; ']'                                                    ; 9917: a9 5d       .]    
    jsr cb558                                                         ; 9919: 20 58 b5     X.   
    jmp cb565                                                         ; 991c: 4c 65 b5    Le.   
; &991f referenced 2 times by &9914, &b662
.sub_c991f
    lda #0                                                            ; 991f: a9 00       ..    
    beq c9925                                                         ; 9921: f0 02       ..    
; &9923 referenced 2 times by &90b8, &b61d
.sub_c9923
    lda #5                                                            ; 9923: a9 05       ..    
; &9925 referenced 1 time by &9921
.c9925
    sta zp_print_bytes                                                ; 9925: 85 14       ..    
    ldx #4                                                            ; 9927: a2 04       ..    
; &9929 referenced 1 time by &9944
.loop_c9929
    lda #0                                                            ; 9929: a9 00       ..    
    sta zp_fwb_m2,x                                                   ; 992b: 95 3f       .?    
    sec                                                               ; 992d: 38          8     
; &992e referenced 1 time by &9941
.loop_c992e
    lda zp_iwa                                                        ; 992e: a5 2a       .*    
    sbc l996b,x                                                       ; 9930: fd 6b 99    .k.   
    tay                                                               ; 9933: a8          .     
    lda zp_iwa_1                                                      ; 9934: a5 2b       .+    
    sbc l99b9,x                                                       ; 9936: fd b9 99    ...   
    bcc c9943                                                         ; 9939: 90 08       ..    
    sta zp_iwa_1                                                      ; 993b: 85 2b       .+    
    sty zp_iwa                                                        ; 993d: 84 2a       .*    
    inc zp_fwb_m2,x                                                   ; 993f: f6 3f       .?    
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
    lda zp_fwb_m2,x                                                   ; 994b: b5 3f       .?    
    beq loop_c9948                                                    ; 994d: f0 f9       ..    
; &994f referenced 1 time by &9949
.c994f
    stx zp_general                                                    ; 994f: 86 37       .7    
    lda zp_print_bytes                                                ; 9951: a5 14       ..    
    beq c9960                                                         ; 9953: f0 0b       ..    
    sbc zp_general                                                    ; 9955: e5 37       .7    
    beq c9960                                                         ; 9957: f0 07       ..    
    tay                                                               ; 9959: a8          .     
; &995a referenced 1 time by &995e
.loop_c995a
    jsr cb565                                                         ; 995a: 20 65 b5     e.   
    dey                                                               ; 995d: 88          .     
    bne loop_c995a                                                    ; 995e: d0 fa       ..    
; &9960 referenced 3 times by &9953, &9957, &9968
.c9960
    lda zp_fwb_m2,x                                                   ; 9960: b5 3f       .?    
    ora #&30 ; '0'                                                    ; 9962: 09 30       .0    
    jsr cb558                                                         ; 9964: 20 58 b5     X.   
    dex                                                               ; 9967: ca          .     
    bpl c9960                                                         ; 9968: 10 f6       ..    
    rts                                                               ; 996a: 60          `     
; &996b referenced 1 time by &9930
.l996b
    equb &01, &0a, &64, &e8, &10                                      ; 996b: 01 0a 64... ..d...
; &9970 referenced 3 times by &b5ec, &b9af, &bc2d
.sub_c9970
    ldy #0                                                            ; 9970: a0 00       ..    
    sty zp_fwb_exp                                                    ; 9972: 84 3d       .=    
    lda zp_page                                                       ; 9974: a5 18       ..    
    sta zp_fwb_m1                                                     ; 9976: 85 3e       .>    
; &9978 referenced 2 times by &9988, &998c
.c9978
    ldy #1                                                            ; 9978: a0 01       ..    
    lda (zp_fwb_exp),y                                                ; 997a: b1 3d       .=    
    cmp zp_iwa_1                                                      ; 997c: c5 2b       .+    
    bcs c998e                                                         ; 997e: b0 0e       ..    
; &9980 referenced 1 time by &9996
.loop_c9980
    ldy #3                                                            ; 9980: a0 03       ..    
    lda (zp_fwb_exp),y                                                ; 9982: b1 3d       .=    
    adc zp_fwb_exp                                                    ; 9984: 65 3d       e=    
    sta zp_fwb_exp                                                    ; 9986: 85 3d       .=    
    bcc c9978                                                         ; 9988: 90 ee       ..    
    inc zp_fwb_m1                                                     ; 998a: e6 3e       .>    
    bcs c9978                                                         ; 998c: b0 ea       ..    
; &998e referenced 1 time by &997e
.c998e
    bne c99a4                                                         ; 998e: d0 14       ..    
    ldy #2                                                            ; 9990: a0 02       ..    
    lda (zp_fwb_exp),y                                                ; 9992: b1 3d       .=    
    cmp zp_iwa                                                        ; 9994: c5 2a       .*    
    bcc loop_c9980                                                    ; 9996: 90 e8       ..    
    bne c99a4                                                         ; 9998: d0 0a       ..    
    tya                                                               ; 999a: 98          .     
    adc zp_fwb_exp                                                    ; 999b: 65 3d       e=    
    sta zp_fwb_exp                                                    ; 999d: 85 3d       .=    
    bcc c99a4                                                         ; 999f: 90 03       ..    
    inc zp_fwb_m1                                                     ; 99a1: e6 3e       .>    
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
    jsr coerce_to_integer                                             ; 99bf: 20 f0 92     ..   
    lda zp_iwa_3                                                      ; 99c2: a5 2d       .-    
    pha                                                               ; 99c4: 48          H     
    jsr iwa_abs                                                       ; 99c5: 20 71 ad     q.   
    jsr sub_c9e1d                                                     ; 99c8: 20 1d 9e     ..   
    stx zp_var_type                                                   ; 99cb: 86 27       .'    
    tay                                                               ; 99cd: a8          .     
    jsr coerce_to_integer                                             ; 99ce: 20 f0 92     ..   
    pla                                                               ; 99d1: 68          h     
    sta l0038                                                         ; 99d2: 85 38       .8    
    eor zp_iwa_3                                                      ; 99d4: 45 2d       E-    
    sta zp_general                                                    ; 99d6: 85 37       .7    
    jsr iwa_abs                                                       ; 99d8: 20 71 ad     q.   
    ldx #&39 ; '9'                                                    ; 99db: a2 39       .9    
    jsr sub_cbe0d                                                     ; 99dd: 20 0d be     ..   
    sty zp_fwb_exp                                                    ; 99e0: 84 3d       .=    
    sty zp_fwb_m1                                                     ; 99e2: 84 3e       .>    
    sty zp_fwb_m2                                                     ; 99e4: 84 3f       .?    
    sty zp_fwb_m3                                                     ; 99e6: 84 40       .@    
    lda zp_iwa_3                                                      ; 99e8: a5 2d       .-    
    ora zp_iwa                                                        ; 99ea: 05 2a       .*    
    ora zp_iwa_1                                                      ; 99ec: 05 2b       .+    
    ora zp_iwa_2                                                      ; 99ee: 05 2c       .,    
    beq c99a7                                                         ; 99f0: f0 b5       ..    
    ldy #&20 ; ' '                                                    ; 99f2: a0 20       .     
; &99f4 referenced 1 time by &99ff
.loop_c99f4
    dey                                                               ; 99f4: 88          .     
    beq return_16                                                     ; 99f5: f0 41       .A    
    asl zp_fileblk                                                    ; 99f7: 06 39       .9    
    rol l003a                                                         ; 99f9: 26 3a       &:    
    rol zp_fwb_sign                                                   ; 99fb: 26 3b       &;    
    rol zp_fwb_ovf                                                    ; 99fd: 26 3c       &<    
    bpl loop_c99f4                                                    ; 99ff: 10 f3       ..    
; &9a01 referenced 1 time by &9a36
.loop_c9a01
    rol zp_fileblk                                                    ; 9a01: 26 39       &9    
    rol l003a                                                         ; 9a03: 26 3a       &:    
    rol zp_fwb_sign                                                   ; 9a05: 26 3b       &;    
    rol zp_fwb_ovf                                                    ; 9a07: 26 3c       &<    
    rol zp_fwb_exp                                                    ; 9a09: 26 3d       &=    
    rol zp_fwb_m1                                                     ; 9a0b: 26 3e       &>    
    rol zp_fwb_m2                                                     ; 9a0d: 26 3f       &?    
    rol zp_fwb_m3                                                     ; 9a0f: 26 40       &@    
    sec                                                               ; 9a11: 38          8     
    lda zp_fwb_exp                                                    ; 9a12: a5 3d       .=    
    sbc zp_iwa                                                        ; 9a14: e5 2a       .*    
    pha                                                               ; 9a16: 48          H     
    lda zp_fwb_m1                                                     ; 9a17: a5 3e       .>    
    sbc zp_iwa_1                                                      ; 9a19: e5 2b       .+    
    pha                                                               ; 9a1b: 48          H     
    lda zp_fwb_m2                                                     ; 9a1c: a5 3f       .?    
    sbc zp_iwa_2                                                      ; 9a1e: e5 2c       .,    
    tax                                                               ; 9a20: aa          .     
    lda zp_fwb_m3                                                     ; 9a21: a5 40       .@    
    sbc zp_iwa_3                                                      ; 9a23: e5 2d       .-    
    bcc c9a33                                                         ; 9a25: 90 0c       ..    
    sta zp_fwb_m3                                                     ; 9a27: 85 40       .@    
    stx zp_fwb_m2                                                     ; 9a29: 86 3f       .?    
    pla                                                               ; 9a2b: 68          h     
    sta zp_fwb_m1                                                     ; 9a2c: 85 3e       .>    
    pla                                                               ; 9a2e: 68          h     
    sta zp_fwb_exp                                                    ; 9a2f: 85 3d       .=    
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
.return_16
    rts                                                               ; 9a38: 60          `     
; &9a39 referenced 1 time by &9aab
.loop_c9a39
    stx zp_var_type                                                   ; 9a39: 86 27       .'    
    jsr unstack_integer                                               ; 9a3b: 20 ea bd     ..   
    jsr stack_real                                                    ; 9a3e: 20 51 bd     Q.   
    jsr int_to_fwa                                                    ; 9a41: 20 be a2     ..   
    jsr fwb_copy_from_fwa                                             ; 9a44: 20 1e a2     ..   
    jsr sub_cbd7e                                                     ; 9a47: 20 7e bd     ~.   
    jsr fwa_unpack_var                                                ; 9a4a: 20 b5 a3     ..   
    jmp c9a62                                                         ; 9a4d: 4c 62 9a    Lb.   
; &9a50 referenced 1 time by &9aa0
.loop_c9a50
    jsr stack_real                                                    ; 9a50: 20 51 bd     Q.   
    jsr sub_c9c42                                                     ; 9a53: 20 42 9c     B.   
    stx zp_var_type                                                   ; 9a56: 86 27       .'    
    tay                                                               ; 9a58: a8          .     
    jsr sub_c92fd                                                     ; 9a59: 20 fd 92     ..   
    jsr sub_cbd7e                                                     ; 9a5c: 20 7e bd     ~.   
; &9a5f referenced 1 time by &b78f
.sub_c9a5f
    jsr fwb_unpack_var                                                ; 9a5f: 20 4e a3     N.   
; &9a62 referenced 1 time by &9a4d
.c9a62
    ldx zp_var_type                                                   ; 9a62: a6 27       .'    
    ldy #0                                                            ; 9a64: a0 00       ..    
    lda zp_fwb_sign                                                   ; 9a66: a5 3b       .;    
    and #&80                                                          ; 9a68: 29 80       ).    
    sta zp_fwb_sign                                                   ; 9a6a: 85 3b       .;    
    lda zp_fwa_sign                                                   ; 9a6c: a5 2e       ..    
    and #&80                                                          ; 9a6e: 29 80       ).    
    cmp zp_fwb_sign                                                   ; 9a70: c5 3b       .;    
    bne return_17                                                     ; 9a72: d0 1e       ..    
    lda zp_fwb_exp                                                    ; 9a74: a5 3d       .=    
    cmp zp_fwa_exp                                                    ; 9a76: c5 30       .0    
    bne c9a93                                                         ; 9a78: d0 19       ..    
    lda zp_fwb_m1                                                     ; 9a7a: a5 3e       .>    
    cmp zp_fwa_m1                                                     ; 9a7c: c5 31       .1    
    bne c9a93                                                         ; 9a7e: d0 13       ..    
    lda zp_fwb_m2                                                     ; 9a80: a5 3f       .?    
    cmp zp_fwa_m2                                                     ; 9a82: c5 32       .2    
    bne c9a93                                                         ; 9a84: d0 0d       ..    
    lda zp_fwb_m3                                                     ; 9a86: a5 40       .@    
    cmp zp_fwa_m3                                                     ; 9a88: c5 33       .3    
    bne c9a93                                                         ; 9a8a: d0 07       ..    
    lda zp_fwb_m4                                                     ; 9a8c: a5 41       .A    
    cmp zp_fwa_m4                                                     ; 9a8e: c5 34       .4    
    bne c9a93                                                         ; 9a90: d0 01       ..    
; &9a92 referenced 1 time by &9a72
.return_17
    rts                                                               ; 9a92: 60          `     
; &9a93 referenced 5 times by &9a78, &9a7e, &9a84, &9a8a, &9a90
.c9a93
    ror a                                                             ; 9a93: 6a          j     
    eor zp_fwb_sign                                                   ; 9a94: 45 3b       E;    
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
    jsr stack_integer                                                 ; 9aa2: 20 94 bd     ..   
    jsr sub_c9c42                                                     ; 9aa5: 20 42 9c     B.   
    tay                                                               ; 9aa8: a8          .     
    beq c9a9a                                                         ; 9aa9: f0 ef       ..    
    bmi loop_c9a39                                                    ; 9aab: 30 8c       0.    
; ***************************************************************************************
; Compare an integer variable with the accumulator
;
; Compare the integer operand against IWA and set flags.
.iwa_test_var
    lda zp_iwa_3                                                      ; 9aad: a5 2d       .-    
    eor #&80                                                          ; 9aaf: 49 80       I.    
    sta zp_iwa_3                                                      ; 9ab1: 85 2d       .-    
    sec                                                               ; 9ab3: 38          8     
    ldy #0                                                            ; 9ab4: a0 00       ..    
    lda (zp_stack_ptr),y                                              ; 9ab6: b1 04       ..    
    sbc zp_iwa                                                        ; 9ab8: e5 2a       .*    
    sta zp_iwa                                                        ; 9aba: 85 2a       .*    
    iny                                                               ; 9abc: c8          .     
    lda (zp_stack_ptr),y                                              ; 9abd: b1 04       ..    
    sbc zp_iwa_1                                                      ; 9abf: e5 2b       .+    
    sta zp_iwa_1                                                      ; 9ac1: 85 2b       .+    
    iny                                                               ; 9ac3: c8          .     
    lda (zp_stack_ptr),y                                              ; 9ac4: b1 04       ..    
    sbc zp_iwa_2                                                      ; 9ac6: e5 2c       .,    
    sta zp_iwa_2                                                      ; 9ac8: 85 2c       .,    
    iny                                                               ; 9aca: c8          .     
    lda (zp_stack_ptr),y                                              ; 9acb: b1 04       ..    
    ldy #0                                                            ; 9acd: a0 00       ..    
    eor #&80                                                          ; 9acf: 49 80       I.    
    sbc zp_iwa_3                                                      ; 9ad1: e5 2d       .-    
    ora zp_iwa                                                        ; 9ad3: 05 2a       .*    
    ora zp_iwa_1                                                      ; 9ad5: 05 2b       .+    
    ora zp_iwa_2                                                      ; 9ad7: 05 2c       .,    
    php                                                               ; 9ad9: 08          .     
    clc                                                               ; 9ada: 18          .     
    lda #4                                                            ; 9adb: a9 04       ..    
    adc zp_stack_ptr                                                  ; 9add: 65 04       e.    
    sta zp_stack_ptr                                                  ; 9adf: 85 04       ..    
    bcc c9ae5                                                         ; 9ae1: 90 02       ..    
    inc zp_stack_ptr_1                                                ; 9ae3: e6 05       ..    
; &9ae5 referenced 1 time by &9ae1
.c9ae5
    plp                                                               ; 9ae5: 28          (     
    rts                                                               ; 9ae6: 60          `     
; &9ae7 referenced 1 time by &9a9e
.c9ae7
    jsr stack_string                                                  ; 9ae7: 20 b2 bd     ..   
    jsr sub_c9c42                                                     ; 9aea: 20 42 9c     B.   
    tay                                                               ; 9aed: a8          .     
    bne c9a9a                                                         ; 9aee: d0 aa       ..    
    stx zp_general                                                    ; 9af0: 86 37       .7    
    ldx zp_strbuf_len                                                 ; 9af2: a6 36       .6    
    ldy #0                                                            ; 9af4: a0 00       ..    
    lda (zp_stack_ptr),y                                              ; 9af6: b1 04       ..    
    sta zp_fileblk                                                    ; 9af8: 85 39       .9    
    cmp zp_strbuf_len                                                 ; 9afa: c5 36       .6    
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
    lda (zp_stack_ptr),y                                              ; 9b08: b1 04       ..    
    cmp l05ff,y                                                       ; 9b0a: d9 ff 05    ...   
    beq loop_c9b03                                                    ; 9b0d: f0 f4       ..    
    bne c9b15                                                         ; 9b0f: d0 04       ..    
; &9b11 referenced 1 time by &9b05
.c9b11
    lda zp_fileblk                                                    ; 9b11: a5 39       .9    
    cmp zp_strbuf_len                                                 ; 9b13: c5 36       .6    
; &9b15 referenced 1 time by &9b0f
.c9b15
    php                                                               ; 9b15: 08          .     
    jsr cbddc                                                         ; 9b16: 20 dc bd     ..   
    ldx zp_general                                                    ; 9b19: a6 37       .7    
    plp                                                               ; 9b1b: 28          (     
    rts                                                               ; 9b1c: 60          `     
; ***************************************************************************************
; Evaluate an expression
;
; The interpreter's main expression entry point. Copies the primary text pointer (PtrA:
; zp_text_ptr / zp_text_ptr_off) to the secondary pointer (PtrB: zp_text_ptr2 / &1B) and
; evaluates the expression there.
;
; On Exit:
;     ZP_VAR_TYPE (&27): result type (integer / real / string)
;     ZP_IWA / ZP_FWA: the result value
;     &1B: advanced past the expression
; &9b1d referenced 11 times by &8821, &886d, &8b53, &8ed2, &93eb, &98c2, &b58c, &b91e, &b99f, &bbb1, &bed2
.eval_expr
    lda zp_text_ptr                                                   ; 9b1d: a5 0b       ..    
    sta zp_text_ptr2                                                  ; 9b1f: 85 19       ..    
    lda l000c                                                         ; 9b21: a5 0c       ..    
    sta l001a                                                         ; 9b23: 85 1a       ..    
    lda zp_text_ptr_off                                               ; 9b25: a5 0a       ..    
    sta zp_text_ptr2_off                                              ; 9b27: 85 1b       ..    
; &9b29 referenced 16 times by &8d39, &8deb, &92dd, &93fa, &9849, &ac1d, &ace2, &acf0, &ae56, &afcc, &afee, &b039, &b28e, &b4b1, &b84f, &b86d
.sub_c9b29
    jsr sub_c9b72                                                     ; 9b29: 20 72 9b     r.   
; &9b2c referenced 1 time by &9b53
.loop_c9b2c
    cpx #&84                                                          ; 9b2c: e0 84       ..    
    beq c9b3a                                                         ; 9b2e: f0 0a       ..    
    cpx #&82                                                          ; 9b30: e0 82       ..    
    beq c9b55                                                         ; 9b32: f0 21       .!    
    dec zp_text_ptr2_off                                              ; 9b34: c6 1b       ..    
    tay                                                               ; 9b36: a8          .     
    sta zp_var_type                                                   ; 9b37: 85 27       .'    
    rts                                                               ; 9b39: 60          `     
; &9b3a referenced 1 time by &9b2e
.c9b3a
    jsr sub_c9b6b                                                     ; 9b3a: 20 6b 9b     k.   
    tay                                                               ; 9b3d: a8          .     
    jsr coerce_to_integer                                             ; 9b3e: 20 f0 92     ..   
    ldy #3                                                            ; 9b41: a0 03       ..    
; &9b43 referenced 1 time by &9b4c
.loop_c9b43
    lda (zp_stack_ptr),y                                              ; 9b43: b1 04       ..    
    ora zp_iwa,y                                                      ; 9b45: 19 2a 00    .*.   
    sta zp_iwa,y                                                      ; 9b48: 99 2a 00    .*.   
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
    jsr coerce_to_integer                                             ; 9b59: 20 f0 92     ..   
    ldy #3                                                            ; 9b5c: a0 03       ..    
; &9b5e referenced 1 time by &9b67
.loop_c9b5e
    lda (zp_stack_ptr),y                                              ; 9b5e: b1 04       ..    
    eor zp_iwa,y                                                      ; 9b60: 59 2a 00    Y*.   
    sta zp_iwa,y                                                      ; 9b63: 99 2a 00    .*.   
    dey                                                               ; 9b66: 88          .     
    bpl loop_c9b5e                                                    ; 9b67: 10 f5       ..    
    bmi loop_c9b4e                                                    ; 9b69: 30 e3       0.    
; &9b6b referenced 2 times by &9b3a, &9b55
.sub_c9b6b
    tay                                                               ; 9b6b: a8          .     
    jsr coerce_to_integer                                             ; 9b6c: 20 f0 92     ..   
    jsr stack_integer                                                 ; 9b6f: 20 94 bd     ..   
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
    jsr coerce_to_integer                                             ; 9b7b: 20 f0 92     ..   
    jsr stack_integer                                                 ; 9b7e: 20 94 bd     ..   
    jsr sub_c9b9c                                                     ; 9b81: 20 9c 9b     ..   
    tay                                                               ; 9b84: a8          .     
    jsr coerce_to_integer                                             ; 9b85: 20 f0 92     ..   
    ldy #3                                                            ; 9b88: a0 03       ..    
; &9b8a referenced 1 time by &9b93
.loop_c9b8a
    lda (zp_stack_ptr),y                                              ; 9b8a: b1 04       ..    
    and zp_iwa,y                                                      ; 9b8c: 39 2a 00    9*.   
    sta zp_iwa,y                                                      ; 9b8f: 99 2a 00    .*.   
    dey                                                               ; 9b92: 88          .     
    bpl loop_c9b8a                                                    ; 9b93: 10 f5       ..    
    jsr sub_cbdff                                                     ; 9b95: 20 ff bd     ..   
    lda #&40 ; '@'                                                    ; 9b98: a9 40       .@    
    bne loop_c9b75                                                    ; 9b9a: d0 d9       ..    
; &9b9c referenced 2 times by &9b72, &9b81
.sub_c9b9c
    jsr sub_c9c42                                                     ; 9b9c: 20 42 9c     B.   
    cpx #&3f ; '?'                                                    ; 9b9f: e0 3f       .?    
    bcs return_18                                                     ; 9ba1: b0 04       ..    
    cpx #&3c ; '<'                                                    ; 9ba3: e0 3c       .<    
    bcs c9ba8                                                         ; 9ba5: b0 01       ..    
; &9ba7 referenced 1 time by &9ba1
.return_18
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
    sty zp_iwa                                                        ; 9bb5: 84 2a       .*    
    sty zp_iwa_1                                                      ; 9bb7: 84 2b       .+    
    sty zp_iwa_2                                                      ; 9bb9: 84 2c       .,    
    sty zp_iwa_3                                                      ; 9bbb: 84 2d       .-    
    lda #&40 ; '@'                                                    ; 9bbd: a9 40       .@    
    rts                                                               ; 9bbf: 60          `     
; &9bc0 referenced 1 time by &9ba8
.c9bc0
    tax                                                               ; 9bc0: aa          .     
    ldy zp_text_ptr2_off                                              ; 9bc1: a4 1b       ..    
    lda (zp_text_ptr2),y                                              ; 9bc3: b1 19       ..    
    cmp #&3d ; '='                                                    ; 9bc5: c9 3d       .=    
    beq c9bd4                                                         ; 9bc7: f0 0b       ..    
    cmp #&3e ; '>'                                                    ; 9bc9: c9 3e       .>    
    beq c9bdf                                                         ; 9bcb: f0 12       ..    
    jsr sub_c9a9d                                                     ; 9bcd: 20 9d 9a     ..   
    bcc c9bb4                                                         ; 9bd0: 90 e2       ..    
    bcs c9bb5                                                         ; 9bd2: b0 e1       ..    
; &9bd4 referenced 1 time by &9bc7
.c9bd4
    inc zp_text_ptr2_off                                              ; 9bd4: e6 1b       ..    
    jsr sub_c9a9d                                                     ; 9bd6: 20 9d 9a     ..   
    beq c9bb4                                                         ; 9bd9: f0 d9       ..    
    bcc c9bb4                                                         ; 9bdb: 90 d7       ..    
    bcs c9bb5                                                         ; 9bdd: b0 d6       ..    
; &9bdf referenced 1 time by &9bcb
.c9bdf
    inc zp_text_ptr2_off                                              ; 9bdf: e6 1b       ..    
    jsr sub_c9a9d                                                     ; 9be1: 20 9d 9a     ..   
    bne c9bb4                                                         ; 9be4: d0 ce       ..    
    beq c9bb5                                                         ; 9be6: f0 cd       ..    
; &9be8 referenced 1 time by &9bac
.c9be8
    tax                                                               ; 9be8: aa          .     
    ldy zp_text_ptr2_off                                              ; 9be9: a4 1b       ..    
    lda (zp_text_ptr2),y                                              ; 9beb: b1 19       ..    
    cmp #&3d ; '='                                                    ; 9bed: c9 3d       .=    
    beq c9bfa                                                         ; 9bef: f0 09       ..    
    jsr sub_c9a9d                                                     ; 9bf1: 20 9d 9a     ..   
    beq c9bb5                                                         ; 9bf4: f0 bf       ..    
    bcs c9bb4                                                         ; 9bf6: b0 bc       ..    
    bcc c9bb5                                                         ; 9bf8: 90 bb       ..    
; &9bfa referenced 1 time by &9bef
.c9bfa
    inc zp_text_ptr2_off                                              ; 9bfa: e6 1b       ..    
    jsr sub_c9a9d                                                     ; 9bfc: 20 9d 9a     ..   
    bcs c9bb4                                                         ; 9bff: b0 b3       ..    
    bcc c9bb5                                                         ; 9c01: 90 b2       ..    
; &9c03 referenced 2 times by &9c27, &b0fb
.c9c03
    brk                                                               ; 9c03: 00          .     
    equb &13                                                          ; 9c04: 13          .     
    equs "String too long"                                            ; 9c05: 53 74 72... Str...
    equb &00                                                          ; 9c14: 00          .     
; &9c15 referenced 1 time by &9c4f
.loop_c9c15
    jsr stack_string                                                  ; 9c15: 20 b2 bd     ..   
    jsr sub_c9e20                                                     ; 9c18: 20 20 9e      .   
    tay                                                               ; 9c1b: a8          .     
    bne c9c88                                                         ; 9c1c: d0 6a       .j    
    clc                                                               ; 9c1e: 18          .     
    stx zp_general                                                    ; 9c1f: 86 37       .7    
    ldy #0                                                            ; 9c21: a0 00       ..    
    lda (zp_stack_ptr),y                                              ; 9c23: b1 04       ..    
    adc zp_strbuf_len                                                 ; 9c25: 65 36       e6    
    bcs c9c03                                                         ; 9c27: b0 da       ..    
    tax                                                               ; 9c29: aa          .     
    pha                                                               ; 9c2a: 48          H     
    ldy zp_strbuf_len                                                 ; 9c2b: a4 36       .6    
; &9c2d referenced 1 time by &9c35
.loop_c9c2d
    lda l05ff,y                                                       ; 9c2d: b9 ff 05    ...   
    sta l05ff,x                                                       ; 9c30: 9d ff 05    ...   
    dex                                                               ; 9c33: ca          .     
    dey                                                               ; 9c34: 88          .     
    bne loop_c9c2d                                                    ; 9c35: d0 f6       ..    
    jsr sub_cbdcb                                                     ; 9c37: 20 cb bd     ..   
    pla                                                               ; 9c3a: 68          h     
    sta zp_strbuf_len                                                 ; 9c3b: 85 36       .6    
    ldx zp_general                                                    ; 9c3d: a6 37       .7    
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
; ***************************************************************************************
; Integer add
;
; IWA = IWA + the integer operand on the BASIC stack.
;
; On Entry:
;     ZP_IWA (&2A): one 32-bit operand
;     (ZP_STACK_PTR) (&04): the other operand on the BASIC stack
;     X: 4
;
; On Exit:
;     ZP_IWA: the sum
.iwa_add
    ldy #0                                                            ; 9c5b: a0 00       ..    
    clc                                                               ; 9c5d: 18          .     
    lda (zp_stack_ptr),y                                              ; 9c5e: b1 04       ..    
    adc zp_iwa                                                        ; 9c60: 65 2a       e*    
    sta zp_iwa                                                        ; 9c62: 85 2a       .*    
    iny                                                               ; 9c64: c8          .     
    lda (zp_stack_ptr),y                                              ; 9c65: b1 04       ..    
    adc zp_iwa_1                                                      ; 9c67: 65 2b       e+    
    sta zp_iwa_1                                                      ; 9c69: 85 2b       .+    
    iny                                                               ; 9c6b: c8          .     
    lda (zp_stack_ptr),y                                              ; 9c6c: b1 04       ..    
    adc zp_iwa_2                                                      ; 9c6e: 65 2c       e,    
    sta zp_iwa_2                                                      ; 9c70: 85 2c       .,    
    iny                                                               ; 9c72: c8          .     
    lda (zp_stack_ptr),y                                              ; 9c73: b1 04       ..    
    adc zp_iwa_3                                                      ; 9c75: 65 2d       e-    
; &9c77 referenced 1 time by &9cde
.c9c77
    sta zp_iwa_3                                                      ; 9c77: 85 2d       .-    
    clc                                                               ; 9c79: 18          .     
    lda zp_stack_ptr                                                  ; 9c7a: a5 04       ..    
    adc #4                                                            ; 9c7c: 69 04       i.    
    sta zp_stack_ptr                                                  ; 9c7e: 85 04       ..    
    lda #&40 ; '@'                                                    ; 9c80: a9 40       .@    
    bcc c9c45                                                         ; 9c82: 90 c1       ..    
    inc zp_stack_ptr_1                                                ; 9c84: e6 05       ..    
    bcs c9c45                                                         ; 9c86: b0 bd       ..    
; &9c88 referenced 6 times by &9c1c, &9c57, &9c92, &9cb6, &9cbe, &9ce8
.c9c88
    jmp c8c0e                                                         ; 9c88: 4c 0e 8c    L..   
; &9c8b referenced 1 time by &9c51
.c9c8b
    jsr stack_real                                                    ; 9c8b: 20 51 bd     Q.   
    jsr sub_c9dd1                                                     ; 9c8e: 20 d1 9d     ..   
    tay                                                               ; 9c91: a8          .     
    beq c9c88                                                         ; 9c92: f0 f4       ..    
    stx zp_var_type                                                   ; 9c94: 86 27       .'    
    bmi c9c9b                                                         ; 9c96: 30 03       0.    
    jsr int_to_fwa                                                    ; 9c98: 20 be a2     ..   
; &9c9b referenced 2 times by &9c96, &9cb2
.c9c9b
    jsr sub_cbd7e                                                     ; 9c9b: 20 7e bd     ~.   
    jsr fwa_add_var                                                   ; 9c9e: 20 00 a5     ..   
; &9ca1 referenced 2 times by &9cf7, &9d0b
.c9ca1
    ldx zp_var_type                                                   ; 9ca1: a6 27       .'    
    lda #&ff                                                          ; 9ca3: a9 ff       ..    
    bne c9c45                                                         ; 9ca5: d0 9e       ..    
; &9ca7 referenced 1 time by &9c59
.c9ca7
    stx zp_var_type                                                   ; 9ca7: 86 27       .'    
    jsr unstack_integer                                               ; 9ca9: 20 ea bd     ..   
    jsr stack_real                                                    ; 9cac: 20 51 bd     Q.   
    jsr int_to_fwa                                                    ; 9caf: 20 be a2     ..   
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
; ***************************************************************************************
; Reverse integer subtract
;
; IWA = stacked operand - IWA.
;
; On Entry:
;     ZP_IWA (&2A): the subtrahend
;     (ZP_STACK_PTR) (&04): the minuend on the BASIC stack
;     X: 4
;
; On Exit:
;     ZP_IWA: operand - IWA
.iwa_rsub
    sec                                                               ; 9cc2: 38          8     
    ldy #0                                                            ; 9cc3: a0 00       ..    
    lda (zp_stack_ptr),y                                              ; 9cc5: b1 04       ..    
    sbc zp_iwa                                                        ; 9cc7: e5 2a       .*    
    sta zp_iwa                                                        ; 9cc9: 85 2a       .*    
    iny                                                               ; 9ccb: c8          .     
    lda (zp_stack_ptr),y                                              ; 9ccc: b1 04       ..    
    sbc zp_iwa_1                                                      ; 9cce: e5 2b       .+    
    sta zp_iwa_1                                                      ; 9cd0: 85 2b       .+    
    iny                                                               ; 9cd2: c8          .     
    lda (zp_stack_ptr),y                                              ; 9cd3: b1 04       ..    
    sbc zp_iwa_2                                                      ; 9cd5: e5 2c       .,    
    sta zp_iwa_2                                                      ; 9cd7: 85 2c       .,    
    iny                                                               ; 9cd9: c8          .     
    lda (zp_stack_ptr),y                                              ; 9cda: b1 04       ..    
    sbc zp_iwa_3                                                      ; 9cdc: e5 2d       .-    
    jmp c9c77                                                         ; 9cde: 4c 77 9c    Lw.   
; &9ce1 referenced 1 time by &9cb8
.c9ce1
    jsr stack_real                                                    ; 9ce1: 20 51 bd     Q.   
    jsr sub_c9dd1                                                     ; 9ce4: 20 d1 9d     ..   
    tay                                                               ; 9ce7: a8          .     
    beq c9c88                                                         ; 9ce8: f0 9e       ..    
    stx zp_var_type                                                   ; 9cea: 86 27       .'    
    bmi c9cf1                                                         ; 9cec: 30 03       0.    
    jsr int_to_fwa                                                    ; 9cee: 20 be a2     ..   
; &9cf1 referenced 1 time by &9cec
.c9cf1
    jsr sub_cbd7e                                                     ; 9cf1: 20 7e bd     ~.   
    jsr fwa_rsub_var                                                  ; 9cf4: 20 fd a4     ..   
    jmp c9ca1                                                         ; 9cf7: 4c a1 9c    L..   
; &9cfa referenced 1 time by &9cc0
.c9cfa
    stx zp_var_type                                                   ; 9cfa: 86 27       .'    
    jsr unstack_integer                                               ; 9cfc: 20 ea bd     ..   
    jsr stack_real                                                    ; 9cff: 20 51 bd     Q.   
    jsr int_to_fwa                                                    ; 9d02: 20 be a2     ..   
    jsr sub_cbd7e                                                     ; 9d05: 20 7e bd     ~.   
    jsr sub_ca4d0                                                     ; 9d08: 20 d0 a4     ..   
    jmp c9ca1                                                         ; 9d0b: 4c a1 9c    L..   
; &9d0e referenced 3 times by &9d60, &9d67, &9d6b
.c9d0e
    jsr int_to_fwa                                                    ; 9d0e: 20 be a2     ..   
; &9d11 referenced 1 time by &9d5a
.loop_c9d11
    jsr unstack_integer                                               ; 9d11: 20 ea bd     ..   
    jsr stack_real                                                    ; 9d14: 20 51 bd     Q.   
    jsr int_to_fwa                                                    ; 9d17: 20 be a2     ..   
    jmp c9d2c                                                         ; 9d1a: 4c 2c 9d    L,.   
; &9d1d referenced 3 times by &9d45, &9d4c, &9d50
.c9d1d
    jsr int_to_fwa                                                    ; 9d1d: 20 be a2     ..   
; &9d20 referenced 1 time by &9d3f
.loop_c9d20
    jsr stack_real                                                    ; 9d20: 20 51 bd     Q.   
    jsr sub_c9e20                                                     ; 9d23: 20 20 9e      .   
    stx zp_var_type                                                   ; 9d26: 86 27       .'    
    tay                                                               ; 9d28: a8          .     
    jsr sub_c92fd                                                     ; 9d29: 20 fd 92     ..   
; &9d2c referenced 1 time by &9d1a
.c9d2c
    jsr sub_cbd7e                                                     ; 9d2c: 20 7e bd     ~.   
    jsr fwa_mul_var                                                   ; 9d2f: 20 56 a6     V.   
    lda #&ff                                                          ; 9d32: a9 ff       ..    
    ldx zp_var_type                                                   ; 9d34: a6 27       .'    
    jmp c9dd4                                                         ; 9d36: 4c d4 9d    L..   
; &9d39 referenced 2 times by &9d3d, &9d58
.c9d39
    jmp c8c0e                                                         ; 9d39: 4c 0e 8c    L..   
; &9d3c referenced 1 time by &9dcb
.c9d3c
    tay                                                               ; 9d3c: a8          .     
    beq c9d39                                                         ; 9d3d: f0 fa       ..    
    bmi loop_c9d20                                                    ; 9d3f: 30 df       0.    
    lda zp_iwa_3                                                      ; 9d41: a5 2d       .-    
    cmp zp_iwa_2                                                      ; 9d43: c5 2c       .,    
    bne c9d1d                                                         ; 9d45: d0 d6       ..    
    tay                                                               ; 9d47: a8          .     
    beq c9d4e                                                         ; 9d48: f0 04       ..    
    cmp #&ff                                                          ; 9d4a: c9 ff       ..    
    bne c9d1d                                                         ; 9d4c: d0 cf       ..    
; &9d4e referenced 1 time by &9d48
.c9d4e
    eor zp_iwa_1                                                      ; 9d4e: 45 2b       E+    
    bmi c9d1d                                                         ; 9d50: 30 cb       0.    
    jsr sub_c9e1d                                                     ; 9d52: 20 1d 9e     ..   
    stx zp_var_type                                                   ; 9d55: 86 27       .'    
    tay                                                               ; 9d57: a8          .     
    beq c9d39                                                         ; 9d58: f0 df       ..    
    bmi loop_c9d11                                                    ; 9d5a: 30 b5       0.    
    lda zp_iwa_3                                                      ; 9d5c: a5 2d       .-    
    cmp zp_iwa_2                                                      ; 9d5e: c5 2c       .,    
    bne c9d0e                                                         ; 9d60: d0 ac       ..    
    tay                                                               ; 9d62: a8          .     
    beq c9d69                                                         ; 9d63: f0 04       ..    
    cmp #&ff                                                          ; 9d65: c9 ff       ..    
    bne c9d0e                                                         ; 9d67: d0 a5       ..    
; &9d69 referenced 1 time by &9d63
.c9d69
    eor zp_iwa_1                                                      ; 9d69: 45 2b       E+    
    bmi c9d0e                                                         ; 9d6b: 30 a1       0.    
; ***************************************************************************************
; Integer multiply
;
; IWA = IWA * the stacked operand. A product wider than &FFFF is truncated to 16
; significant bits.
;
; On Entry:
;     ZP_IWA (&2A): one factor
;     (ZP_STACK_PTR) (&04): the other factor on the BASIC stack
;     ZP_VAR_TYPE (&27): 4
;
; On Exit:
;     ZP_IWA: the product
.iwa_mul
    lda zp_iwa_3                                                      ; 9d6d: a5 2d       .-    
    pha                                                               ; 9d6f: 48          H     
    jsr iwa_abs                                                       ; 9d70: 20 71 ad     q.   
    ldx #&39 ; '9'                                                    ; 9d73: a2 39       .9    
    jsr iwa_store_zp                                                  ; 9d75: 20 44 be     D.   
    jsr unstack_integer                                               ; 9d78: 20 ea bd     ..   
    pla                                                               ; 9d7b: 68          h     
    eor zp_iwa_3                                                      ; 9d7c: 45 2d       E-    
    sta zp_general                                                    ; 9d7e: 85 37       .7    
    jsr iwa_abs                                                       ; 9d80: 20 71 ad     q.   
    ldy #0                                                            ; 9d83: a0 00       ..    
    ldx #0                                                            ; 9d85: a2 00       ..    
    sty zp_fwb_m2                                                     ; 9d87: 84 3f       .?    
    sty zp_fwb_m3                                                     ; 9d89: 84 40       .@    
; &9d8b referenced 1 time by &9db2
.loop_c9d8b
    lsr l003a                                                         ; 9d8b: 46 3a       F:    
    ror zp_fileblk                                                    ; 9d8d: 66 39       f9    
    bcc c9da6                                                         ; 9d8f: 90 15       ..    
    clc                                                               ; 9d91: 18          .     
    tya                                                               ; 9d92: 98          .     
    adc zp_iwa                                                        ; 9d93: 65 2a       e*    
    tay                                                               ; 9d95: a8          .     
    txa                                                               ; 9d96: 8a          .     
    adc zp_iwa_1                                                      ; 9d97: 65 2b       e+    
    tax                                                               ; 9d99: aa          .     
    lda zp_fwb_m2                                                     ; 9d9a: a5 3f       .?    
    adc zp_iwa_2                                                      ; 9d9c: 65 2c       e,    
    sta zp_fwb_m2                                                     ; 9d9e: 85 3f       .?    
    lda zp_fwb_m3                                                     ; 9da0: a5 40       .@    
    adc zp_iwa_3                                                      ; 9da2: 65 2d       e-    
    sta zp_fwb_m3                                                     ; 9da4: 85 40       .@    
; &9da6 referenced 1 time by &9d8f
.c9da6
    asl zp_iwa                                                        ; 9da6: 06 2a       .*    
    rol zp_iwa_1                                                      ; 9da8: 26 2b       &+    
    rol zp_iwa_2                                                      ; 9daa: 26 2c       &,    
    rol zp_iwa_3                                                      ; 9dac: 26 2d       &-    
    lda zp_fileblk                                                    ; 9dae: a5 39       .9    
    ora l003a                                                         ; 9db0: 05 3a       .:    
    bne loop_c9d8b                                                    ; 9db2: d0 d7       ..    
    sty zp_fwb_exp                                                    ; 9db4: 84 3d       .=    
    stx zp_fwb_m1                                                     ; 9db6: 86 3e       .>    
    lda zp_general                                                    ; 9db8: a5 37       .7    
    php                                                               ; 9dba: 08          .     
; &9dbb referenced 1 time by &9e07
.c9dbb
    ldx #&3d ; '='                                                    ; 9dbb: a2 3d       .=    
; &9dbd referenced 1 time by &9e1a
.c9dbd
    jsr iwa_load_zp                                                   ; 9dbd: 20 56 af     V.   
    plp                                                               ; 9dc0: 28          (     
    bpl c9dc6                                                         ; 9dc1: 10 03       ..    
    jsr iwa_negate                                                    ; 9dc3: 20 93 ad     ..   
; &9dc6 referenced 1 time by &9dc1
.c9dc6
    ldx zp_var_type                                                   ; 9dc6: a6 27       .'    
    jmp c9dd4                                                         ; 9dc8: 4c d4 9d    L..   
; &9dcb referenced 1 time by &9dd6
.loop_c9dcb
    jmp c9d3c                                                         ; 9dcb: 4c 3c 9d    L<.   
; &9dce referenced 2 times by &9c53, &9cba
.sub_c9dce
    jsr stack_integer                                                 ; 9dce: 20 94 bd     ..   
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
    beq iwa_mod                                                       ; 9dde: f0 21       .!    
    cpx #&81                                                          ; 9de0: e0 81       ..    
    beq iwa_div                                                       ; 9de2: f0 26       .&    
    rts                                                               ; 9de4: 60          `     
; &9de5 referenced 1 time by &9dda
.c9de5
    tay                                                               ; 9de5: a8          .     
    jsr sub_c92fd                                                     ; 9de6: 20 fd 92     ..   
    jsr stack_real                                                    ; 9de9: 20 51 bd     Q.   
    jsr sub_c9e20                                                     ; 9dec: 20 20 9e      .   
    stx zp_var_type                                                   ; 9def: 86 27       .'    
    tay                                                               ; 9df1: a8          .     
    jsr sub_c92fd                                                     ; 9df2: 20 fd 92     ..   
    jsr sub_cbd7e                                                     ; 9df5: 20 7e bd     ~.   
    jsr fwa_rdiv_var                                                  ; 9df8: 20 ad a6     ..   
    ldx zp_var_type                                                   ; 9dfb: a6 27       .'    
    lda #&ff                                                          ; 9dfd: a9 ff       ..    
    bne c9dd4                                                         ; 9dff: d0 d3       ..    
; ***************************************************************************************
; Integer remainder
;
; IWA = IWA MOD the integer operand. Raises "Division by zero" if the divisor is zero.
;
; On Entry:
;     ZP_IWA (&2A): the dividend
;
; On Exit:
;     ZP_IWA: the remainder
; &9e01 referenced 1 time by &9dde
.iwa_mod
    jsr sub_c99be                                                     ; 9e01: 20 be 99     ..   
    lda l0038                                                         ; 9e04: a5 38       .8    
    php                                                               ; 9e06: 08          .     
    jmp c9dbb                                                         ; 9e07: 4c bb 9d    L..   
; ***************************************************************************************
; Integer divide
;
; IWA = IWA DIV the integer operand. Raises "Division by zero" if the divisor is zero.
;
; On Entry:
;     ZP_IWA (&2A): the dividend
;
; On Exit:
;     ZP_IWA: the quotient
; &9e0a referenced 1 time by &9de2
.iwa_div
    jsr sub_c99be                                                     ; 9e0a: 20 be 99     ..   
    rol zp_fileblk                                                    ; 9e0d: 26 39       &9    
    rol l003a                                                         ; 9e0f: 26 3a       &:    
    rol zp_fwb_sign                                                   ; 9e11: 26 3b       &;    
    rol zp_fwb_ovf                                                    ; 9e13: 26 3c       &<    
    bit zp_general                                                    ; 9e15: 24 37       $7    
    php                                                               ; 9e17: 08          .     
    ldx #&39 ; '9'                                                    ; 9e18: a2 39       .9    
    jmp c9dbd                                                         ; 9e1a: 4c bd 9d    L..   
; &9e1d referenced 2 times by &99c8, &9d52
.sub_c9e1d
    jsr stack_integer                                                 ; 9e1d: 20 94 bd     ..   
; &9e20 referenced 4 times by &9c18, &9d23, &9dd1, &9dec
.sub_c9e20
    jsr eval_factor                                                   ; 9e20: 20 ec ad     ..   
; &9e23 referenced 2 times by &9e57, &9e86
.c9e23
    pha                                                               ; 9e23: 48          H     
; &9e24 referenced 1 time by &9e2c
.loop_c9e24
    ldy zp_text_ptr2_off                                              ; 9e24: a4 1b       ..    
    inc zp_text_ptr2_off                                              ; 9e26: e6 1b       ..    
    lda (zp_text_ptr2),y                                              ; 9e28: b1 19       ..    
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
    jsr stack_real                                                    ; 9e39: 20 51 bd     Q.   
    jsr sub_c92fa                                                     ; 9e3c: 20 fa 92     ..   
    lda zp_fwa_exp                                                    ; 9e3f: a5 30       .0    
    cmp #&87                                                          ; 9e41: c9 87       ..    
    bcs c9e88                                                         ; 9e43: b0 43       .C    
    jsr sub_ca486                                                     ; 9e45: 20 86 a4     ..   
    bne c9e59                                                         ; 9e48: d0 0f       ..    
    jsr sub_cbd7e                                                     ; 9e4a: 20 7e bd     ~.   
    jsr fwa_unpack_var                                                ; 9e4d: 20 b5 a3     ..   
    lda l004a                                                         ; 9e50: a5 4a       .J    
    jsr sub_cab12                                                     ; 9e52: 20 12 ab     ..   
    lda #&ff                                                          ; 9e55: a9 ff       ..    
    bne c9e23                                                         ; 9e57: d0 ca       ..    
; &9e59 referenced 1 time by &9e48
.c9e59
    jsr fwa_pack_temp3                                                ; 9e59: 20 81 a3     ..   
    lda zp_stack_ptr                                                  ; 9e5c: a5 04       ..    
    sta zp_fp_ptr                                                     ; 9e5e: 85 4b       .K    
    lda zp_stack_ptr_1                                                ; 9e60: a5 05       ..    
    sta zp_fp_ptr_1                                                   ; 9e62: 85 4c       .L    
    jsr fwa_unpack_var                                                ; 9e64: 20 b5 a3     ..   
    lda l004a                                                         ; 9e67: a5 4a       .J    
    jsr sub_cab12                                                     ; 9e69: 20 12 ab     ..   
; &9e6c referenced 1 time by &9e8e
.loop_c9e6c
    jsr fwa_pack_temp2                                                ; 9e6c: 20 7d a3     }.   
    jsr sub_cbd7e                                                     ; 9e6f: 20 7e bd     ~.   
    jsr fwa_unpack_var                                                ; 9e72: 20 b5 a3     ..   
    jsr sub_ca801                                                     ; 9e75: 20 01 a8     ..   
    jsr caad1                                                         ; 9e78: 20 d1 aa     ..   
    jsr sub_caa94                                                     ; 9e7b: 20 94 aa     ..   
    jsr sub_ca7ed                                                     ; 9e7e: 20 ed a7     ..   
    jsr fwa_mul_var                                                   ; 9e81: 20 56 a6     V.   
    lda #&ff                                                          ; 9e84: a9 ff       ..    
    bne c9e23                                                         ; 9e86: d0 9b       ..    
; &9e88 referenced 1 time by &9e43
.c9e88
    jsr fwa_pack_temp3                                                ; 9e88: 20 81 a3     ..   
    jsr fwa_set_one                                                   ; 9e8b: 20 99 a6     ..   
    bne loop_c9e6c                                                    ; 9e8e: d0 dc       ..    
; &9e90 referenced 1 time by &9f07
.loop_c9e90
    tya                                                               ; 9e90: 98          .     
    bpl c9e96                                                         ; 9e91: 10 03       ..    
    jsr fwa_to_int                                                    ; 9e93: 20 e4 a3     ..   
; &9e96 referenced 1 time by &9e91
.c9e96
    ldx #0                                                            ; 9e96: a2 00       ..    
    ldy #0                                                            ; 9e98: a0 00       ..    
; &9e9a referenced 1 time by &9eae
.loop_c9e9a
    lda zp_iwa,y                                                      ; 9e9a: b9 2a 00    .*.   
    pha                                                               ; 9e9d: 48          H     
    and #&0f                                                          ; 9e9e: 29 0f       ).    
    sta zp_fwb_m2,x                                                   ; 9ea0: 95 3f       .?    
    pla                                                               ; 9ea2: 68          h     
    lsr a                                                             ; 9ea3: 4a          J     
    lsr a                                                             ; 9ea4: 4a          J     
    lsr a                                                             ; 9ea5: 4a          J     
    lsr a                                                             ; 9ea6: 4a          J     
    inx                                                               ; 9ea7: e8          .     
    sta zp_fwb_m2,x                                                   ; 9ea8: 95 3f       .?    
    inx                                                               ; 9eaa: e8          .     
    iny                                                               ; 9eab: c8          .     
    cpy #4                                                            ; 9eac: c0 04       ..    
    bne loop_c9e9a                                                    ; 9eae: d0 ea       ..    
; &9eb0 referenced 1 time by &9eb5
.loop_c9eb0
    dex                                                               ; 9eb0: ca          .     
    beq c9eb7                                                         ; 9eb1: f0 04       ..    
    lda zp_fwb_m2,x                                                   ; 9eb3: b5 3f       .?    
    beq loop_c9eb0                                                    ; 9eb5: f0 f9       ..    
; &9eb7 referenced 2 times by &9eb1, &9ec5
.c9eb7
    lda zp_fwb_m2,x                                                   ; 9eb7: b5 3f       .?    
    cmp #&0a                                                          ; 9eb9: c9 0a       ..    
    bcc c9ebf                                                         ; 9ebb: 90 02       ..    
    adc #6                                                            ; 9ebd: 69 06       i.    
; &9ebf referenced 1 time by &9ebb
.c9ebf
    adc #&30 ; '0'                                                    ; 9ebf: 69 30       i0    
    jsr ca066                                                         ; 9ec1: 20 66 a0     f.   
    dex                                                               ; 9ec4: ca          .     
    bpl c9eb7                                                         ; 9ec5: 10 f0       ..    
    rts                                                               ; 9ec7: 60          `     
; &9ec8 referenced 1 time by &9f12
.loop_c9ec8
    bpl c9ed1                                                         ; 9ec8: 10 07       ..    
    lda #&2d ; '-'                                                    ; 9eca: a9 2d       .-    
    sta zp_fwa_sign                                                   ; 9ecc: 85 2e       ..    
    jsr ca066                                                         ; 9ece: 20 66 a0     f.   
; &9ed1 referenced 3 times by &9ec8, &9edc, &9f36
.c9ed1
    lda zp_fwa_exp                                                    ; 9ed1: a5 30       .0    
    cmp #&81                                                          ; 9ed3: c9 81       ..    
    bcs c9f25                                                         ; 9ed5: b0 4e       .N    
    jsr fwa_mul10                                                     ; 9ed7: 20 f4 a1     ..   
    dec l0049                                                         ; 9eda: c6 49       .I    
    jmp c9ed1                                                         ; 9edc: 4c d1 9e    L..   
; ***************************************************************************************
; Convert the current value to an ASCII number
;
; Convert the integer (IWA) or real (FWA) value to an ASCII string in the string work
; area, in decimal or hex per the radix flag and the @% print format. Underlies PRINT and
; STR$.
;
; On Entry:
;     ZP_PRINT_FLAG (&15): 0 for decimal, -1 for hexadecimal
;     @% (&0400): print format fields
;     Y: &FF
;
; On Exit:
;     STRING WORK AREA (&0600): the ASCII result
;     ZP_STRBUF_LEN (&36): length of the result
; &9edf referenced 2 times by &8dfb, &b0b9
.number_to_ascii
    ldx l0402                                                         ; 9edf: ae 02 04    ...   
    cpx #3                                                            ; 9ee2: e0 03       ..    
    bcc c9ee8                                                         ; 9ee4: 90 02       ..    
    ldx #0                                                            ; 9ee6: a2 00       ..    
; &9ee8 referenced 1 time by &9ee4
.c9ee8
    stx zp_general                                                    ; 9ee8: 86 37       .7    
    lda l0401                                                         ; 9eea: ad 01 04    ...   
    beq c9ef5                                                         ; 9eed: f0 06       ..    
    cmp #&0a                                                          ; 9eef: c9 0a       ..    
    bcs c9ef9                                                         ; 9ef1: b0 06       ..    
    bcc c9efb                                                         ; 9ef3: 90 06       ..    
; &9ef5 referenced 1 time by &9eed
.c9ef5
    cpx #2                                                            ; 9ef5: e0 02       ..    
    beq c9efb                                                         ; 9ef7: f0 02       ..    
; &9ef9 referenced 2 times by &9ef1, &b0b3
.c9ef9
    lda #&0a                                                          ; 9ef9: a9 0a       ..    
; &9efb referenced 2 times by &9ef3, &9ef7
.c9efb
    sta l0038                                                         ; 9efb: 85 38       .8    
    sta l004e                                                         ; 9efd: 85 4e       .N    
    lda #0                                                            ; 9eff: a9 00       ..    
    sta zp_strbuf_len                                                 ; 9f01: 85 36       .6    
    sta l0049                                                         ; 9f03: 85 49       .I    
    bit zp_print_flag                                                 ; 9f05: 24 15       $.    
    bmi loop_c9e90                                                    ; 9f07: 30 87       0.    
    tya                                                               ; 9f09: 98          .     
    bmi c9f0f                                                         ; 9f0a: 30 03       0.    
    jsr int_to_fwa                                                    ; 9f0c: 20 be a2     ..   
; &9f0f referenced 1 time by &9f0a
.c9f0f
    jsr fwa_sign                                                      ; 9f0f: 20 da a1     ..   
    bne loop_c9ec8                                                    ; 9f12: d0 b4       ..    
    lda zp_general                                                    ; 9f14: a5 37       .7    
    bne c9f1d                                                         ; 9f16: d0 05       ..    
    lda #&30 ; '0'                                                    ; 9f18: a9 30       .0    
    jmp ca066                                                         ; 9f1a: 4c 66 a0    Lf.   
; &9f1d referenced 1 time by &9f16
.c9f1d
    jmp c9f9c                                                         ; 9f1d: 4c 9c 9f    L..   
; &9f20 referenced 1 time by &9f96
.loop_c9f20
    jsr fwa_set_one                                                   ; 9f20: 20 99 a6     ..   
    bne c9f34                                                         ; 9f23: d0 0f       ..    
; &9f25 referenced 1 time by &9ed5
.c9f25
    cmp #&84                                                          ; 9f25: c9 84       ..    
    bcc c9f39                                                         ; 9f27: 90 10       ..    
    bne c9f31                                                         ; 9f29: d0 06       ..    
    lda zp_fwa_m1                                                     ; 9f2b: a5 31       .1    
    cmp #&a0                                                          ; 9f2d: c9 a0       ..    
    bcc c9f39                                                         ; 9f2f: 90 08       ..    
; &9f31 referenced 1 time by &9f29
.c9f31
    jsr fwa_div10                                                     ; 9f31: 20 4d a2     M.   
; &9f34 referenced 1 time by &9f23
.c9f34
    inc l0049                                                         ; 9f34: e6 49       .I    
    jmp c9ed1                                                         ; 9f36: 4c d1 9e    L..   
; &9f39 referenced 2 times by &9f27, &9f2f
.c9f39
    lda zp_fwa_rnd                                                    ; 9f39: a5 35       .5    
    sta zp_var_type                                                   ; 9f3b: 85 27       .'    
    jsr fwa_pack_temp1                                                ; 9f3d: 20 85 a3     ..   
    lda l004e                                                         ; 9f40: a5 4e       .N    
    sta l0038                                                         ; 9f42: 85 38       .8    
    ldx zp_general                                                    ; 9f44: a6 37       .7    
    cpx #2                                                            ; 9f46: e0 02       ..    
    bne c9f5c                                                         ; 9f48: d0 12       ..    
    adc l0049                                                         ; 9f4a: 65 49       eI    
    bmi c9fa0                                                         ; 9f4c: 30 52       0R    
    sta l0038                                                         ; 9f4e: 85 38       .8    
    cmp #&0b                                                          ; 9f50: c9 0b       ..    
    bcc c9f5c                                                         ; 9f52: 90 08       ..    
    lda #&0a                                                          ; 9f54: a9 0a       ..    
    sta l0038                                                         ; 9f56: 85 38       .8    
    lda #0                                                            ; 9f58: a9 00       ..    
    sta zp_general                                                    ; 9f5a: 85 37       .7    
; &9f5c referenced 2 times by &9f48, &9f52
.c9f5c
    jsr fwa_clear                                                     ; 9f5c: 20 86 a6     ..   
    lda #&a0                                                          ; 9f5f: a9 a0       ..    
    sta zp_fwa_m1                                                     ; 9f61: 85 31       .1    
    lda #&83                                                          ; 9f63: a9 83       ..    
    sta zp_fwa_exp                                                    ; 9f65: 85 30       .0    
    ldx l0038                                                         ; 9f67: a6 38       .8    
    beq c9f71                                                         ; 9f69: f0 06       ..    
; &9f6b referenced 1 time by &9f6f
.loop_c9f6b
    jsr fwa_div10                                                     ; 9f6b: 20 4d a2     M.   
    dex                                                               ; 9f6e: ca          .     
    bne loop_c9f6b                                                    ; 9f6f: d0 fa       ..    
; &9f71 referenced 1 time by &9f69
.c9f71
    jsr sub_ca7f5                                                     ; 9f71: 20 f5 a7     ..   
    jsr fwb_unpack_var                                                ; 9f74: 20 4e a3     N.   
    lda zp_var_type                                                   ; 9f77: a5 27       .'    
    sta zp_fwb_rnd                                                    ; 9f79: 85 42       .B    
    jsr fwa_add_fwb_raw                                               ; 9f7b: 20 0b a5     ..   
; &9f7e referenced 1 time by &9f90
.loop_c9f7e
    lda zp_fwa_exp                                                    ; 9f7e: a5 30       .0    
    cmp #&84                                                          ; 9f80: c9 84       ..    
    bcs c9f92                                                         ; 9f82: b0 0e       ..    
    ror zp_fwa_m1                                                     ; 9f84: 66 31       f1    
    ror zp_fwa_m2                                                     ; 9f86: 66 32       f2    
    ror zp_fwa_m3                                                     ; 9f88: 66 33       f3    
    ror zp_fwa_m4                                                     ; 9f8a: 66 34       f4    
    ror zp_fwa_rnd                                                    ; 9f8c: 66 35       f5    
    inc zp_fwa_exp                                                    ; 9f8e: e6 30       .0    
    bne loop_c9f7e                                                    ; 9f90: d0 ec       ..    
; &9f92 referenced 1 time by &9f82
.c9f92
    lda zp_fwa_m1                                                     ; 9f92: a5 31       .1    
    cmp #&a0                                                          ; 9f94: c9 a0       ..    
    bcs loop_c9f20                                                    ; 9f96: b0 88       ..    
    lda l0038                                                         ; 9f98: a5 38       .8    
    bne c9fad                                                         ; 9f9a: d0 11       ..    
; &9f9c referenced 1 time by &9f1d
.c9f9c
    cmp #1                                                            ; 9f9c: c9 01       ..    
    beq c9fe6                                                         ; 9f9e: f0 46       .F    
; &9fa0 referenced 1 time by &9f4c
.c9fa0
    jsr fwa_clear                                                     ; 9fa0: 20 86 a6     ..   
    lda #0                                                            ; 9fa3: a9 00       ..    
    sta l0049                                                         ; 9fa5: 85 49       .I    
    lda l004e                                                         ; 9fa7: a5 4e       .N    
    sta l0038                                                         ; 9fa9: 85 38       .8    
    inc l0038                                                         ; 9fab: e6 38       .8    
; &9fad referenced 1 time by &9f9a
.c9fad
    lda #1                                                            ; 9fad: a9 01       ..    
    cmp zp_general                                                    ; 9faf: c5 37       .7    
    beq c9fe6                                                         ; 9fb1: f0 33       .3    
    ldy l0049                                                         ; 9fb3: a4 49       .I    
    bmi c9fc3                                                         ; 9fb5: 30 0c       0.    
    cpy l0038                                                         ; 9fb7: c4 38       .8    
    bcs c9fe6                                                         ; 9fb9: b0 2b       .+    
    lda #0                                                            ; 9fbb: a9 00       ..    
    sta l0049                                                         ; 9fbd: 85 49       .I    
    iny                                                               ; 9fbf: c8          .     
    tya                                                               ; 9fc0: 98          .     
    bne c9fe6                                                         ; 9fc1: d0 23       .#    
; &9fc3 referenced 1 time by &9fb5
.c9fc3
    lda zp_general                                                    ; 9fc3: a5 37       .7    
    cmp #2                                                            ; 9fc5: c9 02       ..    
    beq c9fcf                                                         ; 9fc7: f0 06       ..    
    lda #1                                                            ; 9fc9: a9 01       ..    
    cpy #&ff                                                          ; 9fcb: c0 ff       ..    
    bne c9fe6                                                         ; 9fcd: d0 17       ..    
; &9fcf referenced 1 time by &9fc7
.c9fcf
    lda #&30 ; '0'                                                    ; 9fcf: a9 30       .0    
    jsr ca066                                                         ; 9fd1: 20 66 a0     f.   
    lda #&2e ; '.'                                                    ; 9fd4: a9 2e       ..    
    jsr ca066                                                         ; 9fd6: 20 66 a0     f.   
    lda #&30 ; '0'                                                    ; 9fd9: a9 30       .0    
; &9fdb referenced 1 time by &9fe2
.loop_c9fdb
    inc l0049                                                         ; 9fdb: e6 49       .I    
    beq c9fe4                                                         ; 9fdd: f0 05       ..    
    jsr ca066                                                         ; 9fdf: 20 66 a0     f.   
    bne loop_c9fdb                                                    ; 9fe2: d0 f7       ..    
; &9fe4 referenced 1 time by &9fdd
.c9fe4
    lda #&80                                                          ; 9fe4: a9 80       ..    
; &9fe6 referenced 5 times by &9f9e, &9fb1, &9fb9, &9fc1, &9fcd
.c9fe6
    sta l004e                                                         ; 9fe6: 85 4e       .N    
; &9fe8 referenced 1 time by &9ff6
.loop_c9fe8
    jsr sub_ca040                                                     ; 9fe8: 20 40 a0     @.   
    dec l004e                                                         ; 9feb: c6 4e       .N    
    bne c9ff4                                                         ; 9fed: d0 05       ..    
    lda #&2e ; '.'                                                    ; 9fef: a9 2e       ..    
    jsr ca066                                                         ; 9ff1: 20 66 a0     f.   
; &9ff4 referenced 1 time by &9fed
.c9ff4
    dec l0038                                                         ; 9ff4: c6 38       .8    
    bne loop_c9fe8                                                    ; 9ff6: d0 f0       ..    
    ldy zp_general                                                    ; 9ff8: a4 37       .7    
    dey                                                               ; 9ffa: 88          .     
    beq ca015                                                         ; 9ffb: f0 18       ..    
    dey                                                               ; 9ffd: 88          .     
    beq ca011                                                         ; 9ffe: f0 11       ..    
    ldy zp_strbuf_len                                                 ; a000: a4 36       .6    
; &a002 referenced 1 time by &a008
.loop_ca002
    dey                                                               ; a002: 88          .     
    lda string_work,y                                                 ; a003: b9 00 06    ...   
    cmp #&30 ; '0'                                                    ; a006: c9 30       .0    
    beq loop_ca002                                                    ; a008: f0 f8       ..    
    cmp #&2e ; '.'                                                    ; a00a: c9 2e       ..    
    beq ca00f                                                         ; a00c: f0 01       ..    
    iny                                                               ; a00e: c8          .     
; &a00f referenced 1 time by &a00c
.ca00f
    sty zp_strbuf_len                                                 ; a00f: 84 36       .6    
; &a011 referenced 1 time by &9ffe
.ca011
    lda l0049                                                         ; a011: a5 49       .I    
    beq return_19                                                     ; a013: f0 2a       .*    
; &a015 referenced 1 time by &9ffb
.ca015
    lda #&45 ; 'E'                                                    ; a015: a9 45       .E    
    jsr ca066                                                         ; a017: 20 66 a0     f.   
    lda l0049                                                         ; a01a: a5 49       .I    
    bpl ca028                                                         ; a01c: 10 0a       ..    
    lda #&2d ; '-'                                                    ; a01e: a9 2d       .-    
    jsr ca066                                                         ; a020: 20 66 a0     f.   
    sec                                                               ; a023: 38          8     
    lda #0                                                            ; a024: a9 00       ..    
    sbc l0049                                                         ; a026: e5 49       .I    
; &a028 referenced 1 time by &a01c
.ca028
    jsr sub_ca052                                                     ; a028: 20 52 a0     R.   
    lda zp_general                                                    ; a02b: a5 37       .7    
    beq return_19                                                     ; a02d: f0 10       ..    
    lda #&20 ; ' '                                                    ; a02f: a9 20       .     
    ldy l0049                                                         ; a031: a4 49       .I    
    bmi ca038                                                         ; a033: 30 03       0.    
    jsr ca066                                                         ; a035: 20 66 a0     f.   
; &a038 referenced 1 time by &a033
.ca038
    cpx #0                                                            ; a038: e0 00       ..    
    bne return_19                                                     ; a03a: d0 03       ..    
    jmp ca066                                                         ; a03c: 4c 66 a0    Lf.   
; &a03f referenced 3 times by &a013, &a02d, &a03a
.return_19
    rts                                                               ; a03f: 60          `     
; &a040 referenced 1 time by &9fe8
.sub_ca040
    lda zp_fwa_m1                                                     ; a040: a5 31       .1    
    lsr a                                                             ; a042: 4a          J     
    lsr a                                                             ; a043: 4a          J     
    lsr a                                                             ; a044: 4a          J     
    lsr a                                                             ; a045: 4a          J     
    jsr sub_ca064                                                     ; a046: 20 64 a0     d.   
    lda zp_fwa_m1                                                     ; a049: a5 31       .1    
    and #&0f                                                          ; a04b: 29 0f       ).    
    sta zp_fwa_m1                                                     ; a04d: 85 31       .1    
    jmp ca197                                                         ; a04f: 4c 97 a1    L..   
; &a052 referenced 1 time by &a028
.sub_ca052
    ldx #&ff                                                          ; a052: a2 ff       ..    
    sec                                                               ; a054: 38          8     
; &a055 referenced 1 time by &a058
.loop_ca055
    inx                                                               ; a055: e8          .     
    sbc #&0a                                                          ; a056: e9 0a       ..    
    bcs loop_ca055                                                    ; a058: b0 fb       ..    
    adc #&0a                                                          ; a05a: 69 0a       i.    
    pha                                                               ; a05c: 48          H     
    txa                                                               ; a05d: 8a          .     
    beq ca063                                                         ; a05e: f0 03       ..    
    jsr sub_ca064                                                     ; a060: 20 64 a0     d.   
; &a063 referenced 1 time by &a05e
.ca063
    pla                                                               ; a063: 68          h     
; &a064 referenced 2 times by &a046, &a060
.sub_ca064
    ora #&30 ; '0'                                                    ; a064: 09 30       .0    
; &a066 referenced 11 times by &9ec1, &9ece, &9f1a, &9fd1, &9fd6, &9fdf, &9ff1, &a017, &a020, &a035, &a03c
.ca066
    stx zp_fwb_sign                                                   ; a066: 86 3b       .;    
    ldx zp_strbuf_len                                                 ; a068: a6 36       .6    
    sta string_work,x                                                 ; a06a: 9d 00 06    ...   
    ldx zp_fwb_sign                                                   ; a06d: a6 3b       .;    
    inc zp_strbuf_len                                                 ; a06f: e6 36       .6    
    rts                                                               ; a071: 60          `     
; &a072 referenced 2 times by &a091, &a095
.ca072
    clc                                                               ; a072: 18          .     
    stx zp_fwa_rnd                                                    ; a073: 86 35       .5    
    jsr fwa_sign                                                      ; a075: 20 da a1     ..   
    lda #&ff                                                          ; a078: a9 ff       ..    
    rts                                                               ; a07a: 60          `     
; &a07b referenced 3 times by &ac60, &ac6b, &ae2a
.sub_ca07b
    ldx #0                                                            ; a07b: a2 00       ..    
    stx zp_fwa_m1                                                     ; a07d: 86 31       .1    
    stx zp_fwa_m2                                                     ; a07f: 86 32       .2    
    stx zp_fwa_m3                                                     ; a081: 86 33       .3    
    stx zp_fwa_m4                                                     ; a083: 86 34       .4    
    stx zp_fwa_rnd                                                    ; a085: 86 35       .5    
    stx l0048                                                         ; a087: 86 48       .H    
    stx l0049                                                         ; a089: 86 49       .I    
    cmp #&2e ; '.'                                                    ; a08b: c9 2e       ..    
    beq ca0a0                                                         ; a08d: f0 11       ..    
    cmp #&3a ; ':'                                                    ; a08f: c9 3a       .:    
    bcs ca072                                                         ; a091: b0 df       ..    
    sbc #&2f ; '/'                                                    ; a093: e9 2f       ./    
    bmi ca072                                                         ; a095: 30 db       0.    
    sta zp_fwa_rnd                                                    ; a097: 85 35       .5    
; &a099 referenced 8 times by &a0a6, &a0bc, &a0c0, &a0cf, &a0d3, &a0d7, &a0db, &a0df
.ca099
    iny                                                               ; a099: c8          .     
    lda (zp_text_ptr2),y                                              ; a09a: b1 19       ..    
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
    ldx zp_fwa_m1                                                     ; a0b4: a6 31       .1    
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
    jsr ca197                                                         ; a0c8: 20 97 a1     ..   
    adc zp_fwa_rnd                                                    ; a0cb: 65 35       e5    
    sta zp_fwa_rnd                                                    ; a0cd: 85 35       .5    
    bcc ca099                                                         ; a0cf: 90 c8       ..    
    inc zp_fwa_m4                                                     ; a0d1: e6 34       .4    
    bne ca099                                                         ; a0d3: d0 c4       ..    
    inc zp_fwa_m3                                                     ; a0d5: e6 33       .3    
    bne ca099                                                         ; a0d7: d0 c0       ..    
    inc zp_fwa_m2                                                     ; a0d9: e6 32       .2    
    bne ca099                                                         ; a0db: d0 bc       ..    
    inc zp_fwa_m1                                                     ; a0dd: e6 31       .1    
    bne ca099                                                         ; a0df: d0 b8       ..    
; &a0e1 referenced 1 time by &a0aa
.ca0e1
    jsr sub_ca140                                                     ; a0e1: 20 40 a1     @.   
    adc l0049                                                         ; a0e4: 65 49       eI    
    sta l0049                                                         ; a0e6: 85 49       .I    
; &a0e8 referenced 3 times by &a0a2, &a0ae, &a0b2
.ca0e8
    sty zp_text_ptr2_off                                              ; a0e8: 84 1b       ..    
    lda l0049                                                         ; a0ea: a5 49       .I    
    ora l0048                                                         ; a0ec: 05 48       .H    
    beq ca11f                                                         ; a0ee: f0 2f       ./    
    jsr fwa_sign                                                      ; a0f0: 20 da a1     ..   
    beq ca11b                                                         ; a0f3: f0 26       .&    
; &a0f5 referenced 1 time by &a127
.loop_ca0f5
    lda #&a8                                                          ; a0f5: a9 a8       ..    
    sta zp_fwa_exp                                                    ; a0f7: 85 30       .0    
    lda #0                                                            ; a0f9: a9 00       ..    
    sta zp_fwa_ovf                                                    ; a0fb: 85 2f       ./    
    sta zp_fwa_sign                                                   ; a0fd: 85 2e       ..    
    jsr fwa_normalise                                                 ; a0ff: 20 03 a3     ..   
    lda l0049                                                         ; a102: a5 49       .I    
    bmi ca111                                                         ; a104: 30 0b       0.    
    beq ca118                                                         ; a106: f0 10       ..    
; &a108 referenced 1 time by &a10d
.loop_ca108
    jsr fwa_mul10                                                     ; a108: 20 f4 a1     ..   
    dec l0049                                                         ; a10b: c6 49       .I    
    bne loop_ca108                                                    ; a10d: d0 f9       ..    
    beq ca118                                                         ; a10f: f0 07       ..    
; &a111 referenced 2 times by &a104, &a116
.ca111
    jsr fwa_div10                                                     ; a111: 20 4d a2     M.   
    inc l0049                                                         ; a114: e6 49       .I    
    bne ca111                                                         ; a116: d0 f9       ..    
; &a118 referenced 2 times by &a106, &a10f
.ca118
    jsr fwa_round                                                     ; a118: 20 5c a6     \.   
; &a11b referenced 1 time by &a0f3
.ca11b
    sec                                                               ; a11b: 38          8     
    lda #&ff                                                          ; a11c: a9 ff       ..    
    rts                                                               ; a11e: 60          `     
; &a11f referenced 1 time by &a0ee
.ca11f
    lda zp_fwa_m2                                                     ; a11f: a5 32       .2    
    sta zp_iwa_3                                                      ; a121: 85 2d       .-    
    and #&80                                                          ; a123: 29 80       ).    
    ora zp_fwa_m1                                                     ; a125: 05 31       .1    
    bne loop_ca0f5                                                    ; a127: d0 cc       ..    
    lda zp_fwa_rnd                                                    ; a129: a5 35       .5    
    sta zp_iwa                                                        ; a12b: 85 2a       .*    
    lda zp_fwa_m4                                                     ; a12d: a5 34       .4    
    sta zp_iwa_1                                                      ; a12f: 85 2b       .+    
    lda zp_fwa_m3                                                     ; a131: a5 33       .3    
    sta zp_iwa_2                                                      ; a133: 85 2c       .,    
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
    lda (zp_text_ptr2),y                                              ; a141: b1 19       ..    
    cmp #&2d ; '-'                                                    ; a143: c9 2d       .-    
    beq loop_ca139                                                    ; a145: f0 f2       ..    
    cmp #&2b ; '+'                                                    ; a147: c9 2b       .+    
    bne ca14e                                                         ; a149: d0 03       ..    
; &a14b referenced 1 time by &a139
.sub_ca14b
    iny                                                               ; a14b: c8          .     
    lda (zp_text_ptr2),y                                              ; a14c: b1 19       ..    
; &a14e referenced 1 time by &a149
.ca14e
    cmp #&3a ; ':'                                                    ; a14e: c9 3a       .:    
    bcs ca174                                                         ; a150: b0 22       ."    
    sbc #&2f ; '/'                                                    ; a152: e9 2f       ./    
    bcc ca174                                                         ; a154: 90 1e       ..    
    sta l004a                                                         ; a156: 85 4a       .J    
    iny                                                               ; a158: c8          .     
    lda (zp_text_ptr2),y                                              ; a159: b1 19       ..    
    cmp #&3a ; ':'                                                    ; a15b: c9 3a       .:    
    bcs ca170                                                         ; a15d: b0 11       ..    
    sbc #&2f ; '/'                                                    ; a15f: e9 2f       ./    
    bcc ca170                                                         ; a161: 90 0d       ..    
    iny                                                               ; a163: c8          .     
    sta zp_fp_temp                                                    ; a164: 85 43       .C    
    lda l004a                                                         ; a166: a5 4a       .J    
    asl a                                                             ; a168: 0a          .     
    asl a                                                             ; a169: 0a          .     
    adc l004a                                                         ; a16a: 65 4a       eJ    
    asl a                                                             ; a16c: 0a          .     
    adc zp_fp_temp                                                    ; a16d: 65 43       eC    
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
    lda zp_fwa_rnd                                                    ; a178: a5 35       .5    
    adc zp_fwb_rnd                                                    ; a17a: 65 42       eB    
    sta zp_fwa_rnd                                                    ; a17c: 85 35       .5    
    lda zp_fwa_m4                                                     ; a17e: a5 34       .4    
    adc zp_fwb_m4                                                     ; a180: 65 41       eA    
    sta zp_fwa_m4                                                     ; a182: 85 34       .4    
    lda zp_fwa_m3                                                     ; a184: a5 33       .3    
    adc zp_fwb_m3                                                     ; a186: 65 40       e@    
    sta zp_fwa_m3                                                     ; a188: 85 33       .3    
    lda zp_fwa_m2                                                     ; a18a: a5 32       .2    
    adc zp_fwb_m2                                                     ; a18c: 65 3f       e?    
    sta zp_fwa_m2                                                     ; a18e: 85 32       .2    
    lda zp_fwa_m1                                                     ; a190: a5 31       .1    
    adc zp_fwb_m1                                                     ; a192: 65 3e       e>    
    sta zp_fwa_m1                                                     ; a194: 85 31       .1    
    rts                                                               ; a196: 60          `     
; &a197 referenced 2 times by &a04f, &a0c8
.ca197
    pha                                                               ; a197: 48          H     
    ldx zp_fwa_m4                                                     ; a198: a6 34       .4    
    lda zp_fwa_m1                                                     ; a19a: a5 31       .1    
    pha                                                               ; a19c: 48          H     
    lda zp_fwa_m2                                                     ; a19d: a5 32       .2    
    pha                                                               ; a19f: 48          H     
    lda zp_fwa_m3                                                     ; a1a0: a5 33       .3    
    pha                                                               ; a1a2: 48          H     
    lda zp_fwa_rnd                                                    ; a1a3: a5 35       .5    
    asl a                                                             ; a1a5: 0a          .     
    rol zp_fwa_m4                                                     ; a1a6: 26 34       &4    
    rol zp_fwa_m3                                                     ; a1a8: 26 33       &3    
    rol zp_fwa_m2                                                     ; a1aa: 26 32       &2    
    rol zp_fwa_m1                                                     ; a1ac: 26 31       &1    
    asl a                                                             ; a1ae: 0a          .     
    rol zp_fwa_m4                                                     ; a1af: 26 34       &4    
    rol zp_fwa_m3                                                     ; a1b1: 26 33       &3    
    rol zp_fwa_m2                                                     ; a1b3: 26 32       &2    
    rol zp_fwa_m1                                                     ; a1b5: 26 31       &1    
    adc zp_fwa_rnd                                                    ; a1b7: 65 35       e5    
    sta zp_fwa_rnd                                                    ; a1b9: 85 35       .5    
    txa                                                               ; a1bb: 8a          .     
    adc zp_fwa_m4                                                     ; a1bc: 65 34       e4    
    sta zp_fwa_m4                                                     ; a1be: 85 34       .4    
    pla                                                               ; a1c0: 68          h     
    adc zp_fwa_m3                                                     ; a1c1: 65 33       e3    
    sta zp_fwa_m3                                                     ; a1c3: 85 33       .3    
    pla                                                               ; a1c5: 68          h     
    adc zp_fwa_m2                                                     ; a1c6: 65 32       e2    
    sta zp_fwa_m2                                                     ; a1c8: 85 32       .2    
    pla                                                               ; a1ca: 68          h     
    adc zp_fwa_m1                                                     ; a1cb: 65 31       e1    
    asl zp_fwa_rnd                                                    ; a1cd: 06 35       .5    
    rol zp_fwa_m4                                                     ; a1cf: 26 34       &4    
    rol zp_fwa_m3                                                     ; a1d1: 26 33       &3    
    rol zp_fwa_m2                                                     ; a1d3: 26 32       &2    
    rol a                                                             ; a1d5: 2a          *     
    sta zp_fwa_m1                                                     ; a1d6: 85 31       .1    
    pla                                                               ; a1d8: 68          h     
    rts                                                               ; a1d9: 60          `     
; ***************************************************************************************
; Get the sign of the FP accumulator
;
; Determine the sign of the floating-point accumulator: zero, positive or negative (Z set
; when FWA is zero). Tests the mantissa bytes (&31-&35) and the sign.
; &a1da referenced 17 times by &9f0f, &a075, &a0f0, &a405, &a48e, &a50b, &a606, &a6ad, &a6e7, &a7b7, &a801, &a8dd, &a8f0, &a90a, &ab7f, &ad77, &ad7e
.fwa_sign
    lda zp_fwa_m1                                                     ; a1da: a5 31       .1    
    ora zp_fwa_m2                                                     ; a1dc: 05 32       .2    
    ora zp_fwa_m3                                                     ; a1de: 05 33       .3    
    ora zp_fwa_m4                                                     ; a1e0: 05 34       .4    
    ora zp_fwa_rnd                                                    ; a1e2: 05 35       .5       ; FWA is zero exactly when the whole mantissa is
    beq ca1ed                                                         ; a1e4: f0 07       ..       ; zero (a normalised non-zero value has bit 7 set)
    lda zp_fwa_sign                                                   ; a1e6: a5 2e       ..       ; Non-zero: the sign lives in bit 7 of the sign byte
    bne return_20                                                     ; a1e8: d0 09       ..    
    lda #1                                                            ; a1ea: a9 01       ..       ; Positive: return +1 (negative path returns -1)
    rts                                                               ; a1ec: 60          `     
; &a1ed referenced 1 time by &a1e4
.ca1ed
    sta zp_fwa_sign                                                   ; a1ed: 85 2e       ..    
    sta zp_fwa_exp                                                    ; a1ef: 85 30       .0    
    sta zp_fwa_ovf                                                    ; a1f1: 85 2f       ./    
; &a1f3 referenced 1 time by &a1e8
.return_20
    rts                                                               ; a1f3: 60          `     
; ***************************************************************************************
; FWA = FWA * 10
;
; Multiply FWA by ten, unnormalised and unrounded.
; &a1f4 referenced 2 times by &9ed7, &a108
.fwa_mul10
    clc                                                               ; a1f4: 18          .     
    lda zp_fwa_exp                                                    ; a1f5: a5 30       .0    
    adc #3                                                            ; a1f7: 69 03       i.    
    sta zp_fwa_exp                                                    ; a1f9: 85 30       .0    
    bcc ca1ff                                                         ; a1fb: 90 02       ..    
    inc zp_fwa_ovf                                                    ; a1fd: e6 2f       ./    
; &a1ff referenced 1 time by &a1fb
.ca1ff
    jsr fwb_copy_from_fwa                                             ; a1ff: 20 1e a2     ..   
    jsr sub_ca242                                                     ; a202: 20 42 a2     B.   
    jsr sub_ca242                                                     ; a205: 20 42 a2     B.   
; &a208 referenced 5 times by &a25b, &a26a, &a284, &a29c, &a5e0
.ca208
    jsr sub_ca178                                                     ; a208: 20 78 a1     x.   
; &a20b referenced 1 time by &a2ba
.ca20b
    bcc return_21                                                     ; a20b: 90 10       ..    
    ror zp_fwa_m1                                                     ; a20d: 66 31       f1    
    ror zp_fwa_m2                                                     ; a20f: 66 32       f2    
    ror zp_fwa_m3                                                     ; a211: 66 33       f3    
    ror zp_fwa_m4                                                     ; a213: 66 34       f4    
    ror zp_fwa_rnd                                                    ; a215: 66 35       f5    
    inc zp_fwa_exp                                                    ; a217: e6 30       .0    
    bne return_21                                                     ; a219: d0 02       ..    
    inc zp_fwa_ovf                                                    ; a21b: e6 2f       ./    
; &a21d referenced 2 times by &a20b, &a219
.return_21
    rts                                                               ; a21d: 60          `     
; ***************************************************************************************
; FWB = FWA
;
; Copy FWA into FWB.
; &a21e referenced 5 times by &9a44, &a1ff, &a23f, &a3f8, &a6b2
.fwb_copy_from_fwa
    lda zp_fwa_sign                                                   ; a21e: a5 2e       ..    
    sta zp_fwb_sign                                                   ; a220: 85 3b       .;    
    lda zp_fwa_ovf                                                    ; a222: a5 2f       ./    
    sta zp_fwb_ovf                                                    ; a224: 85 3c       .<    
    lda zp_fwa_exp                                                    ; a226: a5 30       .0    
    sta zp_fwb_exp                                                    ; a228: 85 3d       .=    
    lda zp_fwa_m1                                                     ; a22a: a5 31       .1    
    sta zp_fwb_m1                                                     ; a22c: 85 3e       .>    
    lda zp_fwa_m2                                                     ; a22e: a5 32       .2    
    sta zp_fwb_m2                                                     ; a230: 85 3f       .?    
    lda zp_fwa_m3                                                     ; a232: a5 33       .3    
    sta zp_fwb_m3                                                     ; a234: 85 40       .@    
    lda zp_fwa_m4                                                     ; a236: a5 34       .4    
    sta zp_fwb_m4                                                     ; a238: 85 41       .A    
    lda zp_fwa_rnd                                                    ; a23a: a5 35       .5    
    sta zp_fwb_rnd                                                    ; a23c: 85 42       .B    
    rts                                                               ; a23e: 60          `     
; &a23f referenced 2 times by &a258, &a25e
.sub_ca23f
    jsr fwb_copy_from_fwa                                             ; a23f: 20 1e a2     ..   
; &a242 referenced 5 times by &a202, &a205, &a261, &a264, &a267
.sub_ca242
    lsr zp_fwb_m1                                                     ; a242: 46 3e       F>    
    ror zp_fwb_m2                                                     ; a244: 66 3f       f?    
    ror zp_fwb_m3                                                     ; a246: 66 40       f@    
    ror zp_fwb_m4                                                     ; a248: 66 41       fA    
    ror zp_fwb_rnd                                                    ; a24a: 66 42       fB    
    rts                                                               ; a24c: 60          `     
; ***************************************************************************************
; FWA = FWA / 10
;
; Divide FWA by ten, unnormalised and unrounded.
; &a24d referenced 3 times by &9f31, &9f6b, &a111
.fwa_div10
    sec                                                               ; a24d: 38          8     
    lda zp_fwa_exp                                                    ; a24e: a5 30       .0    
    sbc #4                                                            ; a250: e9 04       ..    
    sta zp_fwa_exp                                                    ; a252: 85 30       .0    
    bcs ca258                                                         ; a254: b0 02       ..    
    dec zp_fwa_ovf                                                    ; a256: c6 2f       ./    
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
    sta zp_fwb_m1                                                     ; a26f: 85 3e       .>    
    lda zp_fwa_m1                                                     ; a271: a5 31       .1    
    sta zp_fwb_m2                                                     ; a273: 85 3f       .?    
    lda zp_fwa_m2                                                     ; a275: a5 32       .2    
    sta zp_fwb_m3                                                     ; a277: 85 40       .@    
    lda zp_fwa_m3                                                     ; a279: a5 33       .3    
    sta zp_fwb_m4                                                     ; a27b: 85 41       .A    
    lda zp_fwa_m4                                                     ; a27d: a5 34       .4    
    sta zp_fwb_rnd                                                    ; a27f: 85 42       .B    
    lda zp_fwa_rnd                                                    ; a281: a5 35       .5    
    rol a                                                             ; a283: 2a          *     
    jsr ca208                                                         ; a284: 20 08 a2     ..   
    lda #0                                                            ; a287: a9 00       ..    
    sta zp_fwb_m1                                                     ; a289: 85 3e       .>    
    sta zp_fwb_m2                                                     ; a28b: 85 3f       .?    
    lda zp_fwa_m1                                                     ; a28d: a5 31       .1    
    sta zp_fwb_m3                                                     ; a28f: 85 40       .@    
    lda zp_fwa_m2                                                     ; a291: a5 32       .2    
    sta zp_fwb_m4                                                     ; a293: 85 41       .A    
    lda zp_fwa_m3                                                     ; a295: a5 33       .3    
    sta zp_fwb_rnd                                                    ; a297: 85 42       .B    
    lda zp_fwa_m4                                                     ; a299: a5 34       .4    
    rol a                                                             ; a29b: 2a          *     
    jsr ca208                                                         ; a29c: 20 08 a2     ..   
    lda zp_fwa_m2                                                     ; a29f: a5 32       .2    
    rol a                                                             ; a2a1: 2a          *     
    lda zp_fwa_m1                                                     ; a2a2: a5 31       .1    
; ***************************************************************************************
; Add to the rounding byte and ripple the carry up
;
; Add A to the FWA rounding byte, then propagate any carry up through the mantissa (m4 ->
; m1). A carry out of the top renormalises the exponent (and may overflow). Used to round
; the mantissa up.
; &a2a4 referenced 1 time by &a666
.fwa_round_carry
    adc zp_fwa_rnd                                                    ; a2a4: 65 35       e5    
    sta zp_fwa_rnd                                                    ; a2a6: 85 35       .5    
    bcc return_22                                                     ; a2a8: 90 13       ..    
    inc zp_fwa_m4                                                     ; a2aa: e6 34       .4    
    bne return_22                                                     ; a2ac: d0 0f       ..    
    inc zp_fwa_m3                                                     ; a2ae: e6 33       .3    
    bne return_22                                                     ; a2b0: d0 0b       ..    
    inc zp_fwa_m2                                                     ; a2b2: e6 32       .2    
    bne return_22                                                     ; a2b4: d0 07       ..    
    inc zp_fwa_m1                                                     ; a2b6: e6 31       .1    
    bne return_22                                                     ; a2b8: d0 03       ..    
    jmp ca20b                                                         ; a2ba: 4c 0b a2    L..   
; &a2bd referenced 5 times by &a2a8, &a2ac, &a2b0, &a2b4, &a2b8
.return_22
    rts                                                               ; a2bd: 60          `     
; ***************************************************************************************
; Convert the integer accumulator to floating point
;
; Convert the integer in IWA to a real in FWA.
; &a2be referenced 12 times by &9301, &9a41, &9c98, &9caf, &9cee, &9d02, &9d0e, &9d17, &9d1d, &9f0c, &af24, &b4e6
.int_to_fwa
    ldx #0                                                            ; a2be: a2 00       ..    
    stx zp_fwa_rnd                                                    ; a2c0: 86 35       .5    
    stx zp_fwa_ovf                                                    ; a2c2: 86 2f       ./    
    lda zp_iwa_3                                                      ; a2c4: a5 2d       .-    
    bpl ca2cd                                                         ; a2c6: 10 05       ..    
    jsr iwa_negate                                                    ; a2c8: 20 93 ad     ..   
    ldx #&ff                                                          ; a2cb: a2 ff       ..    
; &a2cd referenced 1 time by &a2c6
.ca2cd
    stx zp_fwa_sign                                                   ; a2cd: 86 2e       ..    
    lda zp_iwa                                                        ; a2cf: a5 2a       .*    
    sta zp_fwa_m4                                                     ; a2d1: 85 34       .4    
    lda zp_iwa_1                                                      ; a2d3: a5 2b       .+    
    sta zp_fwa_m3                                                     ; a2d5: 85 33       .3    
    lda zp_iwa_2                                                      ; a2d7: a5 2c       .,    
    sta zp_fwa_m2                                                     ; a2d9: 85 32       .2    
    lda zp_iwa_3                                                      ; a2db: a5 2d       .-    
    sta zp_fwa_m1                                                     ; a2dd: 85 31       .1    
    lda #&a0                                                          ; a2df: a9 a0       ..    
    sta zp_fwa_exp                                                    ; a2e1: 85 30       .0    
    jmp fwa_normalise                                                 ; a2e3: 4c 03 a3    L..   
; &a2e6 referenced 1 time by &a30f
.loop_ca2e6
    sta zp_fwa_sign                                                   ; a2e6: 85 2e       ..    
    sta zp_fwa_exp                                                    ; a2e8: 85 30       .0    
    sta zp_fwa_ovf                                                    ; a2ea: 85 2f       ./    
; &a2ec referenced 4 times by &a2f2, &a305, &a315, &a338
.return_23
    rts                                                               ; a2ec: 60          `     
; &a2ed referenced 1 time by &a852
.sub_ca2ed
    pha                                                               ; a2ed: 48          H     
    jsr fwa_clear                                                     ; a2ee: 20 86 a6     ..   
    pla                                                               ; a2f1: 68          h     
    beq return_23                                                     ; a2f2: f0 f8       ..    
    bpl ca2fd                                                         ; a2f4: 10 07       ..    
    sta zp_fwa_sign                                                   ; a2f6: 85 2e       ..    
    lda #0                                                            ; a2f8: a9 00       ..    
    sec                                                               ; a2fa: 38          8     
    sbc zp_fwa_sign                                                   ; a2fb: e5 2e       ..    
; &a2fd referenced 1 time by &a2f4
.ca2fd
    sta zp_fwa_m1                                                     ; a2fd: 85 31       .1    
    lda #&88                                                          ; a2ff: a9 88       ..    
    sta zp_fwa_exp                                                    ; a301: 85 30       .0    
; ***************************************************************************************
; Normalise FWA
;
; Normalise the floating-point accumulator.
; &a303 referenced 8 times by &a0ff, &a2e3, &a4b3, &a5dc, &a602, &a659, &aa0e, &af33
.fwa_normalise
    lda zp_fwa_m1                                                     ; a303: a5 31       .1    
    bmi return_23                                                     ; a305: 30 e5       0.       ; Top bit already set: nothing to do
    ora zp_fwa_m2                                                     ; a307: 05 32       .2    
    ora zp_fwa_m3                                                     ; a309: 05 33       .3    
    ora zp_fwa_m4                                                     ; a30b: 05 34       .4    
    ora zp_fwa_rnd                                                    ; a30d: 05 35       .5       ; Mantissa entirely zero: the value is zero
    beq loop_ca2e6                                                    ; a30f: f0 d5       ..    
    lda zp_fwa_exp                                                    ; a311: a5 30       .0    
; &a313 referenced 2 times by &a330, &a334
.ca313
    ldy zp_fwa_m1                                                     ; a313: a4 31       .1       ; Shift up a whole byte while the MSB byte is zero
    bmi return_23                                                     ; a315: 30 d5       0.    
    bne ca33a                                                         ; a317: d0 21       .!    
    ldx zp_fwa_m2                                                     ; a319: a6 32       .2    
    stx zp_fwa_m1                                                     ; a31b: 86 31       .1    
    ldx zp_fwa_m3                                                     ; a31d: a6 33       .3    
    stx zp_fwa_m2                                                     ; a31f: 86 32       .2    
    ldx zp_fwa_m4                                                     ; a321: a6 34       .4    
    stx zp_fwa_m3                                                     ; a323: 86 33       .3    
    ldx zp_fwa_rnd                                                    ; a325: a6 35       .5    
    stx zp_fwa_m4                                                     ; a327: 86 34       .4    
    sty zp_fwa_rnd                                                    ; a329: 84 35       .5    
    sec                                                               ; a32b: 38          8     
    sbc #8                                                            ; a32c: e9 08       ..       ; each byte shift advances the exponent by 8
    sta zp_fwa_exp                                                    ; a32e: 85 30       .0    
    bcs ca313                                                         ; a330: b0 e1       ..    
    dec zp_fwa_ovf                                                    ; a332: c6 2f       ./    
    bcc ca313                                                         ; a334: 90 dd       ..    
; &a336 referenced 2 times by &a348, &a34c
.ca336
    ldy zp_fwa_m1                                                     ; a336: a4 31       .1    
    bmi return_23                                                     ; a338: 30 b2       0.    
; &a33a referenced 1 time by &a317
.ca33a
    asl zp_fwa_rnd                                                    ; a33a: 06 35       .5       ; Then shift left one bit at a time to normalise
    rol zp_fwa_m4                                                     ; a33c: 26 34       &4    
    rol zp_fwa_m3                                                     ; a33e: 26 33       &3    
    rol zp_fwa_m2                                                     ; a340: 26 32       &2    
    rol zp_fwa_m1                                                     ; a342: 26 31       &1    
    sbc #0                                                            ; a344: e9 00       ..    
    sta zp_fwa_exp                                                    ; a346: 85 30       .0    
    bcs ca336                                                         ; a348: b0 ec       ..    
    dec zp_fwa_ovf                                                    ; a34a: c6 2f       ./    
    bcc ca336                                                         ; a34c: 90 e8       ..    
; ***************************************************************************************
; Unpack a fp variable into FWB
;
; Unpack the fp variable at (&4B/&4C) into FWB.
; &a34e referenced 7 times by &9a5f, &9f74, &a4d6, &a500, &a60b, &a6ec, &a9df
.fwb_unpack_var
    ldy #4                                                            ; a34e: a0 04       ..    
    lda (zp_fp_ptr),y                                                 ; a350: b1 4b       .K    
    sta zp_fwb_m4                                                     ; a352: 85 41       .A    
    dey                                                               ; a354: 88          .     
    lda (zp_fp_ptr),y                                                 ; a355: b1 4b       .K    
    sta zp_fwb_m3                                                     ; a357: 85 40       .@    
    dey                                                               ; a359: 88          .     
    lda (zp_fp_ptr),y                                                 ; a35a: b1 4b       .K    
    sta zp_fwb_m2                                                     ; a35c: 85 3f       .?    
    dey                                                               ; a35e: 88          .     
    lda (zp_fp_ptr),y                                                 ; a35f: b1 4b       .K    
    sta zp_fwb_sign                                                   ; a361: 85 3b       .;    
    dey                                                               ; a363: 88          .     
    sty zp_fwb_rnd                                                    ; a364: 84 42       .B    
    sty zp_fwb_ovf                                                    ; a366: 84 3c       .<    
    lda (zp_fp_ptr),y                                                 ; a368: b1 4b       .K    
    sta zp_fwb_exp                                                    ; a36a: 85 3d       .=    
    ora zp_fwb_sign                                                   ; a36c: 05 3b       .;    
    ora zp_fwb_m2                                                     ; a36e: 05 3f       .?    
    ora zp_fwb_m3                                                     ; a370: 05 40       .@    
    ora zp_fwb_m4                                                     ; a372: 05 41       .A    
    beq ca37a                                                         ; a374: f0 04       ..    
    lda zp_fwb_sign                                                   ; a376: a5 3b       .;    
    ora #&80                                                          ; a378: 09 80       ..    
; &a37a referenced 1 time by &a374
.ca37a
    sta zp_fwb_m1                                                     ; a37a: 85 3e       .>    
    rts                                                               ; a37c: 60          `     
; ***************************************************************************************
; Pack FWA into TEMP2
;
; Pack FWA into the floating-point temporary at &0471.
; &a37d referenced 2 times by &9e6c, &aa11
.fwa_pack_temp2
    lda #&71 ; 'q'                                                    ; a37d: a9 71       .q    
    bne ca387                                                         ; a37f: d0 06       ..    
; ***************************************************************************************
; Pack FWA into TEMP3
;
; Pack FWA into the floating-point temporary at &0476.
; &a381 referenced 6 times by &9e59, &9e88, &a8ea, &a93c, &a9c3, &aabe
.fwa_pack_temp3
    lda #&76 ; 'v'                                                    ; a381: a9 76       .v    
    bne ca387                                                         ; a383: d0 02       ..    
; ***************************************************************************************
; Pack FWA into TEMP1
;
; Pack FWA into the floating-point temporary at &046C.
; &a385 referenced 9 times by &8d3c, &9f3d, &a6a5, &a7be, &a84b, &a89b, &a9b1, &a9d9, &ab1f
.fwa_pack_temp1
    lda #&6c ; 'l'                                                    ; a385: a9 6c       .l    
; &a387 referenced 3 times by &a37f, &a383, &a835
.ca387
    sta zp_fp_ptr                                                     ; a387: 85 4b       .K    
    lda #4                                                            ; a389: a9 04       ..    
    sta zp_fp_ptr_1                                                   ; a38b: 85 4c       .L    
; ***************************************************************************************
; Pack FWA into a fp variable
;
; Pack FWA into the five-byte fp variable at (&4B/&4C).
; &a38d referenced 7 times by &a4d9, &a6ca, &a7cf, &a9b7, &aa20, &b860, &b882
.fwa_pack_var
    ldy #0                                                            ; a38d: a0 00       ..    
    lda zp_fwa_exp                                                    ; a38f: a5 30       .0    
    sta (zp_fp_ptr),y                                                 ; a391: 91 4b       .K    
    iny                                                               ; a393: c8          .     
    lda zp_fwa_sign                                                   ; a394: a5 2e       ..    
    and #&80                                                          ; a396: 29 80       ).       ; Isolate the sign bit
    sta zp_fwa_sign                                                   ; a398: 85 2e       ..    
    lda zp_fwa_m1                                                     ; a39a: a5 31       .1    
    and #&7f                                                          ; a39c: 29 7f       ).       ; Drop the implied leading 1 from the mantissa MSB
    ora zp_fwa_sign                                                   ; a39e: 05 2e       ..       ; and fold the sign back into its bit 7
    sta (zp_fp_ptr),y                                                 ; a3a0: 91 4b       .K    
    lda zp_fwa_m2                                                     ; a3a2: a5 32       .2    
    iny                                                               ; a3a4: c8          .     
    sta (zp_fp_ptr),y                                                 ; a3a5: 91 4b       .K    
    lda zp_fwa_m3                                                     ; a3a7: a5 33       .3    
    iny                                                               ; a3a9: c8          .     
    sta (zp_fp_ptr),y                                                 ; a3aa: 91 4b       .K    
    lda zp_fwa_m4                                                     ; a3ac: a5 34       .4    
    iny                                                               ; a3ae: c8          .     
    sta (zp_fp_ptr),y                                                 ; a3af: 91 4b       .K    
    rts                                                               ; a3b1: 60          `     
; ***************************************************************************************
; Unpack TEMP1 into FWA
;
; Unpack the floating-point temporary at &046C into FWA.
; &a3b2 referenced 2 times by &aa35, &ba36
.fwa_unpack_temp1
    jsr sub_ca7f5                                                     ; a3b2: 20 f5 a7     ..   
; ***************************************************************************************
; Unpack a floating-point variable into FWA
;
; Unpack the packed five-byte floating-point value addressed by (&4B/&4C) into the
; floating-point accumulator (FWA).
; &a3b5 referenced 10 times by &9a4a, &9e4d, &9e64, &9e72, &a6b5, &a8b2, &a901, &aa26, &aac9, &b2ea
.fwa_unpack_var
    ldy #4                                                            ; a3b5: a0 04       ..       ; Copy the packed value, exponent last
    lda (zp_fp_ptr),y                                                 ; a3b7: b1 4b       .K    
    sta zp_fwa_m4                                                     ; a3b9: 85 34       .4    
    dey                                                               ; a3bb: 88          .     
    lda (zp_fp_ptr),y                                                 ; a3bc: b1 4b       .K    
    sta zp_fwa_m3                                                     ; a3be: 85 33       .3    
    dey                                                               ; a3c0: 88          .     
    lda (zp_fp_ptr),y                                                 ; a3c1: b1 4b       .K    
    sta zp_fwa_m2                                                     ; a3c3: 85 32       .2    
    dey                                                               ; a3c5: 88          .     
    lda (zp_fp_ptr),y                                                 ; a3c6: b1 4b       .K    
    sta zp_fwa_sign                                                   ; a3c8: 85 2e       ..       ; Packed mantissa MSB holds the sign in bit 7
    dey                                                               ; a3ca: 88          .     
    lda (zp_fp_ptr),y                                                 ; a3cb: b1 4b       .K    
    sta zp_fwa_exp                                                    ; a3cd: 85 30       .0    
    sty zp_fwa_rnd                                                    ; a3cf: 84 35       .5       ; Clear the rounding and overflow bytes (Y=0)
    sty zp_fwa_ovf                                                    ; a3d1: 84 2f       ./    
    ora zp_fwa_sign                                                   ; a3d3: 05 2e       ..       ; A=exponent; OR the mantissa to test for zero
    ora zp_fwa_m2                                                     ; a3d5: 05 32       .2    
    ora zp_fwa_m3                                                     ; a3d7: 05 33       .3    
    ora zp_fwa_m4                                                     ; a3d9: 05 34       .4    
    beq ca3e1                                                         ; a3db: f0 04       ..       ; All zero: leave the mantissa MSB clear
    lda zp_fwa_sign                                                   ; a3dd: a5 2e       ..    
    ora #&80                                                          ; a3df: 09 80       ..       ; Non-zero: restore the implied leading 1
; &a3e1 referenced 1 time by &a3db
.ca3e1
    sta zp_fwa_m1                                                     ; a3e1: 85 31       .1    
    rts                                                               ; a3e3: 60          `     
; ***************************************************************************************
; Convert the FP accumulator to an integer
;
; Convert FWA to a 4-byte integer in IWA (variant 1).
; &a3e4 referenced 5 times by &92f4, &98c9, &9e93, &af36, &b4c3
.fwa_to_int
    jsr fwa_to_int2                                                   ; a3e4: 20 fe a3     ..   
; &a3e7 referenced 1 time by &ac95
.sub_ca3e7
    lda zp_fwa_m1                                                     ; a3e7: a5 31       .1    
    sta zp_iwa_3                                                      ; a3e9: 85 2d       .-    
    lda zp_fwa_m2                                                     ; a3eb: a5 32       .2    
    sta zp_iwa_2                                                      ; a3ed: 85 2c       .,    
    lda zp_fwa_m3                                                     ; a3ef: a5 33       .3    
    sta zp_iwa_1                                                      ; a3f1: 85 2b       .+    
    lda zp_fwa_m4                                                     ; a3f3: a5 34       .4    
    sta zp_iwa                                                        ; a3f5: 85 2a       .*    
    rts                                                               ; a3f7: 60          `     
; &a3f8 referenced 1 time by &a400
.loop_ca3f8
    jsr fwb_copy_from_fwa                                             ; a3f8: 20 1e a2     ..   
    jmp fwa_clear                                                     ; a3fb: 4c 86 a6    L..   
; ***************************************************************************************
; Convert the FP accumulator to an integer (variant 2)
;
; Convert FWA to a 4-byte integer in IWA (variant 2).
; &a3fe referenced 4 times by &a3e4, &a491, &a9ee, &ac82
.fwa_to_int2
    lda zp_fwa_exp                                                    ; a3fe: a5 30       .0    
    bpl loop_ca3f8                                                    ; a400: 10 f6       ..    
    jsr fwb_clear                                                     ; a402: 20 53 a4     S.   
    jsr fwa_sign                                                      ; a405: 20 da a1     ..   
    bne ca43c                                                         ; a408: d0 32       .2    
    beq ca468                                                         ; a40a: f0 5c       .\    
; &a40c referenced 2 times by &a43a, &a44e
.ca40c
    lda zp_fwa_exp                                                    ; a40c: a5 30       .0    
    cmp #&a0                                                          ; a40e: c9 a0       ..    
    bcs ca466                                                         ; a410: b0 54       .T    
    cmp #&99                                                          ; a412: c9 99       ..    
    bcs ca43c                                                         ; a414: b0 26       .&    
    adc #8                                                            ; a416: 69 08       i.    
    sta zp_fwa_exp                                                    ; a418: 85 30       .0    
    lda zp_fwb_m3                                                     ; a41a: a5 40       .@    
    sta zp_fwb_m4                                                     ; a41c: 85 41       .A    
    lda zp_fwb_m2                                                     ; a41e: a5 3f       .?    
    sta zp_fwb_m3                                                     ; a420: 85 40       .@    
    lda zp_fwb_m1                                                     ; a422: a5 3e       .>    
    sta zp_fwb_m2                                                     ; a424: 85 3f       .?    
    lda zp_fwa_m4                                                     ; a426: a5 34       .4    
    sta zp_fwb_m1                                                     ; a428: 85 3e       .>    
    lda zp_fwa_m3                                                     ; a42a: a5 33       .3    
    sta zp_fwa_m4                                                     ; a42c: 85 34       .4    
    lda zp_fwa_m2                                                     ; a42e: a5 32       .2    
    sta zp_fwa_m3                                                     ; a430: 85 33       .3    
    lda zp_fwa_m1                                                     ; a432: a5 31       .1    
    sta zp_fwa_m2                                                     ; a434: 85 32       .2    
    lda #0                                                            ; a436: a9 00       ..    
    sta zp_fwa_m1                                                     ; a438: 85 31       .1    
    beq ca40c                                                         ; a43a: f0 d0       ..    
; &a43c referenced 2 times by &a408, &a414
.ca43c
    lsr zp_fwa_m1                                                     ; a43c: 46 31       F1    
    ror zp_fwa_m2                                                     ; a43e: 66 32       f2    
    ror zp_fwa_m3                                                     ; a440: 66 33       f3    
    ror zp_fwa_m4                                                     ; a442: 66 34       f4    
    ror zp_fwb_m1                                                     ; a444: 66 3e       f>    
    ror zp_fwb_m2                                                     ; a446: 66 3f       f?    
    ror zp_fwb_m3                                                     ; a448: 66 40       f@    
    ror zp_fwb_m4                                                     ; a44a: 66 41       fA    
    inc zp_fwa_exp                                                    ; a44c: e6 30       .0    
    bne ca40c                                                         ; a44e: d0 bc       ..    
; &a450 referenced 2 times by &a466, &a4c4
.ca450
    jmp err_too_big                                                   ; a450: 4c 6c a6    Ll.   
; ***************************************************************************************
; FWB = 0
;
; Set the second floating-point accumulator to zero.
; &a453 referenced 3 times by &a402, &a814, &a93f
.fwb_clear
    lda #0                                                            ; a453: a9 00       ..    
    sta zp_fwb_sign                                                   ; a455: 85 3b       .;    
    sta zp_fwb_ovf                                                    ; a457: 85 3c       .<    
    sta zp_fwb_exp                                                    ; a459: 85 3d       .=    
    sta zp_fwb_m1                                                     ; a45b: 85 3e       .>    
    sta zp_fwb_m2                                                     ; a45d: 85 3f       .?    
    sta zp_fwb_m3                                                     ; a45f: 85 40       .@    
    sta zp_fwb_m4                                                     ; a461: 85 41       .A    
    sta zp_fwb_rnd                                                    ; a463: 85 42       .B    
    rts                                                               ; a465: 60          `     
; &a466 referenced 1 time by &a410
.ca466
    bne ca450                                                         ; a466: d0 e8       ..    
; &a468 referenced 1 time by &a40a
.ca468
    lda zp_fwa_sign                                                   ; a468: a5 2e       ..    
    bpl return_24                                                     ; a46a: 10 19       ..    
; &a46c referenced 4 times by &a4b0, &a4c7, &a4cd, &aa0b
.ca46c
    sec                                                               ; a46c: 38          8     
    lda #0                                                            ; a46d: a9 00       ..    
    sbc zp_fwa_m4                                                     ; a46f: e5 34       .4    
    sta zp_fwa_m4                                                     ; a471: 85 34       .4    
    lda #0                                                            ; a473: a9 00       ..    
    sbc zp_fwa_m3                                                     ; a475: e5 33       .3    
    sta zp_fwa_m3                                                     ; a477: 85 33       .3    
    lda #0                                                            ; a479: a9 00       ..    
    sbc zp_fwa_m2                                                     ; a47b: e5 32       .2    
    sta zp_fwa_m2                                                     ; a47d: 85 32       .2    
    lda #0                                                            ; a47f: a9 00       ..    
    sbc zp_fwa_m1                                                     ; a481: e5 31       .1    
    sta zp_fwa_m1                                                     ; a483: 85 31       .1    
; &a485 referenced 1 time by &a46a
.return_24
    rts                                                               ; a485: 60          `     
; &a486 referenced 2 times by &9e45, &aab8
.sub_ca486
    lda zp_fwa_exp                                                    ; a486: a5 30       .0    
    bmi ca491                                                         ; a488: 30 07       0.    
    lda #0                                                            ; a48a: a9 00       ..    
    sta l004a                                                         ; a48c: 85 4a       .J    
    jmp fwa_sign                                                      ; a48e: 4c da a1    L..   
; &a491 referenced 1 time by &a488
.ca491
    jsr fwa_to_int2                                                   ; a491: 20 fe a3     ..   
    lda zp_fwa_m4                                                     ; a494: a5 34       .4    
    sta l004a                                                         ; a496: 85 4a       .J    
    jsr sub_ca4e8                                                     ; a498: 20 e8 a4     ..   
    lda #&80                                                          ; a49b: a9 80       ..    
    sta zp_fwa_exp                                                    ; a49d: 85 30       .0    
    ldx zp_fwa_m1                                                     ; a49f: a6 31       .1    
    bpl ca4b3                                                         ; a4a1: 10 10       ..    
    eor zp_fwa_sign                                                   ; a4a3: 45 2e       E.    
    sta zp_fwa_sign                                                   ; a4a5: 85 2e       ..    
    bpl ca4ae                                                         ; a4a7: 10 05       ..    
    inc l004a                                                         ; a4a9: e6 4a       .J    
    jmp ca4b0                                                         ; a4ab: 4c b0 a4    L..   
; &a4ae referenced 1 time by &a4a7
.ca4ae
    dec l004a                                                         ; a4ae: c6 4a       .J    
; &a4b0 referenced 1 time by &a4ab
.ca4b0
    jsr ca46c                                                         ; a4b0: 20 6c a4     l.   
; &a4b3 referenced 1 time by &a4a1
.ca4b3
    jmp fwa_normalise                                                 ; a4b3: 4c 03 a3    L..   
; &a4b6 referenced 1 time by &a4ca
.sub_ca4b6
    inc zp_fwa_m4                                                     ; a4b6: e6 34       .4    
    bne return_25                                                     ; a4b8: d0 0c       ..    
    inc zp_fwa_m3                                                     ; a4ba: e6 33       .3    
    bne return_25                                                     ; a4bc: d0 08       ..    
    inc zp_fwa_m2                                                     ; a4be: e6 32       .2    
    bne return_25                                                     ; a4c0: d0 04       ..    
    inc zp_fwa_m1                                                     ; a4c2: e6 31       .1    
    beq ca450                                                         ; a4c4: f0 8a       ..    
; &a4c6 referenced 3 times by &a4b8, &a4bc, &a4c0
.return_25
    rts                                                               ; a4c6: 60          `     
; &a4c7 referenced 1 time by &ac92
.sub_ca4c7
    jsr ca46c                                                         ; a4c7: 20 6c a4     l.   
    jsr sub_ca4b6                                                     ; a4ca: 20 b6 a4     ..   
    jmp ca46c                                                         ; a4cd: 4c 6c a4    Ll.   
; &a4d0 referenced 2 times by &9d08, &a9bd
.sub_ca4d0
    jsr fwa_rsub_var                                                  ; a4d0: 20 fd a4     ..   
    jmp fwa_negate                                                    ; a4d3: 4c 7e ad    L~.   
; ***************************************************************************************
; Swap FWA and a fp variable
;
; Exchange the FP accumulator with the fp variable operand.
; &a4d6 referenced 1 time by &a6d5
.fwa_swap_var
    jsr fwb_unpack_var                                                ; a4d6: 20 4e a3     N.   
    jsr fwa_pack_var                                                  ; a4d9: 20 8d a3     ..   
; ***************************************************************************************
; FWA = FWB
;
; Copy FWB into FWA.
; &a4dc referenced 2 times by &a50e, &a559
.fwa_copy_from_fwb
    lda zp_fwb_sign                                                   ; a4dc: a5 3b       .;    
    sta zp_fwa_sign                                                   ; a4de: 85 2e       ..    
    lda zp_fwb_ovf                                                    ; a4e0: a5 3c       .<    
    sta zp_fwa_ovf                                                    ; a4e2: 85 2f       ./    
    lda zp_fwb_exp                                                    ; a4e4: a5 3d       .=    
    sta zp_fwa_exp                                                    ; a4e6: 85 30       .0    
; &a4e8 referenced 1 time by &a498
.sub_ca4e8
    lda zp_fwb_m1                                                     ; a4e8: a5 3e       .>    
    sta zp_fwa_m1                                                     ; a4ea: 85 31       .1    
    lda zp_fwb_m2                                                     ; a4ec: a5 3f       .?    
    sta zp_fwa_m2                                                     ; a4ee: 85 32       .2    
    lda zp_fwb_m3                                                     ; a4f0: a5 40       .@    
    sta zp_fwa_m3                                                     ; a4f2: 85 33       .3    
    lda zp_fwb_m4                                                     ; a4f4: a5 41       .A    
    sta zp_fwa_m4                                                     ; a4f6: 85 34       .4    
    lda zp_fwb_rnd                                                    ; a4f8: a5 42       .B    
    sta zp_fwa_rnd                                                    ; a4fa: 85 35       .5    
; &a4fc referenced 2 times by &a503, &a51d
.return_26
    rts                                                               ; a4fc: 60          `     
; ***************************************************************************************
; FWA = fp var - FWA
;
; Reverse subtract: operand minus FWA (normalised, rounded).
; &a4fd referenced 2 times by &9cf4, &a4d0
.fwa_rsub_var
    jsr fwa_negate                                                    ; a4fd: 20 7e ad     ~.   
; ***************************************************************************************
; FWA = FWA + fp var
;
; Add the fp variable operand to FWA (normalised, rounded).
; &a500 referenced 10 times by &9c9e, &a7dd, &a848, &a863, &a8cc, &a92a, &a930, &aa1d, &aa32, &b774
.fwa_add_var
    jsr fwb_unpack_var                                                ; a500: 20 4e a3     N.   
    beq return_26                                                     ; a503: f0 f7       ..       ; Adding zero leaves FWA unchanged
; ***************************************************************************************
; FWA = FWA + FWB
;
; Add FWB to FWA (normalised, rounded).
; &a505 referenced 3 times by &a830, &a94a, &a9e8
.fwa_add_fwb
    jsr fwa_add_fwb_raw                                               ; a505: 20 0b a5     ..   
    jmp fwa_round                                                     ; a508: 4c 5c a6    L\.   
; ***************************************************************************************
; FWA = FWA + FWB (unrounded)
;
; Add FWB to FWA, normalised but not rounded.
; &a50b referenced 2 times by &9f7b, &a505
.fwa_add_fwb_raw
    jsr fwa_sign                                                      ; a50b: 20 da a1     ..   
    beq fwa_copy_from_fwb                                             ; a50e: f0 cc       ..       ; FWA is zero: the sum is simply FWB
    ldy #0                                                            ; a510: a0 00       ..    
    sec                                                               ; a512: 38          8     
    lda zp_fwa_exp                                                    ; a513: a5 30       .0    
    sbc zp_fwb_exp                                                    ; a515: e5 3d       .=       ; Exponent difference is the alignment shift
    beq ca590                                                         ; a517: f0 77       .w       ; Equal exponents: already aligned
    bcc ca552                                                         ; a519: 90 37       .7       ; FWA the smaller: align it to FWB instead
    cmp #&25 ; '%'                                                    ; a51b: c9 25       .%    
    bcs return_26                                                     ; a51d: b0 dd       ..       ; Differ by >= 37 bits: FWB too small to count
    pha                                                               ; a51f: 48          H     
    and #&38 ; '8'                                                    ; a520: 29 38       )8       ; Whole-byte part of the shift (difference / 8)
    beq ca53d                                                         ; a522: f0 19       ..    
    lsr a                                                             ; a524: 4a          J     
    lsr a                                                             ; a525: 4a          J     
    lsr a                                                             ; a526: 4a          J     
    tax                                                               ; a527: aa          .     
; &a528 referenced 1 time by &a53b
.loop_ca528
    lda zp_fwb_m4                                                     ; a528: a5 41       .A       ; Shift FWB down a byte at a time
    sta zp_fwb_rnd                                                    ; a52a: 85 42       .B    
    lda zp_fwb_m3                                                     ; a52c: a5 40       .@    
    sta zp_fwb_m4                                                     ; a52e: 85 41       .A    
    lda zp_fwb_m2                                                     ; a530: a5 3f       .?    
    sta zp_fwb_m3                                                     ; a532: 85 40       .@    
    lda zp_fwb_m1                                                     ; a534: a5 3e       .>    
    sta zp_fwb_m2                                                     ; a536: 85 3f       .?    
    sty zp_fwb_m1                                                     ; a538: 84 3e       .>    
    dex                                                               ; a53a: ca          .     
    bne loop_ca528                                                    ; a53b: d0 eb       ..    
; &a53d referenced 1 time by &a522
.ca53d
    pla                                                               ; a53d: 68          h     
    and #7                                                            ; a53e: 29 07       ).       ; then the remaining bits, to finish aligning FWB
    beq ca590                                                         ; a540: f0 4e       .N    
    tax                                                               ; a542: aa          .     
; &a543 referenced 1 time by &a54e
.loop_ca543
    lsr zp_fwb_m1                                                     ; a543: 46 3e       F>    
    ror zp_fwb_m2                                                     ; a545: 66 3f       f?    
    ror zp_fwb_m3                                                     ; a547: 66 40       f@    
    ror zp_fwb_m4                                                     ; a549: 66 41       fA    
    ror zp_fwb_rnd                                                    ; a54b: 66 42       fB    
    dex                                                               ; a54d: ca          .     
    bne loop_ca543                                                    ; a54e: d0 f3       ..    
    beq ca590                                                         ; a550: f0 3e       .>    
; &a552 referenced 1 time by &a519
.ca552
    sec                                                               ; a552: 38          8        ; FWB the smaller: shift FWA to align
    lda zp_fwb_exp                                                    ; a553: a5 3d       .=    
    sbc zp_fwa_exp                                                    ; a555: e5 30       .0    
    cmp #&25 ; '%'                                                    ; a557: c9 25       .%    
    bcs fwa_copy_from_fwb                                             ; a559: b0 81       ..    
    pha                                                               ; a55b: 48          H     
    and #&38 ; '8'                                                    ; a55c: 29 38       )8    
    beq ca579                                                         ; a55e: f0 19       ..    
    lsr a                                                             ; a560: 4a          J     
    lsr a                                                             ; a561: 4a          J     
    lsr a                                                             ; a562: 4a          J     
    tax                                                               ; a563: aa          .     
; &a564 referenced 1 time by &a577
.loop_ca564
    lda zp_fwa_m4                                                     ; a564: a5 34       .4    
    sta zp_fwa_rnd                                                    ; a566: 85 35       .5    
    lda zp_fwa_m3                                                     ; a568: a5 33       .3    
    sta zp_fwa_m4                                                     ; a56a: 85 34       .4    
    lda zp_fwa_m2                                                     ; a56c: a5 32       .2    
    sta zp_fwa_m3                                                     ; a56e: 85 33       .3    
    lda zp_fwa_m1                                                     ; a570: a5 31       .1    
    sta zp_fwa_m2                                                     ; a572: 85 32       .2    
    sty zp_fwa_m1                                                     ; a574: 84 31       .1    
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
    lsr zp_fwa_m1                                                     ; a57f: 46 31       F1    
    ror zp_fwa_m2                                                     ; a581: 66 32       f2    
    ror zp_fwa_m3                                                     ; a583: 66 33       f3    
    ror zp_fwa_m4                                                     ; a585: 66 34       f4    
    ror zp_fwa_rnd                                                    ; a587: 66 35       f5    
    dex                                                               ; a589: ca          .     
    bne loop_ca57f                                                    ; a58a: d0 f3       ..    
; &a58c referenced 1 time by &a57c
.ca58c
    lda zp_fwb_exp                                                    ; a58c: a5 3d       .=       ; Result takes the larger exponent
    sta zp_fwa_exp                                                    ; a58e: 85 30       .0    
; &a590 referenced 3 times by &a517, &a540, &a550
.ca590
    lda zp_fwa_sign                                                   ; a590: a5 2e       ..    
    eor zp_fwb_sign                                                   ; a592: 45 3b       E;       ; Compare the operand signs
    bpl fp_mantissas_add                                              ; a594: 10 49       .I       ; Same sign: add; opposite: subtract smaller from larger
    lda zp_fwa_m1                                                     ; a596: a5 31       .1    
    cmp zp_fwb_m1                                                     ; a598: c5 3e       .>    
    bne fp_mantissas_sub                                              ; a59a: d0 1b       ..    
    lda zp_fwa_m2                                                     ; a59c: a5 32       .2    
    cmp zp_fwb_m2                                                     ; a59e: c5 3f       .?    
    bne fp_mantissas_sub                                              ; a5a0: d0 15       ..    
    lda zp_fwa_m3                                                     ; a5a2: a5 33       .3    
    cmp zp_fwb_m3                                                     ; a5a4: c5 40       .@    
    bne fp_mantissas_sub                                              ; a5a6: d0 0f       ..    
    lda zp_fwa_m4                                                     ; a5a8: a5 34       .4    
    cmp zp_fwb_m4                                                     ; a5aa: c5 41       .A    
    bne fp_mantissas_sub                                              ; a5ac: d0 09       ..    
    lda zp_fwa_rnd                                                    ; a5ae: a5 35       .5    
    cmp zp_fwb_rnd                                                    ; a5b0: c5 42       .B    
    bne fp_mantissas_sub                                              ; a5b2: d0 03       ..    
    jmp fwa_clear                                                     ; a5b4: 4c 86 a6    L..      ; Equal magnitudes of opposite sign cancel to zero
; &a5b7 referenced 5 times by &a59a, &a5a0, &a5a6, &a5ac, &a5b2
.fp_mantissas_sub
    bcs ca5e3                                                         ; a5b7: b0 2a       .*    
    sec                                                               ; a5b9: 38          8     
    lda zp_fwb_rnd                                                    ; a5ba: a5 42       .B    
    sbc zp_fwa_rnd                                                    ; a5bc: e5 35       .5    
    sta zp_fwa_rnd                                                    ; a5be: 85 35       .5    
    lda zp_fwb_m4                                                     ; a5c0: a5 41       .A    
    sbc zp_fwa_m4                                                     ; a5c2: e5 34       .4    
    sta zp_fwa_m4                                                     ; a5c4: 85 34       .4    
    lda zp_fwb_m3                                                     ; a5c6: a5 40       .@    
    sbc zp_fwa_m3                                                     ; a5c8: e5 33       .3    
    sta zp_fwa_m3                                                     ; a5ca: 85 33       .3    
    lda zp_fwb_m2                                                     ; a5cc: a5 3f       .?    
    sbc zp_fwa_m2                                                     ; a5ce: e5 32       .2    
    sta zp_fwa_m2                                                     ; a5d0: 85 32       .2    
    lda zp_fwb_m1                                                     ; a5d2: a5 3e       .>    
    sbc zp_fwa_m1                                                     ; a5d4: e5 31       .1    
    sta zp_fwa_m1                                                     ; a5d6: 85 31       .1    
    lda zp_fwb_sign                                                   ; a5d8: a5 3b       .;    
    sta zp_fwa_sign                                                   ; a5da: 85 2e       ..    
    jmp fwa_normalise                                                 ; a5dc: 4c 03 a3    L..   
; &a5df referenced 1 time by &a594
.fp_mantissas_add
    clc                                                               ; a5df: 18          .     
    jmp ca208                                                         ; a5e0: 4c 08 a2    L..   
; &a5e3 referenced 1 time by &a5b7
.ca5e3
    sec                                                               ; a5e3: 38          8     
    lda zp_fwa_rnd                                                    ; a5e4: a5 35       .5    
    sbc zp_fwb_rnd                                                    ; a5e6: e5 42       .B    
    sta zp_fwa_rnd                                                    ; a5e8: 85 35       .5    
    lda zp_fwa_m4                                                     ; a5ea: a5 34       .4    
    sbc zp_fwb_m4                                                     ; a5ec: e5 41       .A    
    sta zp_fwa_m4                                                     ; a5ee: 85 34       .4    
    lda zp_fwa_m3                                                     ; a5f0: a5 33       .3    
    sbc zp_fwb_m3                                                     ; a5f2: e5 40       .@    
    sta zp_fwa_m3                                                     ; a5f4: 85 33       .3    
    lda zp_fwa_m2                                                     ; a5f6: a5 32       .2    
    sbc zp_fwb_m2                                                     ; a5f8: e5 3f       .?    
    sta zp_fwa_m2                                                     ; a5fa: 85 32       .2    
    lda zp_fwa_m1                                                     ; a5fc: a5 31       .1    
    equb &e5                                                          ; a5fe: e5          .     
; ***************************************************************************************
; Compare FWA with a fp variable
;
; Test the fp variable operand against FWA.
.fwa_compare_var
    rol l3185,x                                                       ; a5ff: 3e 85 31    >.1   
    jmp fwa_normalise                                                 ; a602: 4c 03 a3    L..   
; &a605 referenced 1 time by &a609
.return_27
    rts                                                               ; a605: 60          `     
; ***************************************************************************************
; FWA = FWA * fp var (raw)
;
; Multiply FWA by the operand, unnormalised and unrounded.
; &a606 referenced 2 times by &a656, &af30
.fwa_mul_var_raw
    jsr fwa_sign                                                      ; a606: 20 da a1     ..   
    beq return_27                                                     ; a609: f0 fa       ..    
    jsr fwb_unpack_var                                                ; a60b: 20 4e a3     N.   
    bne ca613                                                         ; a60e: d0 03       ..    
    jmp fwa_clear                                                     ; a610: 4c 86 a6    L..   
; &a613 referenced 1 time by &a60e
.ca613
    clc                                                               ; a613: 18          .     
    lda zp_fwa_exp                                                    ; a614: a5 30       .0    
    adc zp_fwb_exp                                                    ; a616: 65 3d       e=    
    bcc ca61d                                                         ; a618: 90 03       ..    
    inc zp_fwa_ovf                                                    ; a61a: e6 2f       ./    
    clc                                                               ; a61c: 18          .     
; &a61d referenced 1 time by &a618
.ca61d
    sbc #&7f                                                          ; a61d: e9 7f       ..    
    sta zp_fwa_exp                                                    ; a61f: 85 30       .0    
    bcs ca625                                                         ; a621: b0 02       ..    
    dec zp_fwa_ovf                                                    ; a623: c6 2f       ./    
; &a625 referenced 1 time by &a621
.ca625
    ldx #5                                                            ; a625: a2 05       ..    
    ldy #0                                                            ; a627: a0 00       ..    
; &a629 referenced 1 time by &a630
.loop_ca629
    lda zp_fwa_exp,x                                                  ; a629: b5 30       .0    
    sta zp_fwb_rnd,x                                                  ; a62b: 95 42       .B    
    sty zp_fwa_exp,x                                                  ; a62d: 94 30       .0    
    dex                                                               ; a62f: ca          .     
    bne loop_ca629                                                    ; a630: d0 f7       ..    
    lda zp_fwa_sign                                                   ; a632: a5 2e       ..    
    eor zp_fwb_sign                                                   ; a634: 45 3b       E;    
    sta zp_fwa_sign                                                   ; a636: 85 2e       ..    
    ldy #&20 ; ' '                                                    ; a638: a0 20       .     
; &a63a referenced 1 time by &a653
.loop_ca63a
    lsr zp_fwb_m1                                                     ; a63a: 46 3e       F>    
    ror zp_fwb_m2                                                     ; a63c: 66 3f       f?    
    ror zp_fwb_m3                                                     ; a63e: 66 40       f@    
    ror zp_fwb_m4                                                     ; a640: 66 41       fA    
    ror zp_fwb_rnd                                                    ; a642: 66 42       fB    
    asl l0046                                                         ; a644: 06 46       .F    
    rol l0045                                                         ; a646: 26 45       &E    
    rol l0044                                                         ; a648: 26 44       &D    
    rol zp_fp_temp                                                    ; a64a: 26 43       &C    
    bcc ca652                                                         ; a64c: 90 04       ..    
    clc                                                               ; a64e: 18          .     
    jsr sub_ca178                                                     ; a64f: 20 78 a1     x.   
; &a652 referenced 1 time by &a64c
.ca652
    dey                                                               ; a652: 88          .     
    bne loop_ca63a                                                    ; a653: d0 e5       ..    
    rts                                                               ; a655: 60          `     
; ***************************************************************************************
; FWA = FWA * fp var
;
; Multiply FWA by the fp variable operand (normalised, rounded).
; &a656 referenced 12 times by &9d2f, &9e81, &a842, &a845, &a85d, &a9b4, &a9c6, &aa17, &aa2c, &aad4, &ab2c, &abbc
.fwa_mul_var
    jsr fwa_mul_var_raw                                               ; a656: 20 06 a6     ..   
; &a659 referenced 2 times by &a7a6, &af81
.ca659
    jsr fwa_normalise                                                 ; a659: 20 03 a3     ..   
; ***************************************************************************************
; Round FWA
;
; Round the floating-point accumulator.
; &a65c referenced 2 times by &a118, &a508
.fwa_round
    lda zp_fwa_rnd                                                    ; a65c: a5 35       .5       ; The rounding byte holds the bits below the LSB
    cmp #&80                                                          ; a65e: c9 80       ..    
    bcc ca67c                                                         ; a660: 90 1a       ..       ; Below half: round down (truncate)
    beq ca676                                                         ; a662: f0 12       ..       ; Exactly half: special-case the LSB
    lda #&ff                                                          ; a664: a9 ff       ..       ; Above half: round up by adding 1
    jsr fwa_round_carry                                               ; a666: 20 a4 a2     ..   
    jmp ca67c                                                         ; a669: 4c 7c a6    L|.   
; &a66c referenced 2 times by &a450, &a684
.err_too_big
    brk                                                               ; a66c: 00          .     
    equb &14                                                          ; a66d: 14          .     
    equs "Too big"                                                    ; a66e: 54 6f 6f... Too...
    equb &00                                                          ; a675: 00          .     
; &a676 referenced 1 time by &a662
.ca676
    lda zp_fwa_m4                                                     ; a676: a5 34       .4    
    ora #1                                                            ; a678: 09 01       ..    
    sta zp_fwa_m4                                                     ; a67a: 85 34       .4    
; &a67c referenced 2 times by &a660, &a669
.ca67c
    lda #0                                                            ; a67c: a9 00       ..       ; Clear the now-spent rounding byte
    sta zp_fwa_rnd                                                    ; a67e: 85 35       .5    
    lda zp_fwa_ovf                                                    ; a680: a5 2f       ./       ; A carry may have overflowed the mantissa
    beq return_28                                                     ; a682: f0 14       ..    
    bpl err_too_big                                                   ; a684: 10 e6       ..       ; Overflowed the exponent range: Too big
; ***************************************************************************************
; FWA = 0
;
; Set the floating-point accumulator to zero.
; &a686 referenced 8 times by &9f5c, &9fa0, &a2ee, &a3fb, &a5b4, &a610, &a699, &aaa6
.fwa_clear
    lda #0                                                            ; a686: a9 00       ..    
    sta zp_fwa_sign                                                   ; a688: 85 2e       ..    
    sta zp_fwa_ovf                                                    ; a68a: 85 2f       ./    
    sta zp_fwa_exp                                                    ; a68c: 85 30       .0    
    sta zp_fwa_m1                                                     ; a68e: 85 31       .1    
    sta zp_fwa_m2                                                     ; a690: 85 32       .2    
    sta zp_fwa_m3                                                     ; a692: 85 33       .3    
    sta zp_fwa_m4                                                     ; a694: 85 34       .4    
    sta zp_fwa_rnd                                                    ; a696: 85 35       .5    
; &a698 referenced 2 times by &a682, &a6ea
.return_28
    rts                                                               ; a698: 60          `     
; ***************************************************************************************
; FWA = 1
;
; Set the floating-point accumulator to 1.
; &a699 referenced 6 times by &9e8b, &9f20, &a6a8, &a9ba, &ab22, &b863
.fwa_set_one
    jsr fwa_clear                                                     ; a699: 20 86 a6     ..   
    ldy #&80                                                          ; a69c: a0 80       ..    
    sty zp_fwa_m1                                                     ; a69e: 84 31       .1    
    iny                                                               ; a6a0: c8          .     
    sty zp_fwa_exp                                                    ; a6a1: 84 30       .0    
    tya                                                               ; a6a3: 98          .     
    rts                                                               ; a6a4: 60          `     
; ***************************************************************************************
; FWA = 1 / FWA
;
; Reciprocal of the FP accumulator (normalised, rounded).
; &a6a5 referenced 2 times by &a921, &ab1a
.fwa_reciprocal
    jsr fwa_pack_temp1                                                ; a6a5: 20 85 a3     ..   
    jsr fwa_set_one                                                   ; a6a8: 20 99 a6     ..   
    bne ca6e7                                                         ; a6ab: d0 3a       .:    
; ***************************************************************************************
; FWA = fp var / FWA
;
; Reverse divide: operand divided by FWA (normalised, rounded).
; &a6ad referenced 4 times by &9df8, &a7d6, &a8b8, &a8f8
.fwa_rdiv_var
    jsr fwa_sign                                                      ; a6ad: 20 da a1     ..   
    beq ca6bb                                                         ; a6b0: f0 09       ..    
    jsr fwb_copy_from_fwa                                             ; a6b2: 20 1e a2     ..   
    jsr fwa_unpack_var                                                ; a6b5: 20 b5 a3     ..   
    bne ca6f1                                                         ; a6b8: d0 37       .7    
    rts                                                               ; a6ba: 60          `     
; &a6bb referenced 2 times by &a6b0, &a6ef
.ca6bb
    jmp c99a7                                                         ; a6bb: 4c a7 99    L..   
; ***************************************************************************************
; TAN
;
; FWA = tan(FWA), argument in radians. Pure routine at &A6C1.
.fn_tan
    jsr sub_c92fa                                                     ; a6be: 20 fa 92     ..   
    jsr sub_ca9d3                                                     ; a6c1: 20 d3 a9     ..   
    lda l004a                                                         ; a6c4: a5 4a       .J    
    pha                                                               ; a6c6: 48          H     
    jsr sub_ca7e9                                                     ; a6c7: 20 e9 a7     ..   
    jsr fwa_pack_var                                                  ; a6ca: 20 8d a3     ..   
    inc l004a                                                         ; a6cd: e6 4a       .J    
    jsr ca99e                                                         ; a6cf: 20 9e a9     ..   
    jsr sub_ca7e9                                                     ; a6d2: 20 e9 a7     ..   
    jsr fwa_swap_var                                                  ; a6d5: 20 d6 a4     ..   
    pla                                                               ; a6d8: 68          h     
    sta l004a                                                         ; a6d9: 85 4a       .J    
    jsr ca99e                                                         ; a6db: 20 9e a9     ..   
    jsr sub_ca7e9                                                     ; a6de: 20 e9 a7     ..   
    jsr ca6e7                                                         ; a6e1: 20 e7 a6     ..   
    lda #&ff                                                          ; a6e4: a9 ff       ..    
    rts                                                               ; a6e6: 60          `     
; &a6e7 referenced 3 times by &a6ab, &a6e1, &a9eb
.ca6e7
    jsr fwa_sign                                                      ; a6e7: 20 da a1     ..   
    beq return_28                                                     ; a6ea: f0 ac       ..    
    jsr fwb_unpack_var                                                ; a6ec: 20 4e a3     N.   
    beq ca6bb                                                         ; a6ef: f0 ca       ..    
; &a6f1 referenced 1 time by &a6b8
.ca6f1
    lda zp_fwa_sign                                                   ; a6f1: a5 2e       ..    
    eor zp_fwb_sign                                                   ; a6f3: 45 3b       E;    
    sta zp_fwa_sign                                                   ; a6f5: 85 2e       ..    
    sec                                                               ; a6f7: 38          8     
    lda zp_fwa_exp                                                    ; a6f8: a5 30       .0    
    sbc zp_fwb_exp                                                    ; a6fa: e5 3d       .=    
    bcs ca701                                                         ; a6fc: b0 03       ..    
    dec zp_fwa_ovf                                                    ; a6fe: c6 2f       ./    
    sec                                                               ; a700: 38          8     
; &a701 referenced 1 time by &a6fc
.ca701
    adc #&80                                                          ; a701: 69 80       i.    
    sta zp_fwa_exp                                                    ; a703: 85 30       .0    
    bcc ca70a                                                         ; a705: 90 03       ..    
    inc zp_fwa_ovf                                                    ; a707: e6 2f       ./    
    clc                                                               ; a709: 18          .     
; &a70a referenced 1 time by &a705
.ca70a
    ldx #&20 ; ' '                                                    ; a70a: a2 20       .     
; &a70c referenced 1 time by &a750
.loop_ca70c
    bcs ca726                                                         ; a70c: b0 18       ..    
    lda zp_fwa_m1                                                     ; a70e: a5 31       .1    
    cmp zp_fwb_m1                                                     ; a710: c5 3e       .>    
    bne ca724                                                         ; a712: d0 10       ..    
    lda zp_fwa_m2                                                     ; a714: a5 32       .2    
    cmp zp_fwb_m2                                                     ; a716: c5 3f       .?    
    bne ca724                                                         ; a718: d0 0a       ..    
    lda zp_fwa_m3                                                     ; a71a: a5 33       .3    
    cmp zp_fwb_m3                                                     ; a71c: c5 40       .@    
    bne ca724                                                         ; a71e: d0 04       ..    
    lda zp_fwa_m4                                                     ; a720: a5 34       .4    
    cmp zp_fwb_m4                                                     ; a722: c5 41       .A    
; &a724 referenced 3 times by &a712, &a718, &a71e
.ca724
    bcc ca73f                                                         ; a724: 90 19       ..    
; &a726 referenced 1 time by &a70c
.ca726
    lda zp_fwa_m4                                                     ; a726: a5 34       .4    
    sbc zp_fwb_m4                                                     ; a728: e5 41       .A    
    sta zp_fwa_m4                                                     ; a72a: 85 34       .4    
    lda zp_fwa_m3                                                     ; a72c: a5 33       .3    
    sbc zp_fwb_m3                                                     ; a72e: e5 40       .@    
    sta zp_fwa_m3                                                     ; a730: 85 33       .3    
    lda zp_fwa_m2                                                     ; a732: a5 32       .2    
    sbc zp_fwb_m2                                                     ; a734: e5 3f       .?    
    sta zp_fwa_m2                                                     ; a736: 85 32       .2    
    lda zp_fwa_m1                                                     ; a738: a5 31       .1    
    sbc zp_fwb_m1                                                     ; a73a: e5 3e       .>    
    sta zp_fwa_m1                                                     ; a73c: 85 31       .1    
    sec                                                               ; a73e: 38          8     
; &a73f referenced 1 time by &a724
.ca73f
    rol l0046                                                         ; a73f: 26 46       &F    
    rol l0045                                                         ; a741: 26 45       &E    
    rol l0044                                                         ; a743: 26 44       &D    
    rol zp_fp_temp                                                    ; a745: 26 43       &C    
    asl zp_fwa_m4                                                     ; a747: 06 34       .4    
    rol zp_fwa_m3                                                     ; a749: 26 33       &3    
    rol zp_fwa_m2                                                     ; a74b: 26 32       &2    
    rol zp_fwa_m1                                                     ; a74d: 26 31       &1    
    dex                                                               ; a74f: ca          .     
    bne loop_ca70c                                                    ; a750: d0 ba       ..    
    ldx #7                                                            ; a752: a2 07       ..    
; &a754 referenced 1 time by &a792
.loop_ca754
    bcs ca76e                                                         ; a754: b0 18       ..    
    lda zp_fwa_m1                                                     ; a756: a5 31       .1    
    cmp zp_fwb_m1                                                     ; a758: c5 3e       .>    
    bne ca76c                                                         ; a75a: d0 10       ..    
    lda zp_fwa_m2                                                     ; a75c: a5 32       .2    
    cmp zp_fwb_m2                                                     ; a75e: c5 3f       .?    
    bne ca76c                                                         ; a760: d0 0a       ..    
    lda zp_fwa_m3                                                     ; a762: a5 33       .3    
    cmp zp_fwb_m3                                                     ; a764: c5 40       .@    
    bne ca76c                                                         ; a766: d0 04       ..    
    lda zp_fwa_m4                                                     ; a768: a5 34       .4    
    cmp zp_fwb_m4                                                     ; a76a: c5 41       .A    
; &a76c referenced 3 times by &a75a, &a760, &a766
.ca76c
    bcc ca787                                                         ; a76c: 90 19       ..    
; &a76e referenced 1 time by &a754
.ca76e
    lda zp_fwa_m4                                                     ; a76e: a5 34       .4    
    sbc zp_fwb_m4                                                     ; a770: e5 41       .A    
    sta zp_fwa_m4                                                     ; a772: 85 34       .4    
    lda zp_fwa_m3                                                     ; a774: a5 33       .3    
    sbc zp_fwb_m3                                                     ; a776: e5 40       .@    
    sta zp_fwa_m3                                                     ; a778: 85 33       .3    
    lda zp_fwa_m2                                                     ; a77a: a5 32       .2    
    sbc zp_fwb_m2                                                     ; a77c: e5 3f       .?    
    sta zp_fwa_m2                                                     ; a77e: 85 32       .2    
    lda zp_fwa_m1                                                     ; a780: a5 31       .1    
    sbc zp_fwb_m1                                                     ; a782: e5 3e       .>    
    sta zp_fwa_m1                                                     ; a784: 85 31       .1    
    sec                                                               ; a786: 38          8     
; &a787 referenced 1 time by &a76c
.ca787
    rol zp_fwa_rnd                                                    ; a787: 26 35       &5    
    asl zp_fwa_m4                                                     ; a789: 06 34       .4    
    rol zp_fwa_m3                                                     ; a78b: 26 33       &3    
    rol zp_fwa_m2                                                     ; a78d: 26 32       &2    
    rol zp_fwa_m1                                                     ; a78f: 26 31       &1    
    dex                                                               ; a791: ca          .     
    bne loop_ca754                                                    ; a792: d0 c0       ..    
    asl zp_fwa_rnd                                                    ; a794: 06 35       .5    
    lda l0046                                                         ; a796: a5 46       .F    
    sta zp_fwa_m4                                                     ; a798: 85 34       .4    
    lda l0045                                                         ; a79a: a5 45       .E    
    sta zp_fwa_m3                                                     ; a79c: 85 33       .3    
    lda l0044                                                         ; a79e: a5 44       .D    
    sta zp_fwa_m2                                                     ; a7a0: 85 32       .2    
    lda zp_fp_temp                                                    ; a7a2: a5 43       .C    
    sta zp_fwa_m1                                                     ; a7a4: 85 31       .1    
    jmp ca659                                                         ; a7a6: 4c 59 a6    LY.   
; &a7a9 referenced 1 time by &a7bc
.loop_ca7a9
    brk                                                               ; a7a9: 00          .     
    equb &15                                                          ; a7aa: 15          .     
    equs "-ve root"                                                   ; a7ab: 2d 76 65... -ve...
    equb &00                                                          ; a7b3: 00          .     
; ***************************************************************************************
; SQR
;
; FWA = square root of FWA. Pure routine at &A7B7.
.fn_sqr
    jsr sub_c92fa                                                     ; a7b4: 20 fa 92     ..   
; &a7b7 referenced 1 time by &a9c0
.ca7b7
    jsr fwa_sign                                                      ; a7b7: 20 da a1     ..   
    beq ca7e6                                                         ; a7ba: f0 2a       .*    
    bmi loop_ca7a9                                                    ; a7bc: 30 eb       0.    
    jsr fwa_pack_temp1                                                ; a7be: 20 85 a3     ..   
    lda zp_fwa_exp                                                    ; a7c1: a5 30       .0    
    lsr a                                                             ; a7c3: 4a          J     
    adc #&40 ; '@'                                                    ; a7c4: 69 40       i@    
    sta zp_fwa_exp                                                    ; a7c6: 85 30       .0    
    lda #5                                                            ; a7c8: a9 05       ..    
    sta l004a                                                         ; a7ca: 85 4a       .J    
    jsr sub_ca7ed                                                     ; a7cc: 20 ed a7     ..   
; &a7cf referenced 1 time by &a7e4
.loop_ca7cf
    jsr fwa_pack_var                                                  ; a7cf: 20 8d a3     ..   
    lda #&6c ; 'l'                                                    ; a7d2: a9 6c       .l    
    sta zp_fp_ptr                                                     ; a7d4: 85 4b       .K    
    jsr fwa_rdiv_var                                                  ; a7d6: 20 ad a6     ..   
    lda #&71 ; 'q'                                                    ; a7d9: a9 71       .q    
    sta zp_fp_ptr                                                     ; a7db: 85 4b       .K    
    jsr fwa_add_var                                                   ; a7dd: 20 00 a5     ..   
    dec zp_fwa_exp                                                    ; a7e0: c6 30       .0    
    dec l004a                                                         ; a7e2: c6 4a       .J    
    bne loop_ca7cf                                                    ; a7e4: d0 e9       ..    
; &a7e6 referenced 1 time by &a7ba
.ca7e6
    lda #&ff                                                          ; a7e6: a9 ff       ..    
    rts                                                               ; a7e8: 60          `     
; &a7e9 referenced 4 times by &a6c7, &a6d2, &a6de, &a83f
.sub_ca7e9
    lda #&7b ; '{'                                                    ; a7e9: a9 7b       .{    
    bne ca7f7                                                         ; a7eb: d0 0a       ..    
; &a7ed referenced 3 times by &9e7e, &a7cc, &aa23
.sub_ca7ed
    lda #&71 ; 'q'                                                    ; a7ed: a9 71       .q    
    bne ca7f7                                                         ; a7ef: d0 06       ..    
; &a7f1 referenced 2 times by &a8f5, &aad1
.sub_ca7f1
    lda #&76 ; 'v'                                                    ; a7f1: a9 76       .v    
    bne ca7f7                                                         ; a7f3: d0 02       ..    
; &a7f5 referenced 6 times by &9f71, &a3b2, &a860, &a8b5, &aa1a, &aa2f
.sub_ca7f5
    lda #&6c ; 'l'                                                    ; a7f5: a9 6c       .l    
; &a7f7 referenced 3 times by &a7eb, &a7ef, &a7f3
.ca7f7
    sta zp_fp_ptr                                                     ; a7f7: 85 4b       .K    
    lda #4                                                            ; a7f9: a9 04       ..    
    sta zp_fp_ptr_1                                                   ; a7fb: 85 4c       .L    
    rts                                                               ; a7fd: 60          `     
; ***************************************************************************************
; LN
;
; FWA = natural log of FWA. Pure routine at &A801.
; &a7fe referenced 1 time by &aba8
.fn_ln
    jsr sub_c92fa                                                     ; a7fe: 20 fa 92     ..   
; &a801 referenced 1 time by &9e75
.sub_ca801
    jsr fwa_sign                                                      ; a801: 20 da a1     ..   
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
    jsr fwb_clear                                                     ; a814: 20 53 a4     S.   
    ldy #&80                                                          ; a817: a0 80       ..    
    sty zp_fwb_sign                                                   ; a819: 84 3b       .;    
    sty zp_fwb_m1                                                     ; a81b: 84 3e       .>    
    iny                                                               ; a81d: c8          .     
    sty zp_fwb_exp                                                    ; a81e: 84 3d       .=    
    ldx zp_fwa_exp                                                    ; a820: a6 30       .0    
    beq ca82a                                                         ; a822: f0 06       ..    
    lda zp_fwa_m1                                                     ; a824: a5 31       .1    
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
    sty zp_fwa_exp                                                    ; a82e: 84 30       .0    
    jsr fwa_add_fwb                                                   ; a830: 20 05 a5     ..   
    lda #&7b ; '{'                                                    ; a833: a9 7b       .{    
    jsr ca387                                                         ; a835: 20 87 a3     ..   
    lda #&73 ; 's'                                                    ; a838: a9 73       .s    
    ldy #&a8                                                          ; a83a: a0 a8       ..    
    jsr sub_ca897                                                     ; a83c: 20 97 a8     ..   
    jsr sub_ca7e9                                                     ; a83f: 20 e9 a7     ..   
    jsr fwa_mul_var                                                   ; a842: 20 56 a6     V.   
    jsr fwa_mul_var                                                   ; a845: 20 56 a6     V.   
    jsr fwa_add_var                                                   ; a848: 20 00 a5     ..   
    jsr fwa_pack_temp1                                                ; a84b: 20 85 a3     ..   
    pla                                                               ; a84e: 68          h     
    sec                                                               ; a84f: 38          8     
    sbc #&81                                                          ; a850: e9 81       ..    
    jsr sub_ca2ed                                                     ; a852: 20 ed a2     ..   
    lda #&6e ; 'n'                                                    ; a855: a9 6e       .n    
    sta zp_fp_ptr                                                     ; a857: 85 4b       .K    
    lda #&a8                                                          ; a859: a9 a8       ..    
    sta zp_fp_ptr_1                                                   ; a85b: 85 4c       .L    
    jsr fwa_mul_var                                                   ; a85d: 20 56 a6     V.   
    jsr sub_ca7f5                                                     ; a860: 20 f5 a7     ..   
    jsr fwa_add_var                                                   ; a863: 20 00 a5     ..   
    lda #&ff                                                          ; a866: a9 ff       ..    
    rts                                                               ; a868: 60          `     
    equb &7f, &5e, &5b, &d8, &aa, &80, &31, &72, &17, &f8, &06, &7a   ; a869: 7f 5e 5b... .^[...
    equb &12, &38, &a5, &0b, &88, &79, &0e, &9f, &f3, &7c, &2a, &ac   ; a875: 12 38 a5... .8....
    equb &3f, &b5, &86, &34, &01, &a2, &7a, &7f, &63, &8e, &37, &ec   ; a881: 3f b5 86... ?.....
    equb &82, &3f, &ff, &ff, &c1, &7f, &ff, &ff, &ff, &ff             ; a88d: 82 3f ff... .?....
; &a897 referenced 4 times by &a83c, &a951, &a9cd, &aade
.sub_ca897
    sta l004d                                                         ; a897: 85 4d       .M    
    sty l004e                                                         ; a899: 84 4e       .N    
    jsr fwa_pack_temp1                                                ; a89b: 20 85 a3     ..   
    ldy #0                                                            ; a89e: a0 00       ..    
    lda (l004d),y                                                     ; a8a0: b1 4d       .M    
    sta l0048                                                         ; a8a2: 85 48       .H    
    inc l004d                                                         ; a8a4: e6 4d       .M    
    bne ca8aa                                                         ; a8a6: d0 02       ..    
    inc l004e                                                         ; a8a8: e6 4e       .N    
; &a8aa referenced 1 time by &a8a6
.ca8aa
    lda l004d                                                         ; a8aa: a5 4d       .M    
    sta zp_fp_ptr                                                     ; a8ac: 85 4b       .K    
    lda l004e                                                         ; a8ae: a5 4e       .N    
    sta zp_fp_ptr_1                                                   ; a8b0: 85 4c       .L    
    jsr fwa_unpack_var                                                ; a8b2: 20 b5 a3     ..   
; &a8b5 referenced 1 time by &a8d1
.loop_ca8b5
    jsr sub_ca7f5                                                     ; a8b5: 20 f5 a7     ..   
    jsr fwa_rdiv_var                                                  ; a8b8: 20 ad a6     ..   
    clc                                                               ; a8bb: 18          .     
    lda l004d                                                         ; a8bc: a5 4d       .M    
    adc #5                                                            ; a8be: 69 05       i.    
    sta l004d                                                         ; a8c0: 85 4d       .M    
    sta zp_fp_ptr                                                     ; a8c2: 85 4b       .K    
    lda l004e                                                         ; a8c4: a5 4e       .N    
    adc #0                                                            ; a8c6: 69 00       i.    
    sta l004e                                                         ; a8c8: 85 4e       .N    
    sta zp_fp_ptr_1                                                   ; a8ca: 85 4c       .L    
    jsr fwa_add_var                                                   ; a8cc: 20 00 a5     ..   
    dec l0048                                                         ; a8cf: c6 48       .H    
    bne loop_ca8b5                                                    ; a8d1: d0 e2       ..    
    rts                                                               ; a8d3: 60          `     
; ***************************************************************************************
; ACS
;
; FWA = arccos(FWA), result in radians. Computed as arcsin then adjusted at &A927.
.fn_acs
    jsr fn_asn                                                        ; a8d4: 20 da a8     ..   
    jmp ca927                                                         ; a8d7: 4c 27 a9    L'.   
; ***************************************************************************************
; ASN
;
; FWA = arcsin(FWA), result in radians. Pure routine at &A8DD.
; &a8da referenced 1 time by &a8d4
.fn_asn
    jsr sub_c92fa                                                     ; a8da: 20 fa 92     ..   
    jsr fwa_sign                                                      ; a8dd: 20 da a1     ..   
    bpl ca8ea                                                         ; a8e0: 10 08       ..    
    lsr zp_fwa_sign                                                   ; a8e2: 46 2e       F.    
    jsr ca8ea                                                         ; a8e4: 20 ea a8     ..   
    jmp ca916                                                         ; a8e7: 4c 16 a9    L..   
; &a8ea referenced 2 times by &a8e0, &a8e4
.ca8ea
    jsr fwa_pack_temp3                                                ; a8ea: 20 81 a3     ..   
    jsr sub_ca9b1                                                     ; a8ed: 20 b1 a9     ..   
    jsr fwa_sign                                                      ; a8f0: 20 da a1     ..   
    beq ca8fe                                                         ; a8f3: f0 09       ..    
    jsr sub_ca7f1                                                     ; a8f5: 20 f1 a7     ..   
    jsr fwa_rdiv_var                                                  ; a8f8: 20 ad a6     ..   
    jmp ca90a                                                         ; a8fb: 4c 0a a9    L..   
; &a8fe referenced 2 times by &a8f3, &abcb
.ca8fe
    jsr sub_caa55                                                     ; a8fe: 20 55 aa     U.   
    jsr fwa_unpack_var                                                ; a901: 20 b5 a3     ..   
; &a904 referenced 2 times by &a90d, &a93a
.ca904
    lda #&ff                                                          ; a904: a9 ff       ..    
    rts                                                               ; a906: 60          `     
; ***************************************************************************************
; ATN
;
; FWA = arctan(FWA), result in radians. Pure routine at &A90A.
.fn_atn
    jsr sub_c92fa                                                     ; a907: 20 fa 92     ..   
; &a90a referenced 1 time by &a8fb
.ca90a
    jsr fwa_sign                                                      ; a90a: 20 da a1     ..   
    beq ca904                                                         ; a90d: f0 f5       ..    
    bpl ca91b                                                         ; a90f: 10 0a       ..    
    lsr zp_fwa_sign                                                   ; a911: 46 2e       F.    
    jsr ca91b                                                         ; a913: 20 1b a9     ..   
; &a916 referenced 1 time by &a8e7
.ca916
    lda #&80                                                          ; a916: a9 80       ..    
    sta zp_fwa_sign                                                   ; a918: 85 2e       ..    
    rts                                                               ; a91a: 60          `     
; &a91b referenced 2 times by &a90f, &a913
.ca91b
    lda zp_fwa_exp                                                    ; a91b: a5 30       .0    
    cmp #&81                                                          ; a91d: c9 81       ..    
    bcc ca936                                                         ; a91f: 90 15       ..    
    jsr fwa_reciprocal                                                ; a921: 20 a5 a6     ..   
    jsr ca936                                                         ; a924: 20 36 a9     6.   
; &a927 referenced 1 time by &a8d7
.ca927
    jsr sub_caa48                                                     ; a927: 20 48 aa     H.   
    jsr fwa_add_var                                                   ; a92a: 20 00 a5     ..   
    jsr sub_caa4c                                                     ; a92d: 20 4c aa     L.   
    jsr fwa_add_var                                                   ; a930: 20 00 a5     ..   
    jmp fwa_negate                                                    ; a933: 4c 7e ad    L~.   
; &a936 referenced 2 times by &a91f, &a924
.ca936
    lda zp_fwa_exp                                                    ; a936: a5 30       .0    
    cmp #&73 ; 's'                                                    ; a938: c9 73       .s    
    bcc ca904                                                         ; a93a: 90 c8       ..    
    jsr fwa_pack_temp3                                                ; a93c: 20 81 a3     ..   
    jsr fwb_clear                                                     ; a93f: 20 53 a4     S.   
    lda #&80                                                          ; a942: a9 80       ..    
    sta zp_fwb_exp                                                    ; a944: 85 3d       .=    
    sta zp_fwb_m1                                                     ; a946: 85 3e       .>    
    sta zp_fwb_sign                                                   ; a948: 85 3b       .;    
    jsr fwa_add_fwb                                                   ; a94a: 20 05 a5     ..   
    lda #&5a ; 'Z'                                                    ; a94d: a9 5a       .Z    
    ldy #&a9                                                          ; a94f: a0 a9       ..    
    jsr sub_ca897                                                     ; a951: 20 97 a8     ..   
    jsr caad1                                                         ; a954: 20 d1 aa     ..   
    lda #&ff                                                          ; a957: a9 ff       ..    
    rts                                                               ; a959: 60          `     
    equb &09, &85, &a3, &59, &e8, &67, &80, &1c, &9d, &07, &36, &80   ; a95a: 09 85 a3... ......
    equb &57, &bb, &78, &df, &80, &ca, &9a, &0e, &83, &84, &8c, &bb   ; a966: 57 bb 78... W.x...
    equb &ca, &6e, &81, &95, &96, &06, &de, &81, &0a, &c7, &6c, &52   ; a972: ca 6e 81... .n....
    equb &7f, &7d, &ad, &90, &a1, &82, &fb                            ; a97e: 7f 7d ad... .}....
    equs "bW/"                                                        ; a985: 62 57 2f    bW/   
    equb &80                                                          ; a988: 80          .     
    equs "mc8,"                                                       ; a989: 6d 63 38... mc8...
; ***************************************************************************************
; COS
;
; FWA = cos(FWA), argument in radians. Pure routine at &A990.
.fn_cos
    jsr sub_c92fa                                                     ; a98d: 20 fa 92     ..   
    jsr sub_ca9d3                                                     ; a990: 20 d3 a9     ..   
    inc l004a                                                         ; a993: e6 4a       .J    
    jmp ca99e                                                         ; a995: 4c 9e a9    L..   
; ***************************************************************************************
; SIN
;
; FWA = sin(FWA), argument in radians. Pure routine at &A99B.
.fn_sin
    jsr sub_c92fa                                                     ; a998: 20 fa 92     ..   
    jsr sub_ca9d3                                                     ; a99b: 20 d3 a9     ..   
; &a99e referenced 3 times by &a6cf, &a6db, &a995
.ca99e
    lda l004a                                                         ; a99e: a5 4a       .J    
    and #2                                                            ; a9a0: 29 02       ).    
    beq ca9aa                                                         ; a9a2: f0 06       ..    
    jsr ca9aa                                                         ; a9a4: 20 aa a9     ..   
    jmp fwa_negate                                                    ; a9a7: 4c 7e ad    L~.   
; &a9aa referenced 2 times by &a9a2, &a9a4
.ca9aa
    lsr l004a                                                         ; a9aa: 46 4a       FJ    
    bcc ca9c3                                                         ; a9ac: 90 15       ..    
    jsr ca9c3                                                         ; a9ae: 20 c3 a9     ..   
; &a9b1 referenced 1 time by &a8ed
.sub_ca9b1
    jsr fwa_pack_temp1                                                ; a9b1: 20 85 a3     ..   
    jsr fwa_mul_var                                                   ; a9b4: 20 56 a6     V.   
    jsr fwa_pack_var                                                  ; a9b7: 20 8d a3     ..   
    jsr fwa_set_one                                                   ; a9ba: 20 99 a6     ..   
    jsr sub_ca4d0                                                     ; a9bd: 20 d0 a4     ..   
    jmp ca7b7                                                         ; a9c0: 4c b7 a7    L..   
; &a9c3 referenced 2 times by &a9ac, &a9ae
.ca9c3
    jsr fwa_pack_temp3                                                ; a9c3: 20 81 a3     ..   
    jsr fwa_mul_var                                                   ; a9c6: 20 56 a6     V.   
    lda #&72 ; 'r'                                                    ; a9c9: a9 72       .r    
    ldy #&aa                                                          ; a9cb: a0 aa       ..    
    jsr sub_ca897                                                     ; a9cd: 20 97 a8     ..   
    jmp caad1                                                         ; a9d0: 4c d1 aa    L..   
; &a9d3 referenced 3 times by &a6c1, &a990, &a99b
.sub_ca9d3
    lda zp_fwa_exp                                                    ; a9d3: a5 30       .0    
    cmp #&98                                                          ; a9d5: c9 98       ..    
    bcs caa38                                                         ; a9d7: b0 5f       ._    
    jsr fwa_pack_temp1                                                ; a9d9: 20 85 a3     ..   
    jsr sub_caa55                                                     ; a9dc: 20 55 aa     U.   
    jsr fwb_unpack_var                                                ; a9df: 20 4e a3     N.   
    lda zp_fwa_sign                                                   ; a9e2: a5 2e       ..    
    sta zp_fwb_sign                                                   ; a9e4: 85 3b       .;    
    dec zp_fwb_exp                                                    ; a9e6: c6 3d       .=    
    jsr fwa_add_fwb                                                   ; a9e8: 20 05 a5     ..   
    jsr ca6e7                                                         ; a9eb: 20 e7 a6     ..   
    jsr fwa_to_int2                                                   ; a9ee: 20 fe a3     ..   
    lda zp_fwa_m4                                                     ; a9f1: a5 34       .4    
    sta l004a                                                         ; a9f3: 85 4a       .J    
    ora zp_fwa_m3                                                     ; a9f5: 05 33       .3    
    ora zp_fwa_m2                                                     ; a9f7: 05 32       .2    
    ora zp_fwa_m1                                                     ; a9f9: 05 31       .1    
    beq caa35                                                         ; a9fb: f0 38       .8    
    lda #&a0                                                          ; a9fd: a9 a0       ..    
    sta zp_fwa_exp                                                    ; a9ff: 85 30       .0    
    ldy #0                                                            ; aa01: a0 00       ..    
    sty zp_fwa_rnd                                                    ; aa03: 84 35       .5    
    lda zp_fwa_m1                                                     ; aa05: a5 31       .1    
    sta zp_fwa_sign                                                   ; aa07: 85 2e       ..    
    bpl caa0e                                                         ; aa09: 10 03       ..    
    jsr ca46c                                                         ; aa0b: 20 6c a4     l.   
; &aa0e referenced 1 time by &aa09
.caa0e
    jsr fwa_normalise                                                 ; aa0e: 20 03 a3     ..   
    jsr fwa_pack_temp2                                                ; aa11: 20 7d a3     }.   
    jsr sub_caa48                                                     ; aa14: 20 48 aa     H.   
    jsr fwa_mul_var                                                   ; aa17: 20 56 a6     V.   
    jsr sub_ca7f5                                                     ; aa1a: 20 f5 a7     ..   
    jsr fwa_add_var                                                   ; aa1d: 20 00 a5     ..   
    jsr fwa_pack_var                                                  ; aa20: 20 8d a3     ..   
    jsr sub_ca7ed                                                     ; aa23: 20 ed a7     ..   
    jsr fwa_unpack_var                                                ; aa26: 20 b5 a3     ..   
    jsr sub_caa4c                                                     ; aa29: 20 4c aa     L.   
    jsr fwa_mul_var                                                   ; aa2c: 20 56 a6     V.   
    jsr sub_ca7f5                                                     ; aa2f: 20 f5 a7     ..   
    jmp fwa_add_var                                                   ; aa32: 4c 00 a5    L..   
; &aa35 referenced 1 time by &a9fb
.caa35
    jmp fwa_unpack_temp1                                              ; aa35: 4c b2 a3    L..   
; &aa38 referenced 1 time by &a9d7
.caa38
    brk                                                               ; aa38: 00          .     
    equb &17                                                          ; aa39: 17          .     
    equs "Accuracy lost"                                              ; aa3a: 41 63 63... Acc...
    equb &00                                                          ; aa47: 00          .     
; &aa48 referenced 2 times by &a927, &aa14
.sub_caa48
    lda #&59 ; 'Y'                                                    ; aa48: a9 59       .Y    
    bne caa4e                                                         ; aa4a: d0 02       ..    
; &aa4c referenced 2 times by &a92d, &aa29
.sub_caa4c
    lda #&5e ; '^'                                                    ; aa4c: a9 5e       .^    
; &aa4e referenced 2 times by &aa4a, &aa57
.caa4e
    sta zp_fp_ptr                                                     ; aa4e: 85 4b       .K    
    lda #&aa                                                          ; aa50: a9 aa       ..    
    sta zp_fp_ptr_1                                                   ; aa52: 85 4c       .L    
    rts                                                               ; aa54: 60          `     
; &aa55 referenced 2 times by &a8fe, &a9dc
.sub_caa55
    lda #&63 ; 'c'                                                    ; aa55: a9 63       .c    
    bne caa4e                                                         ; aa57: d0 f5       ..    
    sta (l00c9,x)                                                     ; aa59: 81 c9       ..    
    bpl caa5d                                                         ; aa5b: 10 00       ..    
; &aa5d referenced 1 time by &aa5b
.caa5d
    brk                                                               ; aa5d: 00          .     
    equb &6f, &15                                                     ; aa5e: 6f 15       o.    
    equs "wza"                                                        ; aa60: 77 7a 61    wza   
    equb &81, &49, &0f, &da, &a2, &7b, &0e, &fa, &35, &12, &86, &65   ; aa63: 81 49 0f... .I....
    equb &2e, &e0, &d3, &05, &84, &8a, &ea, &0c, &1b, &84, &1a, &be   ; aa6f: 2e e0 d3... ......
    equb &bb, &2b, &84                                                ; aa7b: bb 2b 84    .+.   
    equs "7EU"                                                        ; aa7e: 37 45 55    7EU   
    equb &ab, &82, &d5                                                ; aa81: ab 82 d5    ...   
    equs "UW|"                                                        ; aa84: 55 57 7c    UW|   
    equb &83, &c0, &00, &00, &05, &81, &00, &00, &00, &00             ; aa87: 83 c0 00... ......
; ***************************************************************************************
; EXP
;
; FWA = e to the power FWA. Pure routine at &AA94.
.fn_exp
    jsr sub_c92fa                                                     ; aa91: 20 fa 92     ..   
; &aa94 referenced 1 time by &9e7b
.sub_caa94
    lda zp_fwa_exp                                                    ; aa94: a5 30       .0    
    cmp #&87                                                          ; aa96: c9 87       ..    
    bcc caab8                                                         ; aa98: 90 1e       ..    
    bne caaa2                                                         ; aa9a: d0 06       ..    
    ldy zp_fwa_m1                                                     ; aa9c: a4 31       .1    
    cpy #&b3                                                          ; aa9e: c0 b3       ..    
    bcc caab8                                                         ; aaa0: 90 16       ..    
; &aaa2 referenced 1 time by &aa9a
.caaa2
    lda zp_fwa_sign                                                   ; aaa2: a5 2e       ..    
    bpl caaac                                                         ; aaa4: 10 06       ..    
    jsr fwa_clear                                                     ; aaa6: 20 86 a6     ..   
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
    jsr fwa_pack_temp3                                                ; aabe: 20 81 a3     ..   
    lda #&e4                                                          ; aac1: a9 e4       ..    
    sta zp_fp_ptr                                                     ; aac3: 85 4b       .K    
    lda #&aa                                                          ; aac5: a9 aa       ..    
    sta zp_fp_ptr_1                                                   ; aac7: 85 4c       .L    
    jsr fwa_unpack_var                                                ; aac9: 20 b5 a3     ..   
    lda l004a                                                         ; aacc: a5 4a       .J    
    jsr sub_cab12                                                     ; aace: 20 12 ab     ..   
; &aad1 referenced 3 times by &9e78, &a954, &a9d0
.caad1
    jsr sub_ca7f1                                                     ; aad1: 20 f1 a7     ..   
    jsr fwa_mul_var                                                   ; aad4: 20 56 a6     V.   
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
    jsr fwa_reciprocal                                                ; ab1a: 20 a5 a6     ..   
    pla                                                               ; ab1d: 68          h     
; &ab1e referenced 1 time by &ab13
.cab1e
    pha                                                               ; ab1e: 48          H     
    jsr fwa_pack_temp1                                                ; ab1f: 20 85 a3     ..   
    jsr fwa_set_one                                                   ; ab22: 20 99 a6     ..   
; &ab25 referenced 1 time by &ab2f
.cab25
    pla                                                               ; ab25: 68          h     
    beq return_29                                                     ; ab26: f0 0a       ..    
    sec                                                               ; ab28: 38          8     
    sbc #1                                                            ; ab29: e9 01       ..    
    pha                                                               ; ab2b: 48          H     
    jsr fwa_mul_var                                                   ; ab2c: 20 56 a6     V.   
    jmp cab25                                                         ; ab2f: 4c 25 ab    L%.   
; &ab32 referenced 1 time by &ab26
.return_29
    rts                                                               ; ab32: 60          `     
; ***************************************************************************************
; ADVAL
;
; Read an analogue (A/D) channel or a buffer status. ADVAL numeric.
.fn_adval
    jsr sub_c92e3                                                     ; ab33: 20 e3 92     ..   
    ldx zp_iwa                                                        ; ab36: a6 2a       .*    
    lda #osbyte_read_adc_or_get_buffer_status                         ; ab38: a9 80       ..    
    jsr osbyte                                                        ; ab3a: 20 f4 ff     ..      ; Read ADC channel X or buffer status
    txa                                                               ; ab3d: 8a          .     
    jmp iwa_from_ya                                                   ; ab3e: 4c ea ae    L..   
; ***************************************************************************************
; POINT
;
; Logical colour of a graphics point. POINT(x, y).
.fn_point
    jsr sub_c92dd                                                     ; ab41: 20 dd 92     ..   
    jsr stack_integer                                                 ; ab44: 20 94 bd     ..   
    jsr skip_spaces_expect_comma                                      ; ab47: 20 ae 8a     ..   
    jsr cae56                                                         ; ab4a: 20 56 ae     V.   
    jsr coerce_to_integer                                             ; ab4d: 20 f0 92     ..   
    lda zp_iwa                                                        ; ab50: a5 2a       .*    
    pha                                                               ; ab52: 48          H     
    lda zp_iwa_1                                                      ; ab53: a5 2b       .+    
    pha                                                               ; ab55: 48          H     
    jsr unstack_integer                                               ; ab56: 20 ea bd     ..   
    pla                                                               ; ab59: 68          h     
    sta zp_iwa_3                                                      ; ab5a: 85 2d       .-    
    pla                                                               ; ab5c: 68          h     
    sta zp_iwa_2                                                      ; ab5d: 85 2c       .,    
    ldx #&2a ; '*'                                                    ; ab5f: a2 2a       .*    
    lda #osword_read_pixel                                            ; ab61: a9 09       ..    
    jsr osword                                                        ; ab63: 20 f1 ff     ..      ; Read pixel value
    lda zp_fwa_sign                                                   ; ab66: a5 2e       ..    
    bmi cab9d                                                         ; ab68: 30 33       03    
    jmp caed8                                                         ; ab6a: 4c d8 ae    L..   
; ***************************************************************************************
; POS
;
; Horizontal text-cursor position in the window. POS.
.fn_pos
    lda #osbyte_read_text_cursor_pos                                  ; ab6d: a9 86       ..    
    jsr osbyte                                                        ; ab6f: 20 f4 ff     ..      ; Read input cursor position (Sets X=POS and Y=VPOS)
    txa                                                               ; ab72: 8a          .        ; X is the horizontal text position ('POS') / Y is the vertical text position ('VPOS')
    jmp caed8                                                         ; ab73: 4c d8 ae    L..   
; ***************************************************************************************
; VPOS
;
; Vertical text-cursor position in the window. VPOS.
.fn_vpos
    lda #osbyte_read_text_cursor_pos                                  ; ab76: a9 86       ..    
    jsr osbyte                                                        ; ab78: 20 f4 ff     ..      ; Read input cursor position (Sets X=POS and Y=VPOS)
    tya                                                               ; ab7b: 98          .        ; X is the horizontal text position ('POS') / Y is the vertical text position ('VPOS')
    jmp caed8                                                         ; ab7c: 4c d8 ae    L..   
; &ab7f referenced 1 time by &ab8d
.loop_cab7f
    jsr fwa_sign                                                      ; ab7f: 20 da a1     ..   
    beq caba2                                                         ; ab82: f0 1e       ..    
    bpl caba0                                                         ; ab84: 10 1a       ..    
    bmi cab9d                                                         ; ab86: 30 15       0.    
; ***************************************************************************************
; SGN
;
; Sign of a number: -1, 0 or +1. SGN numeric.
.fn_sgn
    jsr eval_factor                                                   ; ab88: 20 ec ad     ..   
    beq cabe6                                                         ; ab8b: f0 59       .Y    
    bmi loop_cab7f                                                    ; ab8d: 30 f0       0.    
    lda zp_iwa_3                                                      ; ab8f: a5 2d       .-    
    ora zp_iwa_2                                                      ; ab91: 05 2c       .,    
    ora zp_iwa_1                                                      ; ab93: 05 2b       .+    
    ora zp_iwa                                                        ; ab95: 05 2a       .*    
    beq caba5                                                         ; ab97: f0 0c       ..    
    lda zp_iwa_3                                                      ; ab99: a5 2d       .-    
    bpl caba0                                                         ; ab9b: 10 03       ..    
; &ab9d referenced 2 times by &ab68, &ab86
.cab9d
    jmp fn_true                                                       ; ab9d: 4c c4 ac    L..   
; &aba0 referenced 2 times by &ab84, &ab9b
.caba0
    lda #1                                                            ; aba0: a9 01       ..    
; &aba2 referenced 1 time by &ab82
.caba2
    jmp caed8                                                         ; aba2: 4c d8 ae    L..   
; &aba5 referenced 1 time by &ab97
.caba5
    lda #&40 ; '@'                                                    ; aba5: a9 40       .@    
    rts                                                               ; aba7: 60          `     
; ***************************************************************************************
; LOG
;
; FWA = base-10 log of FWA. Pure routine at &ABAB.
.fn_log
    jsr fn_ln                                                         ; aba8: 20 fe a7     ..   
    ldy #&69 ; 'i'                                                    ; abab: a0 69       .i    
    lda #&a8                                                          ; abad: a9 a8       ..    
    bne cabb8                                                         ; abaf: d0 07       ..    
; ***************************************************************************************
; RAD
;
; FWA = FWA degrees expressed in radians. Pure routine at &ABB4.
.fn_rad
    jsr sub_c92fa                                                     ; abb1: 20 fa 92     ..   
    ldy #&68 ; 'h'                                                    ; abb4: a0 68       .h    
    lda #&aa                                                          ; abb6: a9 aa       ..    
; &abb8 referenced 2 times by &abaf, &abc9
.cabb8
    sty zp_fp_ptr                                                     ; abb8: 84 4b       .K    
    sta zp_fp_ptr_1                                                   ; abba: 85 4c       .L    
    jsr fwa_mul_var                                                   ; abbc: 20 56 a6     V.   
    lda #&ff                                                          ; abbf: a9 ff       ..    
    rts                                                               ; abc1: 60          `     
; ***************************************************************************************
; DEG
;
; FWA = FWA radians expressed in degrees. Pure routine at &ABC5.
.fn_deg
    jsr sub_c92fa                                                     ; abc2: 20 fa 92     ..   
    ldy #&6d ; 'm'                                                    ; abc5: a0 6d       .m    
    lda #&aa                                                          ; abc7: a9 aa       ..    
    bne cabb8                                                         ; abc9: d0 ed       ..    
; ***************************************************************************************
; PI
;
; FWA = pi (3.14159265). Takes no argument.
.fn_pi
    jsr ca8fe                                                         ; abcb: 20 fe a8     ..   
    inc zp_fwa_exp                                                    ; abce: e6 30       .0    
    tay                                                               ; abd0: a8          .     
    rts                                                               ; abd1: 60          `     
; ***************************************************************************************
; USR
;
; Call machine code and return the result registers packed into a value. USR address.
.fn_usr
    jsr sub_c92e3                                                     ; abd2: 20 e3 92     ..   
    jsr sub_c8f1e                                                     ; abd5: 20 1e 8f     ..   
    sta zp_iwa                                                        ; abd8: 85 2a       .*    
    stx zp_iwa_1                                                      ; abda: 86 2b       .+    
    sty zp_iwa_2                                                      ; abdc: 84 2c       .,    
    php                                                               ; abde: 08          .     
    pla                                                               ; abdf: 68          h     
    sta zp_iwa_3                                                      ; abe0: 85 2d       .-    
    cld                                                               ; abe2: d8          .     
    lda #&40 ; '@'                                                    ; abe3: a9 40       .@    
    rts                                                               ; abe5: 60          `     
; &abe6 referenced 2 times by &ab8b, &abec
.cabe6
    jmp c8c0e                                                         ; abe6: 4c 0e 8c    L..   
; ***************************************************************************************
; EVAL
;
; Evaluate a string as a BASIC expression. EVAL string.
.fn_eval
    jsr eval_factor                                                   ; abe9: 20 ec ad     ..   
    bne cabe6                                                         ; abec: d0 f8       ..    
    inc zp_strbuf_len                                                 ; abee: e6 36       .6    
    ldy zp_strbuf_len                                                 ; abf0: a4 36       .6    
    lda #&0d                                                          ; abf2: a9 0d       ..    
    sta l05ff,y                                                       ; abf4: 99 ff 05    ...   
    jsr stack_string                                                  ; abf7: 20 b2 bd     ..   
    lda zp_text_ptr2                                                  ; abfa: a5 19       ..    
    pha                                                               ; abfc: 48          H     
    lda l001a                                                         ; abfd: a5 1a       ..    
    pha                                                               ; abff: 48          H     
    lda zp_text_ptr2_off                                              ; ac00: a5 1b       ..    
    pha                                                               ; ac02: 48          H     
    ldy zp_stack_ptr                                                  ; ac03: a4 04       ..    
    ldx zp_stack_ptr_1                                                ; ac05: a6 05       ..    
    iny                                                               ; ac07: c8          .     
    sty zp_text_ptr2                                                  ; ac08: 84 19       ..    
    sty zp_general                                                    ; ac0a: 84 37       .7    
    bne cac0f                                                         ; ac0c: d0 01       ..    
    inx                                                               ; ac0e: e8          .     
; &ac0f referenced 1 time by &ac0c
.cac0f
    stx l001a                                                         ; ac0f: 86 1a       ..    
    stx l0038                                                         ; ac11: 86 38       .8    
    ldy #&ff                                                          ; ac13: a0 ff       ..    
    sty zp_fwb_sign                                                   ; ac15: 84 3b       .;    
    iny                                                               ; ac17: c8          .     
    sty zp_text_ptr2_off                                              ; ac18: 84 1b       ..    
    jsr sub_c8955                                                     ; ac1a: 20 55 89     U.   
    jsr sub_c9b29                                                     ; ac1d: 20 29 9b     ).   
    jsr cbddc                                                         ; ac20: 20 dc bd     ..   
; &ac23 referenced 1 time by &ac75
.cac23
    pla                                                               ; ac23: 68          h     
    sta zp_text_ptr2_off                                              ; ac24: 85 1b       ..    
    pla                                                               ; ac26: 68          h     
    sta l001a                                                         ; ac27: 85 1a       ..    
    pla                                                               ; ac29: 68          h     
    sta zp_text_ptr2                                                  ; ac2a: 85 19       ..    
    lda zp_var_type                                                   ; ac2c: a5 27       .'    
    rts                                                               ; ac2e: 60          `     
; ***************************************************************************************
; VAL
;
; Number parsed from the start of a string. VAL string.
.fn_val
    jsr eval_factor                                                   ; ac2f: 20 ec ad     ..   
    bne cac9b                                                         ; ac32: d0 67       .g    
; ***************************************************************************************
; Convert an ASCII number to a value
;
; Convert the ASCII number in the string work area to a value: an integer in IWA or a
; real in FWA. Underlies VAL and numeric tokenising. A binary zero is appended to the
; SWA.
;
; On Entry:
;     ZP_STRBUF_LEN (&36): length of the ASCII number in the SWA
;     STRING WORK AREA (&0600): the ASCII number
;
; On Exit:
;     ZP_IWA / ZP_FWA: the result (integer or real)
;     A, ZP_VAR_TYPE (&27): type: &40 = integer, &FF = real
; &ac34 referenced 1 time by &bad3
.ascii_to_number
    ldy zp_strbuf_len                                                 ; ac34: a4 36       .6    
    lda #0                                                            ; ac36: a9 00       ..    
    sta string_work,y                                                 ; ac38: 99 00 06    ...   
    lda zp_text_ptr2                                                  ; ac3b: a5 19       ..    
    pha                                                               ; ac3d: 48          H     
    lda l001a                                                         ; ac3e: a5 1a       ..    
    pha                                                               ; ac40: 48          H     
    lda zp_text_ptr2_off                                              ; ac41: a5 1b       ..    
    pha                                                               ; ac43: 48          H     
    lda #0                                                            ; ac44: a9 00       ..    
    sta zp_text_ptr2_off                                              ; ac46: 85 1b       ..    
    lda #0                                                            ; ac48: a9 00       ..    
    sta zp_text_ptr2                                                  ; ac4a: 85 19       ..    
    lda #6                                                            ; ac4c: a9 06       ..    
    sta l001a                                                         ; ac4e: 85 1a       ..    
    jsr skip_spaces_ptr2                                              ; ac50: 20 8c 8a     ..   
    cmp #&2d ; '-'                                                    ; ac53: c9 2d       .-    
    beq cac66                                                         ; ac55: f0 0f       ..    
    cmp #&2b ; '+'                                                    ; ac57: c9 2b       .+    
    bne cac5e                                                         ; ac59: d0 03       ..    
    jsr skip_spaces_ptr2                                              ; ac5b: 20 8c 8a     ..   
; &ac5e referenced 1 time by &ac59
.cac5e
    dec zp_text_ptr2_off                                              ; ac5e: c6 1b       ..    
    jsr sub_ca07b                                                     ; ac60: 20 7b a0     {.   
    jmp cac73                                                         ; ac63: 4c 73 ac    Ls.   
; &ac66 referenced 1 time by &ac55
.cac66
    jsr skip_spaces_ptr2                                              ; ac66: 20 8c 8a     ..   
    dec zp_text_ptr2_off                                              ; ac69: c6 1b       ..    
    jsr sub_ca07b                                                     ; ac6b: 20 7b a0     {.   
    bcc cac73                                                         ; ac6e: 90 03       ..    
    jsr sub_cad8f                                                     ; ac70: 20 8f ad     ..   
; &ac73 referenced 2 times by &ac63, &ac6e
.cac73
    sta zp_var_type                                                   ; ac73: 85 27       .'    
    jmp cac23                                                         ; ac75: 4c 23 ac    L#.   
; ***************************************************************************************
; INT
;
; Integer part (floor) of a number. INT numeric.
.fn_int
    jsr eval_factor                                                   ; ac78: 20 ec ad     ..   
    beq cac9b                                                         ; ac7b: f0 1e       ..    
    bpl return_30                                                     ; ac7d: 10 1b       ..    
    lda zp_fwa_sign                                                   ; ac7f: a5 2e       ..    
    php                                                               ; ac81: 08          .     
    jsr fwa_to_int2                                                   ; ac82: 20 fe a3     ..   
    plp                                                               ; ac85: 28          (     
    bpl cac95                                                         ; ac86: 10 0d       ..    
    lda zp_fwb_m1                                                     ; ac88: a5 3e       .>    
    ora zp_fwb_m2                                                     ; ac8a: 05 3f       .?    
    ora zp_fwb_m3                                                     ; ac8c: 05 40       .@    
    ora zp_fwb_m4                                                     ; ac8e: 05 41       .A    
    beq cac95                                                         ; ac90: f0 03       ..    
    jsr sub_ca4c7                                                     ; ac92: 20 c7 a4     ..   
; &ac95 referenced 2 times by &ac86, &ac90
.cac95
    jsr sub_ca3e7                                                     ; ac95: 20 e7 a3     ..   
    lda #&40 ; '@'                                                    ; ac98: a9 40       .@    
; &ac9a referenced 1 time by &ac7d
.return_30
    rts                                                               ; ac9a: 60          `     
; &ac9b referenced 5 times by &ac32, &ac7b, &aca1, &ace5, &acf3
.cac9b
    jmp c8c0e                                                         ; ac9b: 4c 0e 8c    L..   
; ***************************************************************************************
; ASC
;
; ASCII code of the first character of a string, or -1 if empty. ASC string.
.fn_asc
    jsr eval_factor                                                   ; ac9e: 20 ec ad     ..   
    bne cac9b                                                         ; aca1: d0 f8       ..    
    lda zp_strbuf_len                                                 ; aca3: a5 36       .6    
    beq fn_true                                                       ; aca5: f0 1d       ..    
    lda string_work                                                   ; aca7: ad 00 06    ...   
; &acaa referenced 1 time by &acc2
.loop_cacaa
    jmp caed8                                                         ; acaa: 4c d8 ae    L..   
; ***************************************************************************************
; INKEY
;
; Read a key within a time limit, test a key, or read the machine ID. INKEY numeric.
.fn_inkey
    jsr sub_cafad                                                     ; acad: 20 ad af     ..   
    cpy #0                                                            ; acb0: c0 00       ..    
    bne fn_true                                                       ; acb2: d0 10       ..    
    txa                                                               ; acb4: 8a          .     
    jmp iwa_from_ya                                                   ; acb5: 4c ea ae    L..   
; ***************************************************************************************
; EOF
;
; TRUE when at the end of an open file. EOF#channel.
.fn_eof
    jsr sub_cbfb5                                                     ; acb8: 20 b5 bf     ..   
    tax                                                               ; acbb: aa          .     
    lda #osbyte_check_eof                                             ; acbc: a9 7f       ..    
    jsr osbyte                                                        ; acbe: 20 f4 ff     ..      ; Check for end-of-file on file handle Y
    txa                                                               ; acc1: 8a          .        ; X=0 means EOF reached, X=&FF means data remaining
    beq loop_cacaa                                                    ; acc2: f0 e6       ..    
; ***************************************************************************************
; TRUE
;
; The constant TRUE (-1). Sets IWA = -1; this is also the ineg1 integer primitive.
; &acc4 referenced 3 times by &ab9d, &aca5, &acb2
.fn_true
    lda #&ff                                                          ; acc4: a9 ff       ..    
    sta zp_iwa                                                        ; acc6: 85 2a       .*    
    sta zp_iwa_1                                                      ; acc8: 85 2b       .+    
    sta zp_iwa_2                                                      ; acca: 85 2c       .,    
    sta zp_iwa_3                                                      ; accc: 85 2d       .-    
    lda #&40 ; '@'                                                    ; acce: a9 40       .@    
    rts                                                               ; acd0: 60          `     
; ***************************************************************************************
; NOT
;
; Bitwise NOT (one's complement) of an integer. NOT numeric.
.fn_not
    jsr sub_c92e3                                                     ; acd1: 20 e3 92     ..   
    ldx #3                                                            ; acd4: a2 03       ..    
; &acd6 referenced 1 time by &acdd
.loop_cacd6
    lda zp_iwa,x                                                      ; acd6: b5 2a       .*    
    eor #&ff                                                          ; acd8: 49 ff       I.    
    sta zp_iwa,x                                                      ; acda: 95 2a       .*    
    dex                                                               ; acdc: ca          .     
    bpl loop_cacd6                                                    ; acdd: 10 f7       ..    
    lda #&40 ; '@'                                                    ; acdf: a9 40       .@    
    rts                                                               ; ace1: 60          `     
; ***************************************************************************************
; INSTR
;
; Position of one string within another, optionally from a start. INSTR(a$, b$ [,n]).
.fn_instr
    jsr sub_c9b29                                                     ; ace2: 20 29 9b     ).   
    bne cac9b                                                         ; ace5: d0 b4       ..    
    cpx #&2c ; ','                                                    ; ace7: e0 2c       .,    
    bne cad03                                                         ; ace9: d0 18       ..    
    inc zp_text_ptr2_off                                              ; aceb: e6 1b       ..    
    jsr stack_string                                                  ; aced: 20 b2 bd     ..   
    jsr sub_c9b29                                                     ; acf0: 20 29 9b     ).   
    bne cac9b                                                         ; acf3: d0 a6       ..    
    lda #1                                                            ; acf5: a9 01       ..    
    sta zp_iwa                                                        ; acf7: 85 2a       .*    
    inc zp_text_ptr2_off                                              ; acf9: e6 1b       ..    
    cpx #&29 ; ')'                                                    ; acfb: e0 29       .)    
    beq cad12                                                         ; acfd: f0 13       ..    
    cpx #&2c ; ','                                                    ; acff: e0 2c       .,    
    beq cad06                                                         ; ad01: f0 03       ..    
; &ad03 referenced 1 time by &ace9
.cad03
    jmp c8aa2                                                         ; ad03: 4c a2 8a    L..   
; &ad06 referenced 1 time by &ad01
.cad06
    jsr stack_string                                                  ; ad06: 20 b2 bd     ..   
    jsr cae56                                                         ; ad09: 20 56 ae     V.   
    jsr coerce_to_integer                                             ; ad0c: 20 f0 92     ..   
    jsr sub_cbdcb                                                     ; ad0f: 20 cb bd     ..   
; &ad12 referenced 1 time by &acfd
.cad12
    ldy #0                                                            ; ad12: a0 00       ..    
    ldx zp_iwa                                                        ; ad14: a6 2a       .*    
    bne cad1a                                                         ; ad16: d0 02       ..    
    ldx #1                                                            ; ad18: a2 01       ..    
; &ad1a referenced 1 time by &ad16
.cad1a
    stx zp_iwa                                                        ; ad1a: 86 2a       .*    
    txa                                                               ; ad1c: 8a          .     
    dex                                                               ; ad1d: ca          .     
    stx zp_iwa_3                                                      ; ad1e: 86 2d       .-    
    clc                                                               ; ad20: 18          .     
    adc zp_stack_ptr                                                  ; ad21: 65 04       e.    
    sta zp_general                                                    ; ad23: 85 37       .7    
    tya                                                               ; ad25: 98          .     
    adc zp_stack_ptr_1                                                ; ad26: 65 05       e.    
    sta l0038                                                         ; ad28: 85 38       .8    
    lda (zp_stack_ptr),y                                              ; ad2a: b1 04       ..    
    sec                                                               ; ad2c: 38          8     
    sbc zp_iwa_3                                                      ; ad2d: e5 2d       .-    
    bcc cad52                                                         ; ad2f: 90 21       .!    
    sbc zp_strbuf_len                                                 ; ad31: e5 36       .6    
    bcc cad52                                                         ; ad33: 90 1d       ..    
    adc #0                                                            ; ad35: 69 00       i.    
    sta zp_iwa_1                                                      ; ad37: 85 2b       .+    
    jsr cbddc                                                         ; ad39: 20 dc bd     ..   
; &ad3c referenced 2 times by &ad61, &ad65
.cad3c
    ldy #0                                                            ; ad3c: a0 00       ..    
    ldx zp_strbuf_len                                                 ; ad3e: a6 36       .6    
    beq cad4d                                                         ; ad40: f0 0b       ..    
; &ad42 referenced 1 time by &ad4b
.loop_cad42
    lda (zp_general),y                                                ; ad42: b1 37       .7    
    cmp string_work,y                                                 ; ad44: d9 00 06    ...   
    bne cad59                                                         ; ad47: d0 10       ..    
    iny                                                               ; ad49: c8          .     
    dex                                                               ; ad4a: ca          .     
    bne loop_cad42                                                    ; ad4b: d0 f5       ..    
; &ad4d referenced 1 time by &ad40
.cad4d
    lda zp_iwa                                                        ; ad4d: a5 2a       .*    
; &ad4f referenced 1 time by &ad57
.loop_cad4f
    jmp caed8                                                         ; ad4f: 4c d8 ae    L..   
; &ad52 referenced 2 times by &ad2f, &ad33
.cad52
    jsr cbddc                                                         ; ad52: 20 dc bd     ..   
; &ad55 referenced 1 time by &ad5d
.loop_cad55
    lda #0                                                            ; ad55: a9 00       ..    
    beq loop_cad4f                                                    ; ad57: f0 f6       ..    
; &ad59 referenced 1 time by &ad47
.cad59
    inc zp_iwa                                                        ; ad59: e6 2a       .*    
    dec zp_iwa_1                                                      ; ad5b: c6 2b       .+    
    beq loop_cad55                                                    ; ad5d: f0 f6       ..    
    inc zp_general                                                    ; ad5f: e6 37       .7    
    bne cad3c                                                         ; ad61: d0 d9       ..    
    inc l0038                                                         ; ad63: e6 38       .8    
    bne cad3c                                                         ; ad65: d0 d5       ..    
; &ad67 referenced 2 times by &ad6d, &ad8f
.cad67
    jmp c8c0e                                                         ; ad67: 4c 0e 8c    L..   
; ***************************************************************************************
; ABS
;
; Absolute value of a number. ABS numeric.
.fn_abs
    jsr eval_factor                                                   ; ad6a: 20 ec ad     ..   
    beq cad67                                                         ; ad6d: f0 f8       ..    
    bmi cad77                                                         ; ad6f: 30 06       0.    
; ***************************************************************************************
; Make the integer accumulator positive
;
; IWA = ABS(IWA).
;
; On Entry:
;     ZP_IWA (&2A): 32-bit integer
;
; On Exit:
;     ZP_IWA: made positive
;     X: preserved
; &ad71 referenced 4 times by &99c5, &99d8, &9d70, &9d80
.iwa_abs
    bit zp_iwa_3                                                      ; ad71: 24 2d       $-    
    bmi iwa_negate                                                    ; ad73: 30 1e       0.    
    bpl cadaa                                                         ; ad75: 10 33       .3    
; &ad77 referenced 1 time by &ad6f
.cad77
    jsr fwa_sign                                                      ; ad77: 20 da a1     ..   
    bpl cad89                                                         ; ad7a: 10 0d       ..    
    bmi cad83                                                         ; ad7c: 30 05       0.    
; ***************************************************************************************
; FWA = -FWA
;
; Negate the floating-point accumulator.
; &ad7e referenced 5 times by &a4d3, &a4fd, &a933, &a9a7, &ad91
.fwa_negate
    jsr fwa_sign                                                      ; ad7e: 20 da a1     ..   
    beq cad89                                                         ; ad81: f0 06       ..    
; &ad83 referenced 1 time by &ad7c
.cad83
    lda zp_fwa_sign                                                   ; ad83: a5 2e       ..    
    eor #&80                                                          ; ad85: 49 80       I.    
    sta zp_fwa_sign                                                   ; ad87: 85 2e       ..    
; &ad89 referenced 2 times by &ad7a, &ad81
.cad89
    lda #&ff                                                          ; ad89: a9 ff       ..    
    rts                                                               ; ad8b: 60          `     
; &ad8c referenced 1 time by &adf8
.loop_cad8c
    jsr sub_cae02                                                     ; ad8c: 20 02 ae     ..   
; &ad8f referenced 1 time by &ac70
.sub_cad8f
    beq cad67                                                         ; ad8f: f0 d6       ..    
    bmi fwa_negate                                                    ; ad91: 30 eb       0.    
; ***************************************************************************************
; Negate the integer accumulator
;
; IWA = -IWA (two's-complement negate the 32-bit integer).
;
; On Entry:
;     ZP_IWA (&2A): 32-bit integer
;
; On Exit:
;     ZP_IWA: negated
;     X: preserved (A, Y, P destroyed)
; &ad93 referenced 3 times by &9dc3, &a2c8, &ad73
.iwa_negate
    sec                                                               ; ad93: 38          8     
    lda #0                                                            ; ad94: a9 00       ..    
    tay                                                               ; ad96: a8          .     
    sbc zp_iwa                                                        ; ad97: e5 2a       .*    
    sta zp_iwa                                                        ; ad99: 85 2a       .*    
    tya                                                               ; ad9b: 98          .     
    sbc zp_iwa_1                                                      ; ad9c: e5 2b       .+    
    sta zp_iwa_1                                                      ; ad9e: 85 2b       .+    
    tya                                                               ; ada0: 98          .     
    sbc zp_iwa_2                                                      ; ada1: e5 2c       .,    
    sta zp_iwa_2                                                      ; ada3: 85 2c       .,    
    tya                                                               ; ada5: 98          .     
    sbc zp_iwa_3                                                      ; ada6: e5 2d       .-    
    sta zp_iwa_3                                                      ; ada8: 85 2d       .-    
; &adaa referenced 1 time by &ad75
.cadaa
    lda #&40 ; '@'                                                    ; adaa: a9 40       .@    
    rts                                                               ; adac: 60          `     
; &adad referenced 2 times by &baba, &bb38
.sub_cadad
    jsr skip_spaces_ptr2                                              ; adad: 20 8c 8a     ..   
    cmp #&22                                                          ; adb0: c9 22       ."    
    beq cadc9                                                         ; adb2: f0 15       ..    
    ldx #0                                                            ; adb4: a2 00       ..    
; &adb6 referenced 1 time by &adc3
.loop_cadb6
    lda (zp_text_ptr2),y                                              ; adb6: b1 19       ..    
    sta string_work,x                                                 ; adb8: 9d 00 06    ...   
    iny                                                               ; adbb: c8          .     
    inx                                                               ; adbc: e8          .     
    cmp #&0d                                                          ; adbd: c9 0d       ..    
    beq cadc5                                                         ; adbf: f0 04       ..    
    cmp #&2c ; ','                                                    ; adc1: c9 2c       .,    
    bne loop_cadb6                                                    ; adc3: d0 f1       ..    
; &adc5 referenced 1 time by &adbf
.cadc5
    dey                                                               ; adc5: 88          .     
    jmp cade1                                                         ; adc6: 4c e1 ad    L..   
; &adc9 referenced 2 times by &adb2, &adfc
.cadc9
    ldx #0                                                            ; adc9: a2 00       ..    
; &adcb referenced 1 time by &addf
.loop_cadcb
    iny                                                               ; adcb: c8          .     
; &adcc referenced 1 time by &add9
.loop_cadcc
    lda (zp_text_ptr2),y                                              ; adcc: b1 19       ..    
    cmp #&0d                                                          ; adce: c9 0d       ..    
    beq cade9                                                         ; add0: f0 17       ..    
    iny                                                               ; add2: c8          .     
    sta string_work,x                                                 ; add3: 9d 00 06    ...   
    inx                                                               ; add6: e8          .     
    cmp #&22                                                          ; add7: c9 22       ."    
    bne loop_cadcc                                                    ; add9: d0 f1       ..    
    lda (zp_text_ptr2),y                                              ; addb: b1 19       ..    
    cmp #&22                                                          ; addd: c9 22       ."    
    beq loop_cadcb                                                    ; addf: f0 ea       ..    
; &ade1 referenced 1 time by &adc6
.cade1
    dex                                                               ; ade1: ca          .     
    stx zp_strbuf_len                                                 ; ade2: 86 36       .6    
    sty zp_text_ptr2_off                                              ; ade4: 84 1b       ..    
    lda #0                                                            ; ade6: a9 00       ..    
    rts                                                               ; ade8: 60          `     
; &ade9 referenced 1 time by &add0
.cade9
    jmp c8e98                                                         ; ade9: 4c 98 8e    L..   
; ***************************************************************************************
; Evaluate a factor (evaluator level 1)
;
; Evaluate the highest-precedence level of an expression at PtrB: unary minus, unary plus
; and NOT; parenthesised sub-expressions; the ?, !, $ and | indirection operators; string
; literals; and the built-in functions.
; &adec referenced 13 times by &92e3, &92fa, &9e20, &ab88, &abe9, &ac2f, &ac78, &ac9e, &ad6a, &adf4, &aed1, &b0a3, &bf83
.eval_factor
    ldy zp_text_ptr2_off                                              ; adec: a4 1b       ..    
    inc zp_text_ptr2_off                                              ; adee: e6 1b       ..    
    lda (zp_text_ptr2),y                                              ; adf0: b1 19       ..    
    cmp #&20 ; ' '                                                    ; adf2: c9 20       .     
    beq eval_factor                                                   ; adf4: f0 f6       ..    
    cmp #&2d ; '-'                                                    ; adf6: c9 2d       .-    
    beq loop_cad8c                                                    ; adf8: f0 92       ..    
    cmp #&22                                                          ; adfa: c9 22       ."    
    beq cadc9                                                         ; adfc: f0 cb       ..    
    cmp #&2b ; '+'                                                    ; adfe: c9 2b       .+    
    bne cae05                                                         ; ae00: d0 03       ..    
; &ae02 referenced 1 time by &ad8c
.sub_cae02
    jsr skip_spaces_ptr2                                              ; ae02: 20 8c 8a     ..   
; &ae05 referenced 1 time by &ae00
.cae05
    cmp #&8e                                                          ; ae05: c9 8e       ..    
    bcc cae10                                                         ; ae07: 90 07       ..    
    cmp #&c6                                                          ; ae09: c9 c6       ..    
    bcs cae43                                                         ; ae0b: b0 36       .6    
    jmp dispatch_token                                                ; ae0d: 4c b1 8b    L..   
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
    dec zp_text_ptr2_off                                              ; ae20: c6 1b       ..    
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
    lda zp_opt_flag                                                   ; ae30: a5 28       .(    
    and #2                                                            ; ae32: 29 02       ).    
    bne cae43                                                         ; ae34: d0 0d       ..    
    bcs cae43                                                         ; ae36: b0 0b       ..    
    stx zp_text_ptr2_off                                              ; ae38: 86 1b       ..    
; &ae3a referenced 1 time by &85af
.sub_cae3a
    lda resint_p                                                      ; ae3a: ad 40 04    .@.   
    ldy l0441                                                         ; ae3d: ac 41 04    .A.   
    jmp iwa_from_ya                                                   ; ae40: 4c ea ae    L..   
; &ae43 referenced 6 times by &8f1b, &ae0b, &ae2d, &ae34, &ae36, &aec7
.cae43
    brk                                                               ; ae43: 00          .     
    equb &1a                                                          ; ae44: 1a          .     
    equs "No such variable"                                           ; ae45: 4e 6f 20... No ...
    equb &00                                                          ; ae55: 00          .     
; &ae56 referenced 11 times by &8e2b, &9747, &976c, &ab4a, &ad09, &ae1e, &af0c, &afda, &affc, &b05b, &b0cb
.cae56
    jsr sub_c9b29                                                     ; ae56: 20 29 9b     ).   
    inc zp_text_ptr2_off                                              ; ae59: e6 1b       ..    
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
    stx zp_iwa                                                        ; ae6f: 86 2a       .*    
    stx zp_iwa_1                                                      ; ae71: 86 2b       .+    
    stx zp_iwa_2                                                      ; ae73: 86 2c       .,    
    stx zp_iwa_3                                                      ; ae75: 86 2d       .-    
    ldy zp_text_ptr2_off                                              ; ae77: a4 1b       ..    
; &ae79 referenced 1 time by &aea0
.loop_cae79
    lda (zp_text_ptr2),y                                              ; ae79: b1 19       ..    
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
    rol zp_iwa                                                        ; ae94: 26 2a       &*    
    rol zp_iwa_1                                                      ; ae96: 26 2b       &+    
    rol zp_iwa_2                                                      ; ae98: 26 2c       &,    
    rol zp_iwa_3                                                      ; ae9a: 26 2d       &-    
    dex                                                               ; ae9c: ca          .     
    bpl loop_cae93                                                    ; ae9d: 10 f4       ..    
    iny                                                               ; ae9f: c8          .     
    bne loop_cae79                                                    ; aea0: d0 d7       ..    
; &aea2 referenced 3 times by &ae7d, &ae87, &ae8b
.caea2
    txa                                                               ; aea2: 8a          .     
    bpl caeaa                                                         ; aea3: 10 05       ..    
    sty zp_text_ptr2_off                                              ; aea5: 84 1b       ..    
    lda #&40 ; '@'                                                    ; aea7: a9 40       .@    
    rts                                                               ; aea9: 60          `     
; &aeaa referenced 1 time by &aea3
.caeaa
    brk                                                               ; aeaa: 00          .     
    equb &1c                                                          ; aeab: 1c          .     
    equs "Bad HEX"                                                    ; aeac: 42 61 64... Bad...
    equb &00                                                          ; aeb3: 00          .     
; ***************************************************************************************
; =TIME
;
; Read the centisecond elapsed-time clock. TIME.
.fn_time
    ldx #<(zp_iwa)                                                    ; aeb4: a2 2a       .*    
    ldy #>(zp_iwa)                                                    ; aeb6: a0 00       ..    
    lda #osword_read_clock                                            ; aeb8: a9 01       ..    
    jsr osword                                                        ; aeba: 20 f1 ff     ..      ; Read system clock
    lda #&40 ; '@'                                                    ; aebd: a9 40       .@    
    rts                                                               ; aebf: 60          `     
; ***************************************************************************************
; =PAGE
;
; Read PAGE, the start of the BASIC program. PAGE.
.fn_page
    lda #0                                                            ; aec0: a9 00       ..    
    ldy zp_page                                                       ; aec2: a4 18       ..    
    jmp iwa_from_ya                                                   ; aec4: 4c ea ae    L..   
; &aec7 referenced 1 time by &aee2
.loop_caec7
    jmp cae43                                                         ; aec7: 4c 43 ae    LC.   
; ***************************************************************************************
; FALSE
;
; The constant FALSE (0). Sets IWA = 0; this is also the izero integer primitive.
.fn_false
    lda #0                                                            ; aeca: a9 00       ..    
    beq caed8                                                         ; aecc: f0 0a       ..    
; &aece referenced 1 time by &aed4
.loop_caece
    jmp c8c0e                                                         ; aece: 4c 0e 8c    L..   
; ***************************************************************************************
; LEN
;
; Length of a string. LEN string.
.fn_len
    jsr eval_factor                                                   ; aed1: 20 ec ad     ..   
    bne loop_caece                                                    ; aed4: d0 f8       ..    
    lda zp_strbuf_len                                                 ; aed6: a5 36       .6    
; &aed8 referenced 18 times by &8f6b, &8f76, &9182, &9339, &96f8, &ab6a, &ab73, &ab7c, &aba2, &acaa, &ad4f, &aecc, &aef9, &afbc, &b5a9, &b810, &bf75, &bf93
.caed8
    ldy #0                                                            ; aed8: a0 00       ..    
    beq iwa_from_ya                                                   ; aeda: f0 0e       ..    
; ***************************************************************************************
; TO
;
; The TO keyword of FOR. It has no standalone action; reaching it as a statement token is
; an error.
.fn_to
    ldy zp_text_ptr2_off                                              ; aedc: a4 1b       ..    
    lda (zp_text_ptr2),y                                              ; aede: b1 19       ..    
    cmp #&50 ; 'P'                                                    ; aee0: c9 50       .P    
    bne loop_caec7                                                    ; aee2: d0 e3       ..    
    inc zp_text_ptr2_off                                              ; aee4: e6 1b       ..    
    lda zp_top                                                        ; aee6: a5 12       ..    
    ldy l0013                                                         ; aee8: a4 13       ..    
; ***************************************************************************************
; Set the integer accumulator to a small integer
;
; IWA = 256*Y + A.
;
; On Entry:
;     A: low byte
;     Y: high byte
;
; On Exit:
;     ZP_IWA: 256*Y + A (sign-extended)
; &aeea referenced 11 times by &98a4, &ab3e, &acb5, &ae40, &aec4, &aeda, &af00, &af07, &afa3, &afaa, &b351
.iwa_from_ya
    sta zp_iwa                                                        ; aeea: 85 2a       .*    
    sty zp_iwa_1                                                      ; aeec: 84 2b       .+    
    lda #0                                                            ; aeee: a9 00       ..       ; Clear the top 16 bits: the result is 0-65535
    sta zp_iwa_2                                                      ; aef0: 85 2c       .,    
    sta zp_iwa_3                                                      ; aef2: 85 2d       .-    
    lda #&40 ; '@'                                                    ; aef4: a9 40       .@       ; Report the value as an integer (type &40)
    rts                                                               ; aef6: 60          `     
; ***************************************************************************************
; COUNT
;
; Characters printed since the last newline. COUNT.
.fn_count
    lda zp_count                                                      ; aef7: a5 1e       ..    
    jmp caed8                                                         ; aef9: 4c d8 ae    L..   
; ***************************************************************************************
; =LOMEM
;
; Read LOMEM, the start of variable storage. LOMEM.
.fn_lomem
    lda zp_lomem                                                      ; aefc: a5 00       ..    
    ldy l0001                                                         ; aefe: a4 01       ..    
    jmp iwa_from_ya                                                   ; af00: 4c ea ae    L..   
; ***************************************************************************************
; =HIMEM
;
; Read HIMEM, the top of memory for BASIC. HIMEM.
.fn_himem
    lda zp_himem                                                      ; af03: a5 06       ..    
    ldy l0007                                                         ; af05: a4 07       ..    
    jmp iwa_from_ya                                                   ; af07: 4c ea ae    L..   
; &af0a referenced 1 time by &af4f
.loop_caf0a
    inc zp_text_ptr2_off                                              ; af0a: e6 1b       ..    
    jsr cae56                                                         ; af0c: 20 56 ae     V.   
    jsr coerce_to_integer                                             ; af0f: 20 f0 92     ..   
    lda zp_iwa_3                                                      ; af12: a5 2d       .-    
    bmi rnd_seed                                                      ; af14: 30 29       0)    
    ora zp_iwa_2                                                      ; af16: 05 2c       .,    
    ora zp_iwa_1                                                      ; af18: 05 2b       .+    
    bne rnd_range                                                     ; af1a: d0 08       ..    
    lda zp_iwa                                                        ; af1c: a5 2a       .*    
    beq rnd_repeat                                                    ; af1e: f0 4c       .L    
    cmp #1                                                            ; af20: c9 01       ..    
    beq rnd_fraction                                                  ; af22: f0 45       .E    
; ***************************************************************************************
; RND(X): random integer 1 to X
;
; Step the generator; IWA = a random integer from 1 to X.
; &af24 referenced 1 time by &af1a
.rnd_range
    jsr int_to_fwa                                                    ; af24: 20 be a2     ..   
    jsr stack_real                                                    ; af27: 20 51 bd     Q.   
    jsr rnd_fraction                                                  ; af2a: 20 69 af     i.   
    jsr sub_cbd7e                                                     ; af2d: 20 7e bd     ~.   
    jsr fwa_mul_var_raw                                               ; af30: 20 06 a6     ..   
    jsr fwa_normalise                                                 ; af33: 20 03 a3     ..   
    jsr fwa_to_int                                                    ; af36: 20 e4 a3     ..   
    jsr sub_c9222                                                     ; af39: 20 22 92     ".   
    lda #&40 ; '@'                                                    ; af3c: a9 40       .@    
    rts                                                               ; af3e: 60          `     
; ***************************************************************************************
; RND(-X): seed the generator
;
; Seed the random work area from X (RND(-X)).
; &af3f referenced 1 time by &af14
.rnd_seed
    ldx #&0d                                                          ; af3f: a2 0d       ..    
    jsr iwa_store_zp                                                  ; af41: 20 44 be     D.   
    lda #&40 ; '@'                                                    ; af44: a9 40       .@    
    sta l0011                                                         ; af46: 85 11       ..    
    rts                                                               ; af48: 60          `     
; ***************************************************************************************
; RND
;
; Random number; the form depends on the argument (see rnd_*). RND[(numeric)].
.fn_rnd
    ldy zp_text_ptr2_off                                              ; af49: a4 1b       ..    
    lda (zp_text_ptr2),y                                              ; af4b: b1 19       ..    
    cmp #&28 ; '('                                                    ; af4d: c9 28       .(    
    beq loop_caf0a                                                    ; af4f: f0 b9       ..    
; ***************************************************************************************
; RND: random 32-bit integer
;
; Step the generator; IWA = a full-range random integer.
.rnd_integer
    jsr sub_caf87                                                     ; af51: 20 87 af     ..   
    ldx #&0d                                                          ; af54: a2 0d       ..    
; ***************************************************************************************
; Load a zero-page integer variable into the accumulator
;
; Copy a 4-byte integer from a zero-page location into IWA.
; &af56 referenced 2 times by &9dbd, &b326
.iwa_load_zp
    lda zp_lomem,x                                                    ; af56: b5 00       ..    
    sta zp_iwa                                                        ; af58: 85 2a       .*    
    lda l0001,x                                                       ; af5a: b5 01       ..    
    sta zp_iwa_1                                                      ; af5c: 85 2b       .+    
    lda zp_vartop,x                                                   ; af5e: b5 02       ..    
    sta zp_iwa_2                                                      ; af60: 85 2c       .,    
    lda zp_vartop_1,x                                                 ; af62: b5 03       ..    
    sta zp_iwa_3                                                      ; af64: 85 2d       .-    
    lda #&40 ; '@'                                                    ; af66: a9 40       .@    
    rts                                                               ; af68: 60          `     
; ***************************************************************************************
; RND(1): random fraction
;
; Step the generator; FWA = a real in 0 to 0.999999.
; &af69 referenced 2 times by &af22, &af2a
.rnd_fraction
    jsr sub_caf87                                                     ; af69: 20 87 af     ..   
; ***************************************************************************************
; RND(0): repeat the last RND(1)
;
; FWA = the value last returned by rnd_fraction.
; &af6c referenced 1 time by &af1e
.rnd_repeat
    ldx #0                                                            ; af6c: a2 00       ..    
    stx zp_fwa_sign                                                   ; af6e: 86 2e       ..    
    stx zp_fwa_ovf                                                    ; af70: 86 2f       ./    
    stx zp_fwa_rnd                                                    ; af72: 86 35       .5    
    lda #&80                                                          ; af74: a9 80       ..    
    sta zp_fwa_exp                                                    ; af76: 85 30       .0    
; &af78 referenced 1 time by &af7f
.loop_caf78
    lda zp_rnd_seed,x                                                 ; af78: b5 0d       ..    
    sta zp_fwa_m1,x                                                   ; af7a: 95 31       .1    
    inx                                                               ; af7c: e8          .     
    cpx #4                                                            ; af7d: e0 04       ..    
    bne loop_caf78                                                    ; af7f: d0 f7       ..    
    jsr ca659                                                         ; af81: 20 59 a6     Y.   
    lda #&ff                                                          ; af84: a9 ff       ..    
    rts                                                               ; af86: 60          `     
; &af87 referenced 2 times by &af51, &af69
.sub_caf87
    ldy #&20 ; ' '                                                    ; af87: a0 20       .     
; &af89 referenced 1 time by &af9c
.loop_caf89
    lda l000f                                                         ; af89: a5 0f       ..    
    lsr a                                                             ; af8b: 4a          J     
    lsr a                                                             ; af8c: 4a          J     
    lsr a                                                             ; af8d: 4a          J     
    eor l0011                                                         ; af8e: 45 11       E.    
    ror a                                                             ; af90: 6a          j     
    rol zp_rnd_seed                                                   ; af91: 26 0d       &.    
    rol l000e                                                         ; af93: 26 0e       &.    
    rol l000f                                                         ; af95: 26 0f       &.    
    rol l0010                                                         ; af97: 26 10       &.    
    rol l0011                                                         ; af99: 26 11       &.    
    dey                                                               ; af9b: 88          .     
    bne loop_caf89                                                    ; af9c: d0 eb       ..    
    rts                                                               ; af9e: 60          `     
; ***************************************************************************************
; ERL
;
; Line number where the last error occurred. ERL.
.fn_erl
    ldy l0009                                                         ; af9f: a4 09       ..    
    lda zp_erl                                                        ; afa1: a5 08       ..    
    jmp iwa_from_ya                                                   ; afa3: 4c ea ae    L..   
; ***************************************************************************************
; ERR
;
; Error number of the last error. ERR.
.fn_err
    ldy #0                                                            ; afa6: a0 00       ..    
    lda (l00fd),y                                                     ; afa8: b1 fd       ..    
    jmp iwa_from_ya                                                   ; afaa: 4c ea ae    L..   
; &afad referenced 2 times by &acad, &b026
.sub_cafad
    jsr sub_c92e3                                                     ; afad: 20 e3 92     ..   
    lda #osbyte_inkey                                                 ; afb0: a9 81       ..    
    ldx zp_iwa                                                        ; afb2: a6 2a       .*    
    ldy zp_iwa_1                                                      ; afb4: a4 2b       .+    
    jmp osbyte                                                        ; afb6: 4c f4 ff    L..      ; INKEY: Scan for a key with positive X, or read internal key number EOR 128 for negative X
; ***************************************************************************************
; GET
;
; Wait for a key and return its ASCII code. GET.
.fn_get
    jsr osrdch                                                        ; afb9: 20 e0 ff     ..      ; X=ASCII code typed (positive timeout) or internal key number EOR 128 (negative scan) / Y=0 if a key was pressed, Y=&FF on time-out, Y=&1B on Escape
    jmp caed8                                                         ; afbc: 4c d8 ae    L..   
; ***************************************************************************************
; GET$
;
; Read a key as a one-character string, or a byte / line from a file. GET$[#channel].
.fn_gets
    jsr osrdch                                                        ; afbf: 20 e0 ff     ..   
; &afc2 referenced 2 times by &b02c, &b3c2
.cafc2
    sta string_work                                                   ; afc2: 8d 00 06    ...   
    lda #1                                                            ; afc5: a9 01       ..    
    sta zp_strbuf_len                                                 ; afc7: 85 36       .6    
    lda #0                                                            ; afc9: a9 00       ..    
    rts                                                               ; afcb: 60          `     
; ***************************************************************************************
; LEFT$
;
; Leftmost n characters of a string. LEFT$(string, n).
.fn_lefts
    jsr sub_c9b29                                                     ; afcc: 20 29 9b     ).   
    bne cb033                                                         ; afcf: d0 62       .b    
    cpx #&2c ; ','                                                    ; afd1: e0 2c       .,    
    bne cb036                                                         ; afd3: d0 61       .a    
    inc zp_text_ptr2_off                                              ; afd5: e6 1b       ..    
    jsr stack_string                                                  ; afd7: 20 b2 bd     ..   
    jsr cae56                                                         ; afda: 20 56 ae     V.   
    jsr coerce_to_integer                                             ; afdd: 20 f0 92     ..   
    jsr sub_cbdcb                                                     ; afe0: 20 cb bd     ..   
    lda zp_iwa                                                        ; afe3: a5 2a       .*    
    cmp zp_strbuf_len                                                 ; afe5: c5 36       .6    
    bcs cafeb                                                         ; afe7: b0 02       ..    
    sta zp_strbuf_len                                                 ; afe9: 85 36       .6    
; &afeb referenced 1 time by &afe7
.cafeb
    lda #0                                                            ; afeb: a9 00       ..    
    rts                                                               ; afed: 60          `     
; ***************************************************************************************
; RIGHT$
;
; Rightmost n characters of a string. RIGHT$(string, n).
.fn_rights
    jsr sub_c9b29                                                     ; afee: 20 29 9b     ).   
    bne cb033                                                         ; aff1: d0 40       .@    
    cpx #&2c ; ','                                                    ; aff3: e0 2c       .,    
    bne cb036                                                         ; aff5: d0 3f       .?    
    inc zp_text_ptr2_off                                              ; aff7: e6 1b       ..    
    jsr stack_string                                                  ; aff9: 20 b2 bd     ..   
    jsr cae56                                                         ; affc: 20 56 ae     V.   
    jsr coerce_to_integer                                             ; afff: 20 f0 92     ..   
    jsr sub_cbdcb                                                     ; b002: 20 cb bd     ..   
    lda zp_strbuf_len                                                 ; b005: a5 36       .6    
    sec                                                               ; b007: 38          8     
    sbc zp_iwa                                                        ; b008: e5 2a       .*    
    bcc cb023                                                         ; b00a: 90 17       ..    
    beq return_31                                                     ; b00c: f0 17       ..    
    tax                                                               ; b00e: aa          .     
    lda zp_iwa                                                        ; b00f: a5 2a       .*    
    sta zp_strbuf_len                                                 ; b011: 85 36       .6    
    beq return_31                                                     ; b013: f0 10       ..    
    ldy #0                                                            ; b015: a0 00       ..    
; &b017 referenced 1 time by &b021
.loop_cb017
    lda string_work,x                                                 ; b017: bd 00 06    ...   
    sta string_work,y                                                 ; b01a: 99 00 06    ...   
    inx                                                               ; b01d: e8          .     
    iny                                                               ; b01e: c8          .     
    dec zp_iwa                                                        ; b01f: c6 2a       .*    
    bne loop_cb017                                                    ; b021: d0 f4       ..    
; &b023 referenced 1 time by &b00a
.cb023
    lda #0                                                            ; b023: a9 00       ..    
; &b025 referenced 2 times by &b00c, &b013
.return_31
    rts                                                               ; b025: 60          `     
; ***************************************************************************************
; INKEY$
;
; Read a key within a time limit as a string. INKEY$ numeric.
.fn_inkeys
    jsr sub_cafad                                                     ; b026: 20 ad af     ..   
    txa                                                               ; b029: 8a          .     
    cpy #0                                                            ; b02a: c0 00       ..    
    beq cafc2                                                         ; b02c: f0 94       ..    
; &b02e referenced 2 times by &b06b, &b081
.cb02e
    lda #0                                                            ; b02e: a9 00       ..    
    sta zp_strbuf_len                                                 ; b030: 85 36       .6    
    rts                                                               ; b032: 60          `     
; &b033 referenced 3 times by &afcf, &aff1, &b03c
.cb033
    jmp c8c0e                                                         ; b033: 4c 0e 8c    L..   
; &b036 referenced 4 times by &afd3, &aff5, &b040, &b059
.cb036
    jmp c8aa2                                                         ; b036: 4c a2 8a    L..   
; ***************************************************************************************
; MID$
;
; Substring from a start position. MID$(string, start [,length]).
.fn_mids
    jsr sub_c9b29                                                     ; b039: 20 29 9b     ).   
    bne cb033                                                         ; b03c: d0 f5       ..    
    cpx #&2c ; ','                                                    ; b03e: e0 2c       .,    
    bne cb036                                                         ; b040: d0 f4       ..    
    jsr stack_string                                                  ; b042: 20 b2 bd     ..   
    inc zp_text_ptr2_off                                              ; b045: e6 1b       ..    
    jsr sub_c92dd                                                     ; b047: 20 dd 92     ..   
    lda zp_iwa                                                        ; b04a: a5 2a       .*    
    pha                                                               ; b04c: 48          H     
    lda #&ff                                                          ; b04d: a9 ff       ..    
    sta zp_iwa                                                        ; b04f: 85 2a       .*    
    inc zp_text_ptr2_off                                              ; b051: e6 1b       ..    
    cpx #&29 ; ')'                                                    ; b053: e0 29       .)    
    beq cb061                                                         ; b055: f0 0a       ..    
    cpx #&2c ; ','                                                    ; b057: e0 2c       .,    
    bne cb036                                                         ; b059: d0 db       ..    
    jsr cae56                                                         ; b05b: 20 56 ae     V.   
    jsr coerce_to_integer                                             ; b05e: 20 f0 92     ..   
; &b061 referenced 1 time by &b055
.cb061
    jsr sub_cbdcb                                                     ; b061: 20 cb bd     ..   
    pla                                                               ; b064: 68          h     
    tay                                                               ; b065: a8          .     
    clc                                                               ; b066: 18          .     
    beq cb06f                                                         ; b067: f0 06       ..    
    sbc zp_strbuf_len                                                 ; b069: e5 36       .6    
    bcs cb02e                                                         ; b06b: b0 c1       ..    
    dey                                                               ; b06d: 88          .     
    tya                                                               ; b06e: 98          .     
; &b06f referenced 1 time by &b067
.cb06f
    sta zp_iwa_2                                                      ; b06f: 85 2c       .,    
    tax                                                               ; b071: aa          .     
    ldy #0                                                            ; b072: a0 00       ..    
    lda zp_strbuf_len                                                 ; b074: a5 36       .6    
    sec                                                               ; b076: 38          8     
    sbc zp_iwa_2                                                      ; b077: e5 2c       .,    
    cmp zp_iwa                                                        ; b079: c5 2a       .*    
    bcs cb07f                                                         ; b07b: b0 02       ..    
    sta zp_iwa                                                        ; b07d: 85 2a       .*    
; &b07f referenced 1 time by &b07b
.cb07f
    lda zp_iwa                                                        ; b07f: a5 2a       .*    
    beq cb02e                                                         ; b081: f0 ab       ..    
; &b083 referenced 1 time by &b08d
.loop_cb083
    lda string_work,x                                                 ; b083: bd 00 06    ...   
    sta string_work,y                                                 ; b086: 99 00 06    ...   
    iny                                                               ; b089: c8          .     
    inx                                                               ; b08a: e8          .     
    cpy zp_iwa                                                        ; b08b: c4 2a       .*    
    bne loop_cb083                                                    ; b08d: d0 f4       ..    
    sty zp_strbuf_len                                                 ; b08f: 84 36       .6    
    lda #0                                                            ; b091: a9 00       ..    
    rts                                                               ; b093: 60          `     
; ***************************************************************************************
; STR$
;
; String form of a number (STR$~ for hex). STR$[~] numeric.
.fn_strs
    jsr skip_spaces_ptr2                                              ; b094: 20 8c 8a     ..   
    ldy #&ff                                                          ; b097: a0 ff       ..    
    cmp #&7e ; '~'                                                    ; b099: c9 7e       .~    
    beq cb0a1                                                         ; b09b: f0 04       ..    
    ldy #0                                                            ; b09d: a0 00       ..    
    dec zp_text_ptr2_off                                              ; b09f: c6 1b       ..    
; &b0a1 referenced 1 time by &b09b
.cb0a1
    tya                                                               ; b0a1: 98          .     
    pha                                                               ; b0a2: 48          H     
    jsr eval_factor                                                   ; b0a3: 20 ec ad     ..   
    beq cb0bf                                                         ; b0a6: f0 17       ..    
    tay                                                               ; b0a8: a8          .     
    pla                                                               ; b0a9: 68          h     
    sta zp_print_flag                                                 ; b0aa: 85 15       ..    
    lda l0403                                                         ; b0ac: ad 03 04    ...   
    bne cb0b9                                                         ; b0af: d0 08       ..    
    sta zp_general                                                    ; b0b1: 85 37       .7    
    jsr c9ef9                                                         ; b0b3: 20 f9 9e     ..   
    lda #0                                                            ; b0b6: a9 00       ..    
    rts                                                               ; b0b8: 60          `     
; &b0b9 referenced 1 time by &b0af
.cb0b9
    jsr number_to_ascii                                               ; b0b9: 20 df 9e     ..   
    lda #0                                                            ; b0bc: a9 00       ..    
    rts                                                               ; b0be: 60          `     
; &b0bf referenced 2 times by &b0a6, &b0ce
.cb0bf
    jmp c8c0e                                                         ; b0bf: 4c 0e 8c    L..   
; ***************************************************************************************
; STRING$
;
; A string repeated n times. STRING$(n, string).
.fn_strings
    jsr sub_c92dd                                                     ; b0c2: 20 dd 92     ..   
    jsr stack_integer                                                 ; b0c5: 20 94 bd     ..   
    jsr skip_spaces_expect_comma                                      ; b0c8: 20 ae 8a     ..   
    jsr cae56                                                         ; b0cb: 20 56 ae     V.   
    bne cb0bf                                                         ; b0ce: d0 ef       ..    
    jsr unstack_integer                                               ; b0d0: 20 ea bd     ..   
    ldy zp_strbuf_len                                                 ; b0d3: a4 36       .6    
    beq cb0f5                                                         ; b0d5: f0 1e       ..    
    lda zp_iwa                                                        ; b0d7: a5 2a       .*    
    beq cb0f8                                                         ; b0d9: f0 1d       ..    
    dec zp_iwa                                                        ; b0db: c6 2a       .*    
    beq cb0f5                                                         ; b0dd: f0 16       ..    
; &b0df referenced 1 time by &b0f1
.loop_cb0df
    ldx #0                                                            ; b0df: a2 00       ..    
; &b0e1 referenced 1 time by &b0ed
.loop_cb0e1
    lda string_work,x                                                 ; b0e1: bd 00 06    ...   
    sta string_work,y                                                 ; b0e4: 99 00 06    ...   
    inx                                                               ; b0e7: e8          .     
    iny                                                               ; b0e8: c8          .     
    beq cb0fb                                                         ; b0e9: f0 10       ..    
    cpx zp_strbuf_len                                                 ; b0eb: e4 36       .6    
    bcc loop_cb0e1                                                    ; b0ed: 90 f2       ..    
    dec zp_iwa                                                        ; b0ef: c6 2a       .*    
    bne loop_cb0df                                                    ; b0f1: d0 ec       ..    
    sty zp_strbuf_len                                                 ; b0f3: 84 36       .6    
; &b0f5 referenced 2 times by &b0d5, &b0dd
.cb0f5
    lda #0                                                            ; b0f5: a9 00       ..    
    rts                                                               ; b0f7: 60          `     
; &b0f8 referenced 1 time by &b0d9
.cb0f8
    sta zp_strbuf_len                                                 ; b0f8: 85 36       .6    
    rts                                                               ; b0fa: 60          `     
; &b0fb referenced 1 time by &b0e9
.cb0fb
    jmp c9c03                                                         ; b0fb: 4c 03 9c    L..   
; &b0fe referenced 1 time by &b11e
.loop_cb0fe
    pla                                                               ; b0fe: 68          h     
    sta l000c                                                         ; b0ff: 85 0c       ..    
    pla                                                               ; b101: 68          h     
    sta zp_text_ptr                                                   ; b102: 85 0b       ..    
    brk                                                               ; b104: 00          .     
    equb &1d                                                          ; b105: 1d          .     
    equs "No such "                                                   ; b106: 4e 6f 20... No ...
    equb &a4, &2f, &f2, &00                                           ; b10e: a4 2f f2... ./....
; &b112 referenced 1 time by &b1e6
.cb112
    lda zp_page                                                       ; b112: a5 18       ..    
    sta l000c                                                         ; b114: 85 0c       ..    
    lda #0                                                            ; b116: a9 00       ..    
    sta zp_text_ptr                                                   ; b118: 85 0b       ..    
; &b11a referenced 2 times by &b136, &b13a
.cb11a
    ldy #1                                                            ; b11a: a0 01       ..    
    lda (zp_text_ptr),y                                               ; b11c: b1 0b       ..    
    bmi loop_cb0fe                                                    ; b11e: 30 de       0.    
    ldy #3                                                            ; b120: a0 03       ..    
; &b122 referenced 1 time by &b127
.loop_cb122
    iny                                                               ; b122: c8          .     
    lda (zp_text_ptr),y                                               ; b123: b1 0b       ..    
    cmp #&20 ; ' '                                                    ; b125: c9 20       .     
    beq loop_cb122                                                    ; b127: f0 f9       ..    
    cmp #&dd                                                          ; b129: c9 dd       ..    
    beq cb13c                                                         ; b12b: f0 0f       ..    
; &b12d referenced 2 times by &b15e, &b16a
.cb12d
    ldy #3                                                            ; b12d: a0 03       ..    
    lda (zp_text_ptr),y                                               ; b12f: b1 0b       ..    
    clc                                                               ; b131: 18          .     
    adc zp_text_ptr                                                   ; b132: 65 0b       e.    
    sta zp_text_ptr                                                   ; b134: 85 0b       ..    
    bcc cb11a                                                         ; b136: 90 e2       ..    
    inc l000c                                                         ; b138: e6 0c       ..    
    bcs cb11a                                                         ; b13a: b0 de       ..    
; &b13c referenced 1 time by &b12b
.cb13c
    iny                                                               ; b13c: c8          .     
    sty zp_text_ptr_off                                               ; b13d: 84 0a       ..    
    jsr skip_spaces                                                   ; b13f: 20 97 8a     ..   
    tya                                                               ; b142: 98          .     
    tax                                                               ; b143: aa          .     
    clc                                                               ; b144: 18          .     
    adc zp_text_ptr                                                   ; b145: 65 0b       e.    
    ldy l000c                                                         ; b147: a4 0c       ..    
    bcc cb14d                                                         ; b149: 90 02       ..    
    iny                                                               ; b14b: c8          .     
    clc                                                               ; b14c: 18          .     
; &b14d referenced 1 time by &b149
.cb14d
    sbc #0                                                            ; b14d: e9 00       ..    
    sta zp_fwb_ovf                                                    ; b14f: 85 3c       .<    
    tya                                                               ; b151: 98          .     
    sbc #0                                                            ; b152: e9 00       ..    
    sta zp_fwb_exp                                                    ; b154: 85 3d       .=    
    ldy #0                                                            ; b156: a0 00       ..    
; &b158 referenced 1 time by &b162
.loop_cb158
    iny                                                               ; b158: c8          .     
    inx                                                               ; b159: e8          .     
    lda (zp_fwb_ovf),y                                                ; b15a: b1 3c       .<    
    cmp (zp_general),y                                                ; b15c: d1 37       .7    
    bne cb12d                                                         ; b15e: d0 cd       ..    
    cpy zp_fileblk                                                    ; b160: c4 39       .9    
    bne loop_cb158                                                    ; b162: d0 f4       ..    
    iny                                                               ; b164: c8          .     
    lda (zp_fwb_ovf),y                                                ; b165: b1 3c       .<    
    jsr sub_c8926                                                     ; b167: 20 26 89     &.   
    bcs cb12d                                                         ; b16a: b0 c1       ..    
    txa                                                               ; b16c: 8a          .     
    tay                                                               ; b16d: a8          .     
    jsr c986d                                                         ; b16e: 20 6d 98     m.   
    jsr sub_c94ed                                                     ; b171: 20 ed 94     ..   
    ldx #1                                                            ; b174: a2 01       ..    
    jsr sub_c9531                                                     ; b176: 20 31 95     1.   
    ldy #0                                                            ; b179: a0 00       ..    
    lda zp_text_ptr                                                   ; b17b: a5 0b       ..    
    sta (zp_vartop),y                                                 ; b17d: 91 02       ..    
    iny                                                               ; b17f: c8          .     
    lda l000c                                                         ; b180: a5 0c       ..    
    sta (zp_vartop),y                                                 ; b182: 91 02       ..    
    jsr sub_c9539                                                     ; b184: 20 39 95     9.   
    jmp cb1f4                                                         ; b187: 4c f4 b1    L..   
; &b18a referenced 1 time by &b1da
.loop_cb18a
    brk                                                               ; b18a: 00          .     
    equb &1e                                                          ; b18b: 1e          .     
    equs "Bad call"                                                   ; b18c: 42 61 64... Bad...
    equb &00                                                          ; b194: 00          .     
; ***************************************************************************************
; FN
;
; Call a user-defined function and return its value. FNname[(params)].
.fn_fn
    lda #&a4                                                          ; b195: a9 a4       ..    
; &b197 referenced 1 time by &9312
.sub_cb197
    sta zp_var_type                                                   ; b197: 85 27       .'    
    tsx                                                               ; b199: ba          .     
    txa                                                               ; b19a: 8a          .     
    clc                                                               ; b19b: 18          .     
    adc zp_stack_ptr                                                  ; b19c: 65 04       e.    
    jsr reserve_stack                                                 ; b19e: 20 2e be     ..   
    ldy #0                                                            ; b1a1: a0 00       ..    
    txa                                                               ; b1a3: 8a          .     
    sta (zp_stack_ptr),y                                              ; b1a4: 91 04       ..    
; &b1a6 referenced 1 time by &b1af
.loop_cb1a6
    inx                                                               ; b1a6: e8          .     
    iny                                                               ; b1a7: c8          .     
    lda l0100,x                                                       ; b1a8: bd 00 01    ...   
    sta (zp_stack_ptr),y                                              ; b1ab: 91 04       ..    
    cpx #&ff                                                          ; b1ad: e0 ff       ..    
    bne loop_cb1a6                                                    ; b1af: d0 f5       ..    
    txs                                                               ; b1b1: 9a          .     
    lda zp_var_type                                                   ; b1b2: a5 27       .'    
    pha                                                               ; b1b4: 48          H     
    lda zp_text_ptr_off                                               ; b1b5: a5 0a       ..    
    pha                                                               ; b1b7: 48          H     
    lda zp_text_ptr                                                   ; b1b8: a5 0b       ..    
    pha                                                               ; b1ba: 48          H     
    lda l000c                                                         ; b1bb: a5 0c       ..    
    pha                                                               ; b1bd: 48          H     
    lda zp_text_ptr2_off                                              ; b1be: a5 1b       ..    
    tax                                                               ; b1c0: aa          .     
    clc                                                               ; b1c1: 18          .     
    adc zp_text_ptr2                                                  ; b1c2: 65 19       e.    
    ldy l001a                                                         ; b1c4: a4 1a       ..    
    bcc cb1ca                                                         ; b1c6: 90 02       ..    
; &b1c8 referenced 1 time by &908c
.sub_cb1c8
    iny                                                               ; b1c8: c8          .     
    clc                                                               ; b1c9: 18          .     
; &b1ca referenced 1 time by &b1c6
.cb1ca
    sbc #1                                                            ; b1ca: e9 01       ..    
    sta zp_general                                                    ; b1cc: 85 37       .7    
    tya                                                               ; b1ce: 98          .     
    sbc #0                                                            ; b1cf: e9 00       ..    
    sta l0038                                                         ; b1d1: 85 38       .8    
    ldy #2                                                            ; b1d3: a0 02       ..    
    jsr c955b                                                         ; b1d5: 20 5b 95     [.   
    cpy #2                                                            ; b1d8: c0 02       ..    
    beq loop_cb18a                                                    ; b1da: f0 ae       ..    
    stx zp_text_ptr2_off                                              ; b1dc: 86 1b       ..    
    dey                                                               ; b1de: 88          .     
    sty zp_fileblk                                                    ; b1df: 84 39       .9    
    jsr find_proc_fn                                                  ; b1e1: 20 5b 94     [.   
    bne cb1e9                                                         ; b1e4: d0 03       ..    
    jmp cb112                                                         ; b1e6: 4c 12 b1    L..   
; &b1e9 referenced 1 time by &b1e4
.cb1e9
    ldy #0                                                            ; b1e9: a0 00       ..    
    lda (zp_iwa),y                                                    ; b1eb: b1 2a       .*    
    sta zp_text_ptr                                                   ; b1ed: 85 0b       ..    
    iny                                                               ; b1ef: c8          .     
    lda (zp_iwa),y                                                    ; b1f0: b1 2a       .*    
    sta l000c                                                         ; b1f2: 85 0c       ..    
; &b1f4 referenced 1 time by &b187
.cb1f4
    lda #0                                                            ; b1f4: a9 00       ..    
    pha                                                               ; b1f6: 48          H     
    sta zp_text_ptr_off                                               ; b1f7: 85 0a       ..    
    jsr skip_spaces                                                   ; b1f9: 20 97 8a     ..   
    cmp #&28 ; '('                                                    ; b1fc: c9 28       .(    
    beq cb24d                                                         ; b1fe: f0 4d       .M    
    dec zp_text_ptr_off                                               ; b200: c6 0a       ..    
; &b202 referenced 1 time by &b30a
.cb202
    lda zp_text_ptr2_off                                              ; b202: a5 1b       ..    
    pha                                                               ; b204: 48          H     
    lda zp_text_ptr2                                                  ; b205: a5 19       ..    
    pha                                                               ; b207: 48          H     
    lda l001a                                                         ; b208: a5 1a       ..    
    pha                                                               ; b20a: 48          H     
    jsr c8ba3                                                         ; b20b: 20 a3 8b     ..   
    pla                                                               ; b20e: 68          h     
    sta l001a                                                         ; b20f: 85 1a       ..    
    pla                                                               ; b211: 68          h     
    sta zp_text_ptr2                                                  ; b212: 85 19       ..    
    pla                                                               ; b214: 68          h     
    sta zp_text_ptr2_off                                              ; b215: 85 1b       ..    
    pla                                                               ; b217: 68          h     
    beq cb226                                                         ; b218: f0 0c       ..    
    sta zp_fwb_m2                                                     ; b21a: 85 3f       .?    
; &b21c referenced 1 time by &b224
.loop_cb21c
    jsr sub_cbe0b                                                     ; b21c: 20 0b be     ..   
    jsr sub_c8cc1                                                     ; b21f: 20 c1 8c     ..   
    dec zp_fwb_m2                                                     ; b222: c6 3f       .?    
    bne loop_cb21c                                                    ; b224: d0 f6       ..    
; &b226 referenced 1 time by &b218
.cb226
    pla                                                               ; b226: 68          h     
    sta l000c                                                         ; b227: 85 0c       ..    
    pla                                                               ; b229: 68          h     
    sta zp_text_ptr                                                   ; b22a: 85 0b       ..    
    pla                                                               ; b22c: 68          h     
    sta zp_text_ptr_off                                               ; b22d: 85 0a       ..    
    pla                                                               ; b22f: 68          h     
    ldy #0                                                            ; b230: a0 00       ..    
    lda (zp_stack_ptr),y                                              ; b232: b1 04       ..    
    tax                                                               ; b234: aa          .     
    txs                                                               ; b235: 9a          .     
; &b236 referenced 1 time by &b23f
.loop_cb236
    iny                                                               ; b236: c8          .     
    inx                                                               ; b237: e8          .     
    lda (zp_stack_ptr),y                                              ; b238: b1 04       ..    
    sta l0100,x                                                       ; b23a: 9d 00 01    ...   
    cpx #&ff                                                          ; b23d: e0 ff       ..    
    bne loop_cb236                                                    ; b23f: d0 f5       ..    
    tya                                                               ; b241: 98          .     
    adc zp_stack_ptr                                                  ; b242: 65 04       e.    
    sta zp_stack_ptr                                                  ; b244: 85 04       ..    
    bcc cb24a                                                         ; b246: 90 02       ..    
    inc zp_stack_ptr_1                                                ; b248: e6 05       ..    
; &b24a referenced 1 time by &b246
.cb24a
    lda zp_var_type                                                   ; b24a: a5 27       .'    
    rts                                                               ; b24c: 60          `     
; &b24d referenced 2 times by &b1fe, &b27e
.cb24d
    lda zp_text_ptr2_off                                              ; b24d: a5 1b       ..    
    pha                                                               ; b24f: 48          H     
    lda zp_text_ptr2                                                  ; b250: a5 19       ..    
    pha                                                               ; b252: 48          H     
    lda l001a                                                         ; b253: a5 1a       ..    
    pha                                                               ; b255: 48          H     
    jsr sub_c9582                                                     ; b256: 20 82 95     ..   
    beq cb2b5                                                         ; b259: f0 5a       .Z    
    lda zp_text_ptr2_off                                              ; b25b: a5 1b       ..    
    sta zp_text_ptr_off                                               ; b25d: 85 0a       ..    
    pla                                                               ; b25f: 68          h     
    sta l001a                                                         ; b260: 85 1a       ..    
    pla                                                               ; b262: 68          h     
    sta zp_text_ptr2                                                  ; b263: 85 19       ..    
    pla                                                               ; b265: 68          h     
    sta zp_text_ptr2_off                                              ; b266: 85 1b       ..    
    pla                                                               ; b268: 68          h     
    tax                                                               ; b269: aa          .     
    lda zp_iwa_2                                                      ; b26a: a5 2c       .,    
    pha                                                               ; b26c: 48          H     
    lda zp_iwa_1                                                      ; b26d: a5 2b       .+    
    pha                                                               ; b26f: 48          H     
    lda zp_iwa                                                        ; b270: a5 2a       .*    
    pha                                                               ; b272: 48          H     
    inx                                                               ; b273: e8          .     
    txa                                                               ; b274: 8a          .     
    pha                                                               ; b275: 48          H     
    jsr sub_cb30d                                                     ; b276: 20 0d b3     ..   
    jsr skip_spaces                                                   ; b279: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; b27c: c9 2c       .,    
    beq cb24d                                                         ; b27e: f0 cd       ..    
    cmp #&29 ; ')'                                                    ; b280: c9 29       .)    
    bne cb2b5                                                         ; b282: d0 31       .1    
    lda #0                                                            ; b284: a9 00       ..    
    pha                                                               ; b286: 48          H     
    jsr skip_spaces_ptr2                                              ; b287: 20 8c 8a     ..   
    cmp #&28 ; '('                                                    ; b28a: c9 28       .(    
    bne cb2b5                                                         ; b28c: d0 27       .'    
; &b28e referenced 1 time by &b2a5
.loop_cb28e
    jsr sub_c9b29                                                     ; b28e: 20 29 9b     ).   
    jsr sub_cbd90                                                     ; b291: 20 90 bd     ..   
    lda zp_var_type                                                   ; b294: a5 27       .'    
    sta zp_iwa_3                                                      ; b296: 85 2d       .-    
    jsr stack_integer                                                 ; b298: 20 94 bd     ..   
    pla                                                               ; b29b: 68          h     
    tax                                                               ; b29c: aa          .     
    inx                                                               ; b29d: e8          .     
    txa                                                               ; b29e: 8a          .     
    pha                                                               ; b29f: 48          H     
    jsr skip_spaces_ptr2                                              ; b2a0: 20 8c 8a     ..   
    cmp #&2c ; ','                                                    ; b2a3: c9 2c       .,    
    beq loop_cb28e                                                    ; b2a5: f0 e7       ..    
    cmp #&29 ; ')'                                                    ; b2a7: c9 29       .)    
    bne cb2b5                                                         ; b2a9: d0 0a       ..    
    pla                                                               ; b2ab: 68          h     
    pla                                                               ; b2ac: 68          h     
    sta l004d                                                         ; b2ad: 85 4d       .M    
    sta l004e                                                         ; b2af: 85 4e       .N    
    cpx l004d                                                         ; b2b1: e4 4d       .M    
    beq cb2ca                                                         ; b2b3: f0 15       ..    
; &b2b5 referenced 6 times by &b259, &b282, &b28c, &b2a9, &b2da, &b2fb
.cb2b5
    ldx #&fb                                                          ; b2b5: a2 fb       ..    
    txs                                                               ; b2b7: 9a          .     
    pla                                                               ; b2b8: 68          h     
    sta l000c                                                         ; b2b9: 85 0c       ..    
    pla                                                               ; b2bb: 68          h     
    sta zp_text_ptr                                                   ; b2bc: 85 0b       ..    
    brk                                                               ; b2be: 00          .     
    equb &1f                                                          ; b2bf: 1f          .     
    equs "Arguments"                                                  ; b2c0: 41 72 67... Arg...
    equb &00                                                          ; b2c9: 00          .     
; &b2ca referenced 2 times by &b2b3, &b305
.cb2ca
    jsr unstack_integer                                               ; b2ca: 20 ea bd     ..   
    pla                                                               ; b2cd: 68          h     
    sta zp_iwa                                                        ; b2ce: 85 2a       .*    
    pla                                                               ; b2d0: 68          h     
    sta zp_iwa_1                                                      ; b2d1: 85 2b       .+    
    pla                                                               ; b2d3: 68          h     
    sta zp_iwa_2                                                      ; b2d4: 85 2c       .,    
    bmi cb2f9                                                         ; b2d6: 30 21       0!    
    lda zp_iwa_3                                                      ; b2d8: a5 2d       .-    
    beq cb2b5                                                         ; b2da: f0 d9       ..    
    sta zp_var_type                                                   ; b2dc: 85 27       .'    
    ldx #&37 ; '7'                                                    ; b2de: a2 37       .7    
    jsr iwa_store_zp                                                  ; b2e0: 20 44 be     D.   
    lda zp_var_type                                                   ; b2e3: a5 27       .'    
    bpl cb2f0                                                         ; b2e5: 10 09       ..    
    jsr sub_cbd7e                                                     ; b2e7: 20 7e bd     ~.   
    jsr fwa_unpack_var                                                ; b2ea: 20 b5 a3     ..   
    jmp cb2f3                                                         ; b2ed: 4c f3 b2    L..   
; &b2f0 referenced 1 time by &b2e5
.cb2f0
    jsr unstack_integer                                               ; b2f0: 20 ea bd     ..   
; &b2f3 referenced 1 time by &b2ed
.cb2f3
    jsr sub_cb4b7                                                     ; b2f3: 20 b7 b4     ..   
    jmp cb303                                                         ; b2f6: 4c 03 b3    L..   
; &b2f9 referenced 1 time by &b2d6
.cb2f9
    lda zp_iwa_3                                                      ; b2f9: a5 2d       .-    
    bne cb2b5                                                         ; b2fb: d0 b8       ..    
    jsr sub_cbdcb                                                     ; b2fd: 20 cb bd     ..   
    jsr sub_c8c21                                                     ; b300: 20 21 8c     !.   
; &b303 referenced 1 time by &b2f6
.cb303
    dec l004d                                                         ; b303: c6 4d       .M    
    bne cb2ca                                                         ; b305: d0 c3       ..    
    lda l004e                                                         ; b307: a5 4e       .N    
    pha                                                               ; b309: 48          H     
    jmp cb202                                                         ; b30a: 4c 02 b2    L..   
; &b30d referenced 2 times by &932d, &b276
.sub_cb30d
    ldy zp_iwa_2                                                      ; b30d: a4 2c       .,    
    cpy #4                                                            ; b30f: c0 04       ..    
    bne cb318                                                         ; b311: d0 05       ..    
    ldx #&37 ; '7'                                                    ; b313: a2 37       .7    
    jsr iwa_store_zp                                                  ; b315: 20 44 be     D.   
; &b318 referenced 1 time by &b311
.cb318
    jsr cb32c                                                         ; b318: 20 2c b3     ,.   
    php                                                               ; b31b: 08          .     
    jsr sub_cbd90                                                     ; b31c: 20 90 bd     ..   
    plp                                                               ; b31f: 28          (     
    beq cb329                                                         ; b320: f0 07       ..    
    bmi cb329                                                         ; b322: 30 05       0.    
    ldx #&37 ; '7'                                                    ; b324: a2 37       .7    
    jsr iwa_load_zp                                                   ; b326: 20 56 af     V.   
; &b329 referenced 2 times by &b320, &b322
.cb329
    jmp stack_integer                                                 ; b329: 4c 94 bd    L..   
; &b32c referenced 3 times by &9685, &ae27, &b318
.cb32c
    ldy zp_iwa_2                                                      ; b32c: a4 2c       .,    
    bmi cb384                                                         ; b32e: 30 54       0T    
    beq cb34f                                                         ; b330: f0 1d       ..    
    cpy #5                                                            ; b332: c0 05       ..    
    beq cb354                                                         ; b334: f0 1e       ..    
; ***************************************************************************************
; Load an integer variable into the accumulator
;
; Copy the 4-byte integer addressed by zp_iwa into IWA.
;
; On Entry:
;     ZP_IWA (&2A/&2B): a pointer to the 4-byte integer variable
;
; On Exit:
;     ZP_IWA: the loaded integer
;     X: preserved
.iwa_load_var
    ldy #3                                                            ; b336: a0 03       ..    
    lda (zp_iwa),y                                                    ; b338: b1 2a       .*    
    sta zp_iwa_3                                                      ; b33a: 85 2d       .-    
    dey                                                               ; b33c: 88          .     
    lda (zp_iwa),y                                                    ; b33d: b1 2a       .*    
    sta zp_iwa_2                                                      ; b33f: 85 2c       .,    
    dey                                                               ; b341: 88          .     
    lda (zp_iwa),y                                                    ; b342: b1 2a       .*    
    tax                                                               ; b344: aa          .     
    dey                                                               ; b345: 88          .     
    lda (zp_iwa),y                                                    ; b346: b1 2a       .*    
    sta zp_iwa                                                        ; b348: 85 2a       .*    
    stx zp_iwa_1                                                      ; b34a: 86 2b       .+    
    lda #&40 ; '@'                                                    ; b34c: a9 40       .@    
    rts                                                               ; b34e: 60          `     
; &b34f referenced 1 time by &b330
.cb34f
    lda (zp_iwa),y                                                    ; b34f: b1 2a       .*    
    jmp iwa_from_ya                                                   ; b351: 4c ea ae    L..   
; &b354 referenced 2 times by &b334, &b766
.cb354
    dey                                                               ; b354: 88          .     
    lda (zp_iwa),y                                                    ; b355: b1 2a       .*    
    sta zp_fwa_m4                                                     ; b357: 85 34       .4    
    dey                                                               ; b359: 88          .     
    lda (zp_iwa),y                                                    ; b35a: b1 2a       .*    
    sta zp_fwa_m3                                                     ; b35c: 85 33       .3    
    dey                                                               ; b35e: 88          .     
    lda (zp_iwa),y                                                    ; b35f: b1 2a       .*    
    sta zp_fwa_m2                                                     ; b361: 85 32       .2    
    dey                                                               ; b363: 88          .     
    lda (zp_iwa),y                                                    ; b364: b1 2a       .*    
    sta zp_fwa_sign                                                   ; b366: 85 2e       ..    
    dey                                                               ; b368: 88          .     
    lda (zp_iwa),y                                                    ; b369: b1 2a       .*    
    sta zp_fwa_exp                                                    ; b36b: 85 30       .0    
    sty zp_fwa_rnd                                                    ; b36d: 84 35       .5    
    sty zp_fwa_ovf                                                    ; b36f: 84 2f       ./    
    ora zp_fwa_sign                                                   ; b371: 05 2e       ..    
    ora zp_fwa_m2                                                     ; b373: 05 32       .2    
    ora zp_fwa_m3                                                     ; b375: 05 33       .3    
    ora zp_fwa_m4                                                     ; b377: 05 34       .4    
    beq cb37f                                                         ; b379: f0 04       ..    
    lda zp_fwa_sign                                                   ; b37b: a5 2e       ..    
    ora #&80                                                          ; b37d: 09 80       ..    
; &b37f referenced 1 time by &b379
.cb37f
    sta zp_fwa_m1                                                     ; b37f: 85 31       .1    
    lda #&ff                                                          ; b381: a9 ff       ..    
    rts                                                               ; b383: 60          `     
; &b384 referenced 1 time by &b32e
.cb384
    cpy #&80                                                          ; b384: c0 80       ..    
    beq cb3a7                                                         ; b386: f0 1f       ..    
    ldy #3                                                            ; b388: a0 03       ..    
    lda (zp_iwa),y                                                    ; b38a: b1 2a       .*    
    sta zp_strbuf_len                                                 ; b38c: 85 36       .6    
    beq return_32                                                     ; b38e: f0 16       ..    
    ldy #1                                                            ; b390: a0 01       ..    
    lda (zp_iwa),y                                                    ; b392: b1 2a       .*    
    sta l0038                                                         ; b394: 85 38       .8    
    dey                                                               ; b396: 88          .     
    lda (zp_iwa),y                                                    ; b397: b1 2a       .*    
    sta zp_general                                                    ; b399: 85 37       .7    
    ldy zp_strbuf_len                                                 ; b39b: a4 36       .6    
; &b39d referenced 1 time by &b3a4
.loop_cb39d
    dey                                                               ; b39d: 88          .     
    lda (zp_general),y                                                ; b39e: b1 37       .7    
    sta string_work,y                                                 ; b3a0: 99 00 06    ...   
    tya                                                               ; b3a3: 98          .     
    bne loop_cb39d                                                    ; b3a4: d0 f7       ..    
; &b3a6 referenced 1 time by &b38e
.return_32
    rts                                                               ; b3a6: 60          `     
; &b3a7 referenced 1 time by &b386
.cb3a7
    lda zp_iwa_1                                                      ; b3a7: a5 2b       .+    
    beq cb3c0                                                         ; b3a9: f0 15       ..    
    ldy #0                                                            ; b3ab: a0 00       ..    
; &b3ad referenced 1 time by &b3b7
.loop_cb3ad
    lda (zp_iwa),y                                                    ; b3ad: b1 2a       .*    
    sta string_work,y                                                 ; b3af: 99 00 06    ...   
    eor #&0d                                                          ; b3b2: 49 0d       I.    
    beq cb3ba                                                         ; b3b4: f0 04       ..    
    iny                                                               ; b3b6: c8          .     
    bne loop_cb3ad                                                    ; b3b7: d0 f4       ..    
    tya                                                               ; b3b9: 98          .     
; &b3ba referenced 1 time by &b3b4
.cb3ba
    sty zp_strbuf_len                                                 ; b3ba: 84 36       .6    
    rts                                                               ; b3bc: 60          `     
; ***************************************************************************************
; CHR$
;
; One-character string for an ASCII code. CHR$ numeric.
.fn_chrs
    jsr sub_c92e3                                                     ; b3bd: 20 e3 92     ..   
; &b3c0 referenced 1 time by &b3a9
.cb3c0
    lda zp_iwa                                                        ; b3c0: a5 2a       .*    
    jmp cafc2                                                         ; b3c2: 4c c2 af    L..   
; &b3c5 referenced 1 time by &b402
.sub_cb3c5
    ldy #0                                                            ; b3c5: a0 00       ..    
    sty zp_erl                                                        ; b3c7: 84 08       ..    
    sty l0009                                                         ; b3c9: 84 09       ..    
    ldx zp_page                                                       ; b3cb: a6 18       ..    
    stx l0038                                                         ; b3cd: 86 38       .8    
    sty zp_general                                                    ; b3cf: 84 37       .7    
    ldx l000c                                                         ; b3d1: a6 0c       ..    
    cpx #7                                                            ; b3d3: e0 07       ..    
    beq return_33                                                     ; b3d5: f0 2a       .*    
    ldx zp_text_ptr                                                   ; b3d7: a6 0b       ..    
; &b3d9 referenced 1 time by &b3ff
.loop_cb3d9
    jsr read_via_ptr_general                                          ; b3d9: 20 42 89     B.   
    cmp #&0d                                                          ; b3dc: c9 0d       ..    
    bne cb3f9                                                         ; b3de: d0 19       ..    
    cpx zp_general                                                    ; b3e0: e4 37       .7    
    lda l000c                                                         ; b3e2: a5 0c       ..    
    sbc l0038                                                         ; b3e4: e5 38       .8    
    bcc return_33                                                     ; b3e6: 90 19       ..    
    jsr read_via_ptr_general                                          ; b3e8: 20 42 89     B.   
    ora #0                                                            ; b3eb: 09 00       ..    
    bmi return_33                                                     ; b3ed: 30 12       0.    
    sta l0009                                                         ; b3ef: 85 09       ..    
    jsr read_via_ptr_general                                          ; b3f1: 20 42 89     B.   
    sta zp_erl                                                        ; b3f4: 85 08       ..    
    jsr read_via_ptr_general                                          ; b3f6: 20 42 89     B.   
; &b3f9 referenced 1 time by &b3de
.cb3f9
    cpx zp_general                                                    ; b3f9: e4 37       .7    
    lda l000c                                                         ; b3fb: a5 0c       ..    
    sbc l0038                                                         ; b3fd: e5 38       .8    
    bcs loop_cb3d9                                                    ; b3ff: b0 d8       ..    
; &b401 referenced 3 times by &b3d5, &b3e6, &b3ed
.return_33
    rts                                                               ; b401: 60          `     
.brk_handler
    jsr sub_cb3c5                                                     ; b402: 20 c5 b3     ..   
    sty zp_trace_flag                                                 ; b405: 84 20       .     
    lda (l00fd),y                                                     ; b407: b1 fd       ..    
    bne cb413                                                         ; b409: d0 08       ..    
    lda #&33 ; '3'                                                    ; b40b: a9 33       .3    
    sta zp_error_vec                                                  ; b40d: 85 16       ..    
    lda #&b4                                                          ; b40f: a9 b4       ..    
    sta l0017                                                         ; b411: 85 17       ..    
; &b413 referenced 1 time by &b409
.cb413
    lda zp_error_vec                                                  ; b413: a5 16       ..    
    sta zp_text_ptr                                                   ; b415: 85 0b       ..    
    lda l0017                                                         ; b417: a5 17       ..    
    sta l000c                                                         ; b419: 85 0c       ..    
    jsr sub_cbd3a                                                     ; b41b: 20 3a bd     :.   
    tax                                                               ; b41e: aa          .     
    stx zp_text_ptr_off                                               ; b41f: 86 0a       ..    
    lda #osbyte_vdu_queue_size                                        ; b421: a9 da       ..    
    jsr osbyte                                                        ; b423: 20 f4 ff     ..      ; osbyte: vdu queue size
    lda #osbyte_acknowledge_escape                                    ; b426: a9 7e       .~    
    jsr osbyte                                                        ; b428: 20 f4 ff     ..      ; Clear escape condition and perform escape effects
    ldx #&ff                                                          ; b42b: a2 ff       ..    
    stx zp_opt_flag                                                   ; b42d: 86 28       .(    
    txs                                                               ; b42f: 9a          .     
    jmp c8ba3                                                         ; b430: 4c a3 8b    L..   
    equb &f6, &3a, &e7, &9e, &f1                                      ; b433: f6 3a e7... .:....
    equb &22, " at line ", &22, ";"                                   ; b438: 22 20 61... " a...
    equb &9e, &3a, &e0, &8b, &f1, &3a, &e0, &0d                       ; b444: 9e 3a e0... .:....
; ***************************************************************************************
; SOUND
;
; Make a sound on a channel. SOUND channel, amplitude, pitch, duration.
.stmt_sound
    jsr eval_expr_to_integer                                          ; b44c: 20 21 88     !.   
    ldx #3                                                            ; b44f: a2 03       ..    
; &b451 referenced 1 time by &b45f
.loop_cb451
    lda zp_iwa                                                        ; b451: a5 2a       .*    
    pha                                                               ; b453: 48          H     
    lda zp_iwa_1                                                      ; b454: a5 2b       .+    
    pha                                                               ; b456: 48          H     
    txa                                                               ; b457: 8a          .     
    pha                                                               ; b458: 48          H     
    jsr sub_c92da                                                     ; b459: 20 da 92     ..   
    pla                                                               ; b45c: 68          h     
    tax                                                               ; b45d: aa          .     
    dex                                                               ; b45e: ca          .     
    bne loop_cb451                                                    ; b45f: d0 f0       ..    
    jsr sub_c9852                                                     ; b461: 20 52 98     R.   
    lda zp_iwa                                                        ; b464: a5 2a       .*    
    sta zp_fwb_exp                                                    ; b466: 85 3d       .=    
    lda zp_iwa_1                                                      ; b468: a5 2b       .+    
    sta zp_fwb_m1                                                     ; b46a: 85 3e       .>    
    ldy #7                                                            ; b46c: a0 07       ..    
    ldx #5                                                            ; b46e: a2 05       ..    
    bne cb48f                                                         ; b470: d0 1d       ..    
; ***************************************************************************************
; ENVELOPE
;
; Define a pitch/amplitude envelope for SOUND. ENVELOPE n,t,... (14 parameters).
.stmt_envelope
    jsr eval_expr_to_integer                                          ; b472: 20 21 88     !.   
    ldx #&0d                                                          ; b475: a2 0d       ..    
; &b477 referenced 1 time by &b482
.loop_cb477
    lda zp_iwa                                                        ; b477: a5 2a       .*    
    pha                                                               ; b479: 48          H     
    txa                                                               ; b47a: 8a          .     
    pha                                                               ; b47b: 48          H     
    jsr sub_c92da                                                     ; b47c: 20 da 92     ..   
    pla                                                               ; b47f: 68          h     
    tax                                                               ; b480: aa          .     
    dex                                                               ; b481: ca          .     
    bne loop_cb477                                                    ; b482: d0 f3       ..    
    jsr sub_c9852                                                     ; b484: 20 52 98     R.   
    lda zp_iwa                                                        ; b487: a5 2a       .*    
    sta l0044                                                         ; b489: 85 44       .D    
    ldx #&0c                                                          ; b48b: a2 0c       ..    
    ldy #osword_envelope                                              ; b48d: a0 08       ..    
; &b48f referenced 2 times by &b470, &b493
.cb48f
    pla                                                               ; b48f: 68          h     
    sta zp_general,x                                                  ; b490: 95 37       .7    
    dex                                                               ; b492: ca          .     
    bpl cb48f                                                         ; b493: 10 fa       ..    
    tya                                                               ; b495: 98          .     
    ldx #<(zp_general)                                                ; b496: a2 37       .7    
    ldy #>(zp_general)                                                ; b498: a0 00       ..    
    jsr osword                                                        ; b49a: 20 f1 ff     ..      ; ENVELOPE command
    jmp statement_loop                                                ; b49d: 4c 9b 8b    L..   
; ***************************************************************************************
; WIDTH
;
; Set the output line width for PRINT. WIDTH n.
.stmt_width
    jsr eval_expr_to_integer                                          ; b4a0: 20 21 88     !.   
    jsr sub_c9852                                                     ; b4a3: 20 52 98     R.   
    ldy zp_iwa                                                        ; b4a6: a4 2a       .*    
    dey                                                               ; b4a8: 88          .     
    sty zp_width                                                      ; b4a9: 84 23       .#    
    jmp statement_loop                                                ; b4ab: 4c 9b 8b    L..   
; &b4ae referenced 2 times by &b4bf, &b4e2
.cb4ae
    jmp c8c0e                                                         ; b4ae: 4c 0e 8c    L..   
; &b4b1 referenced 2 times by &b7d1, &bb2c
.sub_cb4b1
    jsr sub_c9b29                                                     ; b4b1: 20 29 9b     ).   
; &b4b4 referenced 6 times by &85b4, &8c05, &911e, &933e, &ba39, &bad6
.sub_cb4b4
    jsr sub_cbe0b                                                     ; b4b4: 20 0b be     ..   
; &b4b7 referenced 1 time by &b2f3
.sub_cb4b7
    lda zp_fileblk                                                    ; b4b7: a5 39       .9    
    cmp #5                                                            ; b4b9: c9 05       ..    
    beq cb4e0                                                         ; b4bb: f0 23       .#    
    lda zp_var_type                                                   ; b4bd: a5 27       .'    
    beq cb4ae                                                         ; b4bf: f0 ed       ..    
    bpl iwa_store_var                                                 ; b4c1: 10 03       ..    
    jsr fwa_to_int                                                    ; b4c3: 20 e4 a3     ..   
; ***************************************************************************************
; Store the accumulator into an integer variable
;
; Copy IWA into the 4-byte integer variable addressed by &37.
;
; On Entry:
;     (ZP_GENERAL) (&37/&38): a pointer to the integer variable
;     &39: non-zero
;
; On Exit:
;     X: preserved
; &b4c6 referenced 1 time by &b4c1
.iwa_store_var
    ldy #0                                                            ; b4c6: a0 00       ..    
    lda zp_iwa                                                        ; b4c8: a5 2a       .*    
    sta (zp_general),y                                                ; b4ca: 91 37       .7    
    lda zp_fileblk                                                    ; b4cc: a5 39       .9    
    beq return_34                                                     ; b4ce: f0 0f       ..    
    lda zp_iwa_1                                                      ; b4d0: a5 2b       .+    
    iny                                                               ; b4d2: c8          .     
    sta (zp_general),y                                                ; b4d3: 91 37       .7    
    lda zp_iwa_2                                                      ; b4d5: a5 2c       .,    
    iny                                                               ; b4d7: c8          .     
    sta (zp_general),y                                                ; b4d8: 91 37       .7    
    lda zp_iwa_3                                                      ; b4da: a5 2d       .-    
    iny                                                               ; b4dc: c8          .     
    sta (zp_general),y                                                ; b4dd: 91 37       .7    
; &b4df referenced 1 time by &b4ce
.return_34
    rts                                                               ; b4df: 60          `     
; &b4e0 referenced 1 time by &b4bb
.cb4e0
    lda zp_var_type                                                   ; b4e0: a5 27       .'    
    beq cb4ae                                                         ; b4e2: f0 ca       ..    
    bmi cb4e9                                                         ; b4e4: 30 03       0.    
    jsr int_to_fwa                                                    ; b4e6: 20 be a2     ..   
; &b4e9 referenced 2 times by &b4e4, &b77f
.cb4e9
    ldy #0                                                            ; b4e9: a0 00       ..    
    lda zp_fwa_exp                                                    ; b4eb: a5 30       .0    
    sta (zp_general),y                                                ; b4ed: 91 37       .7    
    iny                                                               ; b4ef: c8          .     
    lda zp_fwa_sign                                                   ; b4f0: a5 2e       ..    
    and #&80                                                          ; b4f2: 29 80       ).    
    sta zp_fwa_sign                                                   ; b4f4: 85 2e       ..    
    lda zp_fwa_m1                                                     ; b4f6: a5 31       .1    
    and #&7f                                                          ; b4f8: 29 7f       ).    
    ora zp_fwa_sign                                                   ; b4fa: 05 2e       ..    
    sta (zp_general),y                                                ; b4fc: 91 37       .7    
    iny                                                               ; b4fe: c8          .     
    lda zp_fwa_m2                                                     ; b4ff: a5 32       .2    
    sta (zp_general),y                                                ; b501: 91 37       .7    
    iny                                                               ; b503: c8          .     
    lda zp_fwa_m3                                                     ; b504: a5 33       .3    
    sta (zp_general),y                                                ; b506: 91 37       .7    
    iny                                                               ; b508: c8          .     
    lda zp_fwa_m4                                                     ; b509: a5 34       .4    
    sta (zp_general),y                                                ; b50b: 91 37       .7    
    rts                                                               ; b50d: 60          `     
; &b50e referenced 3 times by &8571, &b688, &bff0
.sub_cb50e
    sta zp_general                                                    ; b50e: 85 37       .7    
    cmp #&80                                                          ; b510: c9 80       ..    
    bcc cb558                                                         ; b512: 90 44       .D    
    lda #&71 ; 'q'                                                    ; b514: a9 71       .q    
    sta l0038                                                         ; b516: 85 38       .8    
    lda #&80                                                          ; b518: a9 80       ..    
    sta zp_fileblk                                                    ; b51a: 85 39       .9    
    sty l003a                                                         ; b51c: 84 3a       .:    
; &b51e referenced 2 times by &b530, &b534
.cb51e
    ldy #0                                                            ; b51e: a0 00       ..    
; &b520 referenced 1 time by &b523
.loop_cb520
    iny                                                               ; b520: c8          .     
    lda (l0038),y                                                     ; b521: b1 38       .8    
    bpl loop_cb520                                                    ; b523: 10 fb       ..    
    cmp zp_general                                                    ; b525: c5 37       .7    
    beq cb536                                                         ; b527: f0 0d       ..    
    iny                                                               ; b529: c8          .     
    tya                                                               ; b52a: 98          .     
    sec                                                               ; b52b: 38          8     
    adc l0038                                                         ; b52c: 65 38       e8    
    sta l0038                                                         ; b52e: 85 38       .8    
    bcc cb51e                                                         ; b530: 90 ec       ..    
    inc zp_fileblk                                                    ; b532: e6 39       .9    
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
; &b558 referenced 13 times by &855c, &855f, &8e17, &8ea4, &9911, &9919, &9964, &b512, &b53c, &b583, &b64b, &ba9f, &bc02
.cb558
    cmp #&0d                                                          ; b558: c9 0d       ..    
    bne cb567                                                         ; b55a: d0 0b       ..    
    jsr oswrch                                                        ; b55c: 20 ee ff     ..   
    jmp cbc28                                                         ; b55f: 4c 28 bc    L(.   
; &b562 referenced 2 times by &852b, &854e
.sub_cb562
    jsr sub_cb545                                                     ; b562: 20 45 b5     E.   
; &b565 referenced 9 times by &8544, &8559, &8db5, &8e08, &8e5f, &991c, &995a, &b57e, &b580
.cb565
    lda #&20 ; ' '                                                    ; b565: a9 20       .     
; &b567 referenced 1 time by &b55a
.cb567
    pha                                                               ; b567: 48          H     
    lda zp_width                                                      ; b568: a5 23       .#    
    cmp zp_count                                                      ; b56a: c5 1e       ..    
    bcs cb571                                                         ; b56c: b0 03       ..    
    jsr sub_cbc25                                                     ; b56e: 20 25 bc     %.   
; &b571 referenced 1 time by &b56c
.cb571
    pla                                                               ; b571: 68          h     
    inc zp_count                                                      ; b572: e6 1e       ..    
    jmp (wrchv)                                                       ; b574: 6c 0e 02    l..   
; &b577 referenced 3 times by &b626, &b62d, &b634
.sub_cb577
    and zp_listo                                                      ; b577: 25 1f       %.    
    beq return_35                                                     ; b579: f0 0e       ..    
    txa                                                               ; b57b: 8a          .     
    beq return_35                                                     ; b57c: f0 0b       ..    
    bmi cb565                                                         ; b57e: 30 e5       0.    
; &b580 referenced 1 time by &b587
.loop_cb580
    jsr cb565                                                         ; b580: 20 65 b5     e.   
    jsr cb558                                                         ; b583: 20 58 b5     X.   
    dex                                                               ; b586: ca          .     
    bne loop_cb580                                                    ; b587: d0 f7       ..    
; &b589 referenced 2 times by &b579, &b57c
.return_35
    rts                                                               ; b589: 60          `     
; &b58a referenced 1 time by &b5a1
.loop_cb58a
    inc zp_text_ptr_off                                               ; b58a: e6 0a       ..    
    jsr eval_expr                                                     ; b58c: 20 1d 9b     ..   
    jsr c984c                                                         ; b58f: 20 4c 98     L.   
    jsr sub_c92ee                                                     ; b592: 20 ee 92     ..   
    lda zp_iwa                                                        ; b595: a5 2a       .*    
    sta zp_listo                                                      ; b597: 85 1f       ..    
    jmp immediate_loop                                                ; b599: 4c f6 8a    L..   
; ***************************************************************************************
; LIST
;
; List program lines, de-tokenising them. LIST [start[,end]].
.stmt_list
    iny                                                               ; b59c: c8          .     
    lda (zp_text_ptr),y                                               ; b59d: b1 0b       ..    
    cmp #&4f ; 'O'                                                    ; b59f: c9 4f       .O    
    beq loop_cb58a                                                    ; b5a1: f0 e7       ..    
    lda #0                                                            ; b5a3: a9 00       ..    
    sta zp_fwb_sign                                                   ; b5a5: 85 3b       .;    
    sta zp_fwb_ovf                                                    ; b5a7: 85 3c       .<    
    jsr caed8                                                         ; b5a9: 20 d8 ae     ..   
    jsr sub_c97df                                                     ; b5ac: 20 df 97     ..   
    php                                                               ; b5af: 08          .     
    jsr stack_integer                                                 ; b5b0: 20 94 bd     ..   
    lda #&ff                                                          ; b5b3: a9 ff       ..    
    sta zp_iwa                                                        ; b5b5: 85 2a       .*    
    lda #&7f                                                          ; b5b7: a9 7f       ..    
    sta zp_iwa_1                                                      ; b5b9: 85 2b       .+    
    plp                                                               ; b5bb: 28          (     
    bcc cb5cf                                                         ; b5bc: 90 11       ..    
    jsr skip_spaces                                                   ; b5be: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; b5c1: c9 2c       .,    
    beq cb5d8                                                         ; b5c3: f0 13       ..    
    jsr unstack_integer                                               ; b5c5: 20 ea bd     ..   
    jsr stack_integer                                                 ; b5c8: 20 94 bd     ..   
    dec zp_text_ptr_off                                               ; b5cb: c6 0a       ..    
    bpl cb5db                                                         ; b5cd: 10 0c       ..    
; &b5cf referenced 1 time by &b5bc
.cb5cf
    jsr skip_spaces                                                   ; b5cf: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; b5d2: c9 2c       .,    
    beq cb5d8                                                         ; b5d4: f0 02       ..    
    dec zp_text_ptr_off                                               ; b5d6: c6 0a       ..    
; &b5d8 referenced 2 times by &b5c3, &b5d4
.cb5d8
    jsr sub_c97df                                                     ; b5d8: 20 df 97     ..   
; &b5db referenced 1 time by &b5cd
.cb5db
    lda zp_iwa                                                        ; b5db: a5 2a       .*    
    sta zp_fwa_m1                                                     ; b5dd: 85 31       .1    
    lda zp_iwa_1                                                      ; b5df: a5 2b       .+    
    sta zp_fwa_m2                                                     ; b5e1: 85 32       .2    
    jsr check_end_of_statement                                        ; b5e3: 20 57 98     W.   
    jsr sub_cbe6f                                                     ; b5e6: 20 6f be     o.   
    jsr unstack_integer                                               ; b5e9: 20 ea bd     ..   
    jsr sub_c9970                                                     ; b5ec: 20 70 99     p.   
    lda zp_fwb_exp                                                    ; b5ef: a5 3d       .=    
    sta zp_text_ptr                                                   ; b5f1: 85 0b       ..    
    lda zp_fwb_m1                                                     ; b5f3: a5 3e       .>    
    sta l000c                                                         ; b5f5: 85 0c       ..    
    bcc cb60f                                                         ; b5f7: 90 16       ..    
    dey                                                               ; b5f9: 88          .     
    bcs cb602                                                         ; b5fa: b0 06       ..    
; &b5fc referenced 1 time by &b63d
.loop_cb5fc
    jsr sub_cbc25                                                     ; b5fc: 20 25 bc     %.   
    jsr c986d                                                         ; b5ff: 20 6d 98     m.   
; &b602 referenced 1 time by &b5fa
.cb602
    lda (zp_text_ptr),y                                               ; b602: b1 0b       ..    
    sta zp_iwa_1                                                      ; b604: 85 2b       .+    
    iny                                                               ; b606: c8          .     
    lda (zp_text_ptr),y                                               ; b607: b1 0b       ..    
    sta zp_iwa                                                        ; b609: 85 2a       .*    
    iny                                                               ; b60b: c8          .     
    iny                                                               ; b60c: c8          .     
    sty zp_text_ptr_off                                               ; b60d: 84 0a       ..    
; &b60f referenced 1 time by &b5f7
.cb60f
    lda zp_iwa                                                        ; b60f: a5 2a       .*    
    clc                                                               ; b611: 18          .     
    sbc zp_fwa_m1                                                     ; b612: e5 31       .1    
    lda zp_iwa_1                                                      ; b614: a5 2b       .+    
    sbc zp_fwa_m2                                                     ; b616: e5 32       .2    
    bcc cb61d                                                         ; b618: 90 03       ..    
    jmp immediate_loop                                                ; b61a: 4c f6 8a    L..   
; &b61d referenced 1 time by &b618
.cb61d
    jsr sub_c9923                                                     ; b61d: 20 23 99     #.   
    ldx #&ff                                                          ; b620: a2 ff       ..    
    stx l004d                                                         ; b622: 86 4d       .M    
    lda #1                                                            ; b624: a9 01       ..    
    jsr sub_cb577                                                     ; b626: 20 77 b5     w.   
    ldx zp_fwb_sign                                                   ; b629: a6 3b       .;    
    lda #2                                                            ; b62b: a9 02       ..    
    jsr sub_cb577                                                     ; b62d: 20 77 b5     w.   
    ldx zp_fwb_ovf                                                    ; b630: a6 3c       .<    
    lda #4                                                            ; b632: a9 04       ..    
    jsr sub_cb577                                                     ; b634: 20 77 b5     w.   
; &b637 referenced 1 time by &b665
.cb637
    ldy zp_text_ptr_off                                               ; b637: a4 0a       ..    
; &b639 referenced 2 times by &b64f, &b68c
.cb639
    lda (zp_text_ptr),y                                               ; b639: b1 0b       ..    
    cmp #&0d                                                          ; b63b: c9 0d       ..    
    beq loop_cb5fc                                                    ; b63d: f0 bd       ..    
    cmp #&22                                                          ; b63f: c9 22       ."    
    bne cb651                                                         ; b641: d0 0e       ..    
    lda #&ff                                                          ; b643: a9 ff       ..    
    eor l004d                                                         ; b645: 45 4d       EM    
    sta l004d                                                         ; b647: 85 4d       .M    
    lda #&22                                                          ; b649: a9 22       ."    
; &b64b referenced 1 time by &b653
.loop_cb64b
    jsr cb558                                                         ; b64b: 20 58 b5     X.   
    iny                                                               ; b64e: c8          .     
    bne cb639                                                         ; b64f: d0 e8       ..    
; &b651 referenced 1 time by &b641
.cb651
    bit l004d                                                         ; b651: 24 4d       $M    
    bpl loop_cb64b                                                    ; b653: 10 f6       ..    
    cmp #&8d                                                          ; b655: c9 8d       ..    
    bne cb668                                                         ; b657: d0 0f       ..    
    jsr sub_c97eb                                                     ; b659: 20 eb 97     ..   
    sty zp_text_ptr_off                                               ; b65c: 84 0a       ..    
    lda #0                                                            ; b65e: a9 00       ..    
    sta zp_print_bytes                                                ; b660: 85 14       ..    
    jsr sub_c991f                                                     ; b662: 20 1f 99     ..   
    jmp cb637                                                         ; b665: 4c 37 b6    L7.   
; &b668 referenced 1 time by &b657
.cb668
    cmp #&e3                                                          ; b668: c9 e3       ..    
    bne cb66e                                                         ; b66a: d0 02       ..    
    inc zp_fwb_sign                                                   ; b66c: e6 3b       .;    
; &b66e referenced 1 time by &b66a
.cb66e
    cmp #&ed                                                          ; b66e: c9 ed       ..    
    bne cb678                                                         ; b670: d0 06       ..    
    ldx zp_fwb_sign                                                   ; b672: a6 3b       .;    
    beq cb678                                                         ; b674: f0 02       ..    
    dec zp_fwb_sign                                                   ; b676: c6 3b       .;    
; &b678 referenced 2 times by &b670, &b674
.cb678
    cmp #&f5                                                          ; b678: c9 f5       ..    
    bne cb67e                                                         ; b67a: d0 02       ..    
    inc zp_fwb_ovf                                                    ; b67c: e6 3c       .<    
; &b67e referenced 1 time by &b67a
.cb67e
    cmp #&fd                                                          ; b67e: c9 fd       ..    
    bne cb688                                                         ; b680: d0 06       ..    
    ldx zp_fwb_ovf                                                    ; b682: a6 3c       .<    
    beq cb688                                                         ; b684: f0 02       ..    
    dec zp_fwb_ovf                                                    ; b686: c6 3c       .<    
; &b688 referenced 2 times by &b680, &b684
.cb688
    jsr sub_cb50e                                                     ; b688: 20 0e b5     ..   
    iny                                                               ; b68b: c8          .     
    bne cb639                                                         ; b68c: d0 ab       ..    
; &b68e referenced 2 times by &b69c, &b6a7
.cb68e
    brk                                                               ; b68e: 00          .     
    equs " No "                                                       ; b68f: 20 4e 6f...  No...
    equb &e3, &00                                                     ; b693: e3 00       ..    
; ***************************************************************************************
; NEXT
;
; End a FOR loop: update the counter and loop back unless the limit is passed. NEXT
; [var,...].
; &b695 referenced 1 time by &b763
.stmt_next
    jsr sub_c95c9                                                     ; b695: 20 c9 95     ..   
    bne cb6a3                                                         ; b698: d0 09       ..    
    ldx zp_for_level                                                  ; b69a: a6 26       .&    
    beq cb68e                                                         ; b69c: f0 f0       ..    
    bcs cb6d7                                                         ; b69e: b0 37       .7    
; &b6a0 referenced 1 time by &b6a3
.loop_cb6a0
    jmp c982a                                                         ; b6a0: 4c 2a 98    L*.   
; &b6a3 referenced 1 time by &b698
.cb6a3
    bcs loop_cb6a0                                                    ; b6a3: b0 fb       ..    
    ldx zp_for_level                                                  ; b6a5: a6 26       .&    
    beq cb68e                                                         ; b6a7: f0 e5       ..    
; &b6a9 referenced 1 time by &b6c5
.loop_cb6a9
    lda zp_iwa                                                        ; b6a9: a5 2a       .*    
    cmp l04f1,x                                                       ; b6ab: dd f1 04    ...   
    bne cb6be                                                         ; b6ae: d0 0e       ..    
    lda zp_iwa_1                                                      ; b6b0: a5 2b       .+    
    cmp l04f2,x                                                       ; b6b2: dd f2 04    ...   
    bne cb6be                                                         ; b6b5: d0 07       ..    
    lda zp_iwa_2                                                      ; b6b7: a5 2c       .,    
    cmp l04f3,x                                                       ; b6b9: dd f3 04    ...   
    beq cb6d7                                                         ; b6bc: f0 19       ..    
; &b6be referenced 2 times by &b6ae, &b6b5
.cb6be
    txa                                                               ; b6be: 8a          .     
    sec                                                               ; b6bf: 38          8     
    sbc #&0f                                                          ; b6c0: e9 0f       ..    
    tax                                                               ; b6c2: aa          .     
    stx zp_for_level                                                  ; b6c3: 86 26       .&    
    bne loop_cb6a9                                                    ; b6c5: d0 e2       ..    
    brk                                                               ; b6c7: 00          .     
    equs "!Can't Match "                                              ; b6c8: 21 43 61... !Ca...
    equb &e3, &00                                                     ; b6d5: e3 00       ..    
; &b6d7 referenced 2 times by &b69e, &b6bc
.cb6d7
    lda l04f1,x                                                       ; b6d7: bd f1 04    ...   
    sta zp_iwa                                                        ; b6da: 85 2a       .*    
    lda l04f2,x                                                       ; b6dc: bd f2 04    ...   
    sta zp_iwa_1                                                      ; b6df: 85 2b       .+    
    ldy l04f3,x                                                       ; b6e1: bc f3 04    ...   
    cpy #5                                                            ; b6e4: c0 05       ..    
    beq cb766                                                         ; b6e6: f0 7e       .~    
    ldy #0                                                            ; b6e8: a0 00       ..    
    lda (zp_iwa),y                                                    ; b6ea: b1 2a       .*    
    adc l04f4,x                                                       ; b6ec: 7d f4 04    }..   
    sta (zp_iwa),y                                                    ; b6ef: 91 2a       .*    
    sta zp_general                                                    ; b6f1: 85 37       .7    
    iny                                                               ; b6f3: c8          .     
    lda (zp_iwa),y                                                    ; b6f4: b1 2a       .*    
    adc l04f5,x                                                       ; b6f6: 7d f5 04    }..   
    sta (zp_iwa),y                                                    ; b6f9: 91 2a       .*    
    sta l0038                                                         ; b6fb: 85 38       .8    
    iny                                                               ; b6fd: c8          .     
    lda (zp_iwa),y                                                    ; b6fe: b1 2a       .*    
    adc l04f6,x                                                       ; b700: 7d f6 04    }..   
    sta (zp_iwa),y                                                    ; b703: 91 2a       .*    
    sta zp_fileblk                                                    ; b705: 85 39       .9    
    iny                                                               ; b707: c8          .     
    lda (zp_iwa),y                                                    ; b708: b1 2a       .*    
    adc l04f7,x                                                       ; b70a: 7d f7 04    }..   
    sta (zp_iwa),y                                                    ; b70d: 91 2a       .*    
    tay                                                               ; b70f: a8          .     
    lda zp_general                                                    ; b710: a5 37       .7    
    sec                                                               ; b712: 38          8     
    sbc l04f9,x                                                       ; b713: fd f9 04    ...   
    sta zp_general                                                    ; b716: 85 37       .7    
    lda l0038                                                         ; b718: a5 38       .8    
    sbc l04fa,x                                                       ; b71a: fd fa 04    ...   
    sta l0038                                                         ; b71d: 85 38       .8    
    lda zp_fileblk                                                    ; b71f: a5 39       .9    
    sbc l04fb,x                                                       ; b721: fd fb 04    ...   
    sta zp_fileblk                                                    ; b724: 85 39       .9    
    tya                                                               ; b726: 98          .     
    sbc l04fc,x                                                       ; b727: fd fc 04    ...   
    ora zp_general                                                    ; b72a: 05 37       .7    
    ora l0038                                                         ; b72c: 05 38       .8    
    ora zp_fileblk                                                    ; b72e: 05 39       .9    
    beq cb741                                                         ; b730: f0 0f       ..    
    tya                                                               ; b732: 98          .     
    eor l04f7,x                                                       ; b733: 5d f7 04    ]..   
    eor l04fc,x                                                       ; b736: 5d fc 04    ]..   
    bpl cb73f                                                         ; b739: 10 04       ..    
    bcs cb741                                                         ; b73b: b0 04       ..    
    bcc cb751                                                         ; b73d: 90 12       ..    
; &b73f referenced 1 time by &b739
.cb73f
    bcs cb751                                                         ; b73f: b0 10       ..    
; &b741 referenced 5 times by &b730, &b73b, &b792, &b799, &b79d
.cb741
    ldy l04fe,x                                                       ; b741: bc fe 04    ...   
    lda l04ff,x                                                       ; b744: bd ff 04    ...   
    sty zp_text_ptr                                                   ; b747: 84 0b       ..    
    sta l000c                                                         ; b749: 85 0c       ..    
    jsr c9877                                                         ; b74b: 20 77 98     w.   
    jmp c8ba3                                                         ; b74e: 4c a3 8b    L..   
; &b751 referenced 4 times by &b73d, &b73f, &b79b, &b79f
.cb751
    lda zp_for_level                                                  ; b751: a5 26       .&    
    sec                                                               ; b753: 38          8     
    sbc #&0f                                                          ; b754: e9 0f       ..    
    sta zp_for_level                                                  ; b756: 85 26       .&    
    ldy zp_text_ptr2_off                                              ; b758: a4 1b       ..    
    sty zp_text_ptr_off                                               ; b75a: 84 0a       ..    
    jsr skip_spaces                                                   ; b75c: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; b75f: c9 2c       .,    
    bne cb7a1                                                         ; b761: d0 3e       .>    
    jmp stmt_next                                                     ; b763: 4c 95 b6    L..   
; &b766 referenced 1 time by &b6e6
.cb766
    jsr cb354                                                         ; b766: 20 54 b3     T.   
    lda zp_for_level                                                  ; b769: a5 26       .&    
    clc                                                               ; b76b: 18          .     
    adc #&f4                                                          ; b76c: 69 f4       i.    
    sta zp_fp_ptr                                                     ; b76e: 85 4b       .K    
    lda #5                                                            ; b770: a9 05       ..    
    sta zp_fp_ptr_1                                                   ; b772: 85 4c       .L    
    jsr fwa_add_var                                                   ; b774: 20 00 a5     ..   
    lda zp_iwa                                                        ; b777: a5 2a       .*    
    sta zp_general                                                    ; b779: 85 37       .7    
    lda zp_iwa_1                                                      ; b77b: a5 2b       .+    
    sta l0038                                                         ; b77d: 85 38       .8    
    jsr cb4e9                                                         ; b77f: 20 e9 b4     ..   
    lda zp_for_level                                                  ; b782: a5 26       .&    
    sta zp_var_type                                                   ; b784: 85 27       .'    
    clc                                                               ; b786: 18          .     
    adc #&f9                                                          ; b787: 69 f9       i.    
    sta zp_fp_ptr                                                     ; b789: 85 4b       .K    
    lda #5                                                            ; b78b: a9 05       ..    
    sta zp_fp_ptr_1                                                   ; b78d: 85 4c       .L    
    jsr sub_c9a5f                                                     ; b78f: 20 5f 9a     _.   
    beq cb741                                                         ; b792: f0 ad       ..    
    lda l04f5,x                                                       ; b794: bd f5 04    ...   
    bmi cb79d                                                         ; b797: 30 04       0.    
    bcs cb741                                                         ; b799: b0 a6       ..    
    bcc cb751                                                         ; b79b: 90 b4       ..    
; &b79d referenced 1 time by &b797
.cb79d
    bcc cb741                                                         ; b79d: 90 a2       ..    
    bcs cb751                                                         ; b79f: b0 b0       ..    
; &b7a1 referenced 1 time by &b761
.cb7a1
    jmp c8b96                                                         ; b7a1: 4c 96 8b    L..   
; &b7a4 referenced 2 times by &b7c7, &b7c9
.cb7a4
    brk                                                               ; b7a4: 00          .     
    equb &22, &e3                                                     ; b7a5: 22 e3       ".    
    equs " variable"                                                  ; b7a7: 20 76 61...  va...
; &b7b0 referenced 1 time by &b7d8
.loop_cb7b0
    brk                                                               ; b7b0: 00          .     
    equs "#Too many "                                                 ; b7b1: 23 54 6f... #To...
    equb &e3, &73                                                     ; b7bb: e3 73       .s    
; &b7bd referenced 1 time by &b7ef
.loop_cb7bd
    brk                                                               ; b7bd: 00          .     
    equs "$No "                                                       ; b7be: 24 4e 6f... $No...
    equb &b8, &00                                                     ; b7c2: b8 00       ..    
; ***************************************************************************************
; FOR
;
; Begin a counted loop, stacking the control variable, limit and step. FOR var = start TO
; limit [STEP step].
.stmt_for
    jsr sub_c9582                                                     ; b7c4: 20 82 95     ..   
    beq cb7a4                                                         ; b7c7: f0 db       ..    
    bcs cb7a4                                                         ; b7c9: b0 d9       ..    
    jsr stack_integer                                                 ; b7cb: 20 94 bd     ..   
    jsr sub_c9841                                                     ; b7ce: 20 41 98     A.   
    jsr sub_cb4b1                                                     ; b7d1: 20 b1 b4     ..   
    ldy zp_for_level                                                  ; b7d4: a4 26       .&    
    cpy #&96                                                          ; b7d6: c0 96       ..    
    bcs loop_cb7b0                                                    ; b7d8: b0 d6       ..    
    lda zp_general                                                    ; b7da: a5 37       .7    
    sta for_gosub_stack,y                                             ; b7dc: 99 00 05    ...   
    lda l0038                                                         ; b7df: a5 38       .8    
    sta l0501,y                                                       ; b7e1: 99 01 05    ...   
    lda zp_fileblk                                                    ; b7e4: a5 39       .9    
    sta l0502,y                                                       ; b7e6: 99 02 05    ...   
    tax                                                               ; b7e9: aa          .     
    jsr skip_spaces_ptr2                                              ; b7ea: 20 8c 8a     ..   
    cmp #&b8                                                          ; b7ed: c9 b8       ..    
    bne loop_cb7bd                                                    ; b7ef: d0 cc       ..    
    cpx #5                                                            ; b7f1: e0 05       ..    
    beq cb84f                                                         ; b7f3: f0 5a       .Z    
    jsr sub_c92dd                                                     ; b7f5: 20 dd 92     ..   
    ldy zp_for_level                                                  ; b7f8: a4 26       .&    
    lda zp_iwa                                                        ; b7fa: a5 2a       .*    
    sta l0508,y                                                       ; b7fc: 99 08 05    ...   
    lda zp_iwa_1                                                      ; b7ff: a5 2b       .+    
    sta l0509,y                                                       ; b801: 99 09 05    ...   
    lda zp_iwa_2                                                      ; b804: a5 2c       .,    
    sta l050a,y                                                       ; b806: 99 0a 05    ...   
    lda zp_iwa_3                                                      ; b809: a5 2d       .-    
    sta l050b,y                                                       ; b80b: 99 0b 05    ...   
    lda #1                                                            ; b80e: a9 01       ..    
    jsr caed8                                                         ; b810: 20 d8 ae     ..   
    jsr skip_spaces_ptr2                                              ; b813: 20 8c 8a     ..   
    cmp #&88                                                          ; b816: c9 88       ..    
    bne cb81f                                                         ; b818: d0 05       ..    
    jsr sub_c92dd                                                     ; b81a: 20 dd 92     ..   
    ldy zp_text_ptr2_off                                              ; b81d: a4 1b       ..    
; &b81f referenced 1 time by &b818
.cb81f
    sty zp_text_ptr_off                                               ; b81f: 84 0a       ..    
    ldy zp_for_level                                                  ; b821: a4 26       .&    
    lda zp_iwa                                                        ; b823: a5 2a       .*    
    sta l0503,y                                                       ; b825: 99 03 05    ...   
    lda zp_iwa_1                                                      ; b828: a5 2b       .+    
    sta l0504,y                                                       ; b82a: 99 04 05    ...   
    lda zp_iwa_2                                                      ; b82d: a5 2c       .,    
    sta l0505,y                                                       ; b82f: 99 05 05    ...   
    lda zp_iwa_3                                                      ; b832: a5 2d       .-    
    sta l0506,y                                                       ; b834: 99 06 05    ...   
; &b837 referenced 1 time by &b885
.cb837
    jsr sub_c9880                                                     ; b837: 20 80 98     ..   
    ldy zp_for_level                                                  ; b83a: a4 26       .&    
    lda zp_text_ptr                                                   ; b83c: a5 0b       ..    
    sta l050d,y                                                       ; b83e: 99 0d 05    ...   
    lda l000c                                                         ; b841: a5 0c       ..    
    sta l050e,y                                                       ; b843: 99 0e 05    ...   
    clc                                                               ; b846: 18          .     
    tya                                                               ; b847: 98          .     
    adc #&0f                                                          ; b848: 69 0f       i.    
    sta zp_for_level                                                  ; b84a: 85 26       .&    
    jmp c8ba3                                                         ; b84c: 4c a3 8b    L..   
; &b84f referenced 1 time by &b7f3
.cb84f
    jsr sub_c9b29                                                     ; b84f: 20 29 9b     ).   
    jsr sub_c92fd                                                     ; b852: 20 fd 92     ..   
    lda zp_for_level                                                  ; b855: a5 26       .&    
    clc                                                               ; b857: 18          .     
    adc #8                                                            ; b858: 69 08       i.    
    sta zp_fp_ptr                                                     ; b85a: 85 4b       .K    
    lda #5                                                            ; b85c: a9 05       ..    
    sta zp_fp_ptr_1                                                   ; b85e: 85 4c       .L    
    jsr fwa_pack_var                                                  ; b860: 20 8d a3     ..   
    jsr fwa_set_one                                                   ; b863: 20 99 a6     ..   
    jsr skip_spaces_ptr2                                              ; b866: 20 8c 8a     ..   
    cmp #&88                                                          ; b869: c9 88       ..    
    bne cb875                                                         ; b86b: d0 08       ..    
    jsr sub_c9b29                                                     ; b86d: 20 29 9b     ).   
    jsr sub_c92fd                                                     ; b870: 20 fd 92     ..   
    ldy zp_text_ptr2_off                                              ; b873: a4 1b       ..    
; &b875 referenced 1 time by &b86b
.cb875
    sty zp_text_ptr_off                                               ; b875: 84 0a       ..    
    lda zp_for_level                                                  ; b877: a5 26       .&    
    clc                                                               ; b879: 18          .     
    adc #3                                                            ; b87a: 69 03       i.    
    sta zp_fp_ptr                                                     ; b87c: 85 4b       .K    
    lda #5                                                            ; b87e: a9 05       ..    
    sta zp_fp_ptr_1                                                   ; b880: 85 4c       .L    
    jsr fwa_pack_var                                                  ; b882: 20 8d a3     ..   
    jmp cb837                                                         ; b885: 4c 37 b8    L7.   
; ***************************************************************************************
; GOSUB
;
; Call a subroutine at a line number, stacking the return position. GOSUB line.
.stmt_gosub
    jsr sub_cb99a                                                     ; b888: 20 9a b9     ..   
; &b88b referenced 1 time by &b97a
.cb88b
    jsr check_end_of_statement                                        ; b88b: 20 57 98     W.   
    ldy zp_gosub_level                                                ; b88e: a4 25       .%    
    cpy #&1a                                                          ; b890: c0 1a       ..    
    bcs cb8a2                                                         ; b892: b0 0e       ..    
    lda zp_text_ptr                                                   ; b894: a5 0b       ..    
    sta l05cc,y                                                       ; b896: 99 cc 05    ...   
    lda l000c                                                         ; b899: a5 0c       ..    
    sta l05e6,y                                                       ; b89b: 99 e6 05    ...   
    inc zp_gosub_level                                                ; b89e: e6 25       .%    
    bcc cb8d2                                                         ; b8a0: 90 30       .0    
; &b8a2 referenced 1 time by &b892
.cb8a2
    brk                                                               ; b8a2: 00          .     
    equs "%Too many "                                                 ; b8a3: 25 54 6f... %To...
    equb &e4, &73                                                     ; b8ad: e4 73       .s    
; &b8af referenced 1 time by &b8bb
.loop_cb8af
    brk                                                               ; b8af: 00          .     
    equs "&No "                                                       ; b8b0: 26 4e 6f... &No...
    equb &e4, &00                                                     ; b8b4: e4 00       ..    
; ***************************************************************************************
; RETURN
;
; Return from a GOSUB to the stacked return position. RETURN.
.stmt_return
    jsr check_end_of_statement                                        ; b8b6: 20 57 98     W.   
    ldx zp_gosub_level                                                ; b8b9: a6 25       .%    
    beq loop_cb8af                                                    ; b8bb: f0 f2       ..    
    dec zp_gosub_level                                                ; b8bd: c6 25       .%    
    ldy l05cb,x                                                       ; b8bf: bc cb 05    ...   
    lda l05e5,x                                                       ; b8c2: bd e5 05    ...   
    sty zp_text_ptr                                                   ; b8c5: 84 0b       ..    
    sta l000c                                                         ; b8c7: 85 0c       ..    
    jmp statement_loop                                                ; b8c9: 4c 9b 8b    L..   
; ***************************************************************************************
; GOTO
;
; Jump to a line number. GOTO line.
.stmt_goto
    jsr sub_cb99a                                                     ; b8cc: 20 9a b9     ..   
    jsr check_end_of_statement                                        ; b8cf: 20 57 98     W.   
; &b8d2 referenced 3 times by &98ee, &b8a0, &b967
.cb8d2
    lda zp_trace_flag                                                 ; b8d2: a5 20       .     
    beq cb8d9                                                         ; b8d4: f0 03       ..    
    jsr sub_c9905                                                     ; b8d6: 20 05 99     ..   
; &b8d9 referenced 1 time by &b8d4
.cb8d9
    ldy zp_fwb_exp                                                    ; b8d9: a4 3d       .=    
    lda zp_fwb_m1                                                     ; b8db: a5 3e       .>    
; &b8dd referenced 1 time by &bbd3
.cb8dd
    sty zp_text_ptr                                                   ; b8dd: 84 0b       ..    
    sta l000c                                                         ; b8df: 85 0c       ..    
    jmp c8ba3                                                         ; b8e1: 4c a3 8b    L..   
; &b8e4 referenced 1 time by &b8f7
.loop_cb8e4
    jsr check_end_of_statement                                        ; b8e4: 20 57 98     W.   
    lda #&33 ; '3'                                                    ; b8e7: a9 33       .3    
    sta zp_error_vec                                                  ; b8e9: 85 16       ..    
    lda #&b4                                                          ; b8eb: a9 b4       ..    
    sta l0017                                                         ; b8ed: 85 17       ..    
    jmp statement_loop                                                ; b8ef: 4c 9b 8b    L..   
; &b8f2 referenced 1 time by &b91a
.loop_cb8f2
    jsr skip_spaces                                                   ; b8f2: 20 97 8a     ..   
    cmp #&87                                                          ; b8f5: c9 87       ..    
    beq loop_cb8e4                                                    ; b8f7: f0 eb       ..    
    ldy zp_text_ptr_off                                               ; b8f9: a4 0a       ..    
    dey                                                               ; b8fb: 88          .     
    jsr c986d                                                         ; b8fc: 20 6d 98     m.   
    lda zp_text_ptr                                                   ; b8ff: a5 0b       ..    
    sta zp_error_vec                                                  ; b901: 85 16       ..    
    lda l000c                                                         ; b903: a5 0c       ..    
    sta l0017                                                         ; b905: 85 17       ..    
    jmp stmt_data                                                     ; b907: 4c 7d 8b    L}.   
; &b90a referenced 1 time by &b92f
.loop_cb90a
    brk                                                               ; b90a: 00          .     
    equb &27, &ee                                                     ; b90b: 27 ee       '.    
    equs " syntax"                                                    ; b90d: 20 73 79...  sy...
    equb &00                                                          ; b914: 00          .     
; ***************************************************************************************
; ON
;
; ON expr GOTO/GOSUB computed jump, or ON ERROR error trapping. ON expr GOTO/GOSUB list |
; ON ERROR stmts.
.stmt_on
    jsr skip_spaces                                                   ; b915: 20 97 8a     ..   
    cmp #&85                                                          ; b918: c9 85       ..    
    beq loop_cb8f2                                                    ; b91a: f0 d6       ..    
    dec zp_text_ptr_off                                               ; b91c: c6 0a       ..    
    jsr eval_expr                                                     ; b91e: 20 1d 9b     ..   
    jsr coerce_to_integer                                             ; b921: 20 f0 92     ..   
    ldy zp_text_ptr2_off                                              ; b924: a4 1b       ..    
    iny                                                               ; b926: c8          .     
    sty zp_text_ptr_off                                               ; b927: 84 0a       ..    
    cpx #&e5                                                          ; b929: e0 e5       ..    
    beq cb931                                                         ; b92b: f0 04       ..    
    cpx #&e4                                                          ; b92d: e0 e4       ..    
    bne loop_cb90a                                                    ; b92f: d0 d9       ..    
; &b931 referenced 1 time by &b92b
.cb931
    txa                                                               ; b931: 8a          .     
    pha                                                               ; b932: 48          H     
    lda zp_iwa_1                                                      ; b933: a5 2b       .+    
    ora zp_iwa_2                                                      ; b935: 05 2c       .,    
    ora zp_iwa_3                                                      ; b937: 05 2d       .-    
    bne cb97d                                                         ; b939: d0 42       .B    
    ldx zp_iwa                                                        ; b93b: a6 2a       .*    
    beq cb97d                                                         ; b93d: f0 3e       .>    
    dex                                                               ; b93f: ca          .     
    beq cb95c                                                         ; b940: f0 1a       ..    
    ldy zp_text_ptr_off                                               ; b942: a4 0a       ..    
; &b944 referenced 2 times by &b955, &b958
.cb944
    lda (zp_text_ptr),y                                               ; b944: b1 0b       ..    
    iny                                                               ; b946: c8          .     
    cmp #&0d                                                          ; b947: c9 0d       ..    
    beq cb97d                                                         ; b949: f0 32       .2    
    cmp #&3a ; ':'                                                    ; b94b: c9 3a       .:    
    beq cb97d                                                         ; b94d: f0 2e       ..    
    cmp #&8b                                                          ; b94f: c9 8b       ..    
    beq cb97d                                                         ; b951: f0 2a       .*    
    cmp #&2c ; ','                                                    ; b953: c9 2c       .,    
    bne cb944                                                         ; b955: d0 ed       ..    
    dex                                                               ; b957: ca          .     
    bne cb944                                                         ; b958: d0 ea       ..    
    sty zp_text_ptr_off                                               ; b95a: 84 0a       ..    
; &b95c referenced 1 time by &b940
.cb95c
    jsr sub_cb99a                                                     ; b95c: 20 9a b9     ..   
    pla                                                               ; b95f: 68          h     
    cmp #&e4                                                          ; b960: c9 e4       ..    
    beq cb96a                                                         ; b962: f0 06       ..    
    jsr c9877                                                         ; b964: 20 77 98     w.   
    jmp cb8d2                                                         ; b967: 4c d2 b8    L..   
; &b96a referenced 1 time by &b962
.cb96a
    ldy zp_text_ptr_off                                               ; b96a: a4 0a       ..    
; &b96c referenced 1 time by &b975
.loop_cb96c
    lda (zp_text_ptr),y                                               ; b96c: b1 0b       ..    
    iny                                                               ; b96e: c8          .     
    cmp #&0d                                                          ; b96f: c9 0d       ..    
    beq cb977                                                         ; b971: f0 04       ..    
    cmp #&3a ; ':'                                                    ; b973: c9 3a       .:    
    bne loop_cb96c                                                    ; b975: d0 f5       ..    
; &b977 referenced 1 time by &b971
.cb977
    dey                                                               ; b977: 88          .     
    sty zp_text_ptr_off                                               ; b978: 84 0a       ..    
    jmp cb88b                                                         ; b97a: 4c 8b b8    L..   
; &b97d referenced 5 times by &b939, &b93d, &b949, &b94d, &b951
.cb97d
    ldy zp_text_ptr_off                                               ; b97d: a4 0a       ..    
    pla                                                               ; b97f: 68          h     
; &b980 referenced 1 time by &b989
.loop_cb980
    lda (zp_text_ptr),y                                               ; b980: b1 0b       ..    
    iny                                                               ; b982: c8          .     
    cmp #&8b                                                          ; b983: c9 8b       ..    
    beq cb995                                                         ; b985: f0 0e       ..    
    cmp #&0d                                                          ; b987: c9 0d       ..    
    bne loop_cb980                                                    ; b989: d0 f5       ..    
    brk                                                               ; b98b: 00          .     
    equb &28, &ee                                                     ; b98c: 28 ee       (.    
    equs " range"                                                     ; b98e: 20 72 61...  ra...
    equb &00                                                          ; b994: 00          .     
; &b995 referenced 1 time by &b985
.cb995
    sty zp_text_ptr_off                                               ; b995: 84 0a       ..    
    jmp c98e3                                                         ; b997: 4c e3 98    L..   
; &b99a referenced 4 times by &b888, &b8cc, &b95c, &baff
.sub_cb99a
    jsr sub_c97df                                                     ; b99a: 20 df 97     ..   
    bcs cb9af                                                         ; b99d: b0 10       ..    
    jsr eval_expr                                                     ; b99f: 20 1d 9b     ..   
    jsr coerce_to_integer                                             ; b9a2: 20 f0 92     ..   
    lda zp_text_ptr2_off                                              ; b9a5: a5 1b       ..    
    sta zp_text_ptr_off                                               ; b9a7: 85 0a       ..    
    lda zp_iwa_1                                                      ; b9a9: a5 2b       .+    
    and #&7f                                                          ; b9ab: 29 7f       ).    
    sta zp_iwa_1                                                      ; b9ad: 85 2b       .+    
; &b9af referenced 2 times by &98e8, &b99d
.cb9af
    jsr sub_c9970                                                     ; b9af: 20 70 99     p.   
    bcs cb9b5                                                         ; b9b2: b0 01       ..    
    rts                                                               ; b9b4: 60          `     
; &b9b5 referenced 1 time by &b9b2
.cb9b5
    brk                                                               ; b9b5: 00          .     
    equs ")No such line"                                              ; b9b6: 29 4e 6f... )No...
    equb &00                                                          ; b9c3: 00          .     
; &b9c4 referenced 2 times by &ba00, &ba1b
.cb9c4
    jmp c8c0e                                                         ; b9c4: 4c 0e 8c    L..   
; &b9c7 referenced 1 time by &b9e7
.loop_cb9c7
    jmp c982a                                                         ; b9c7: 4c 2a 98    L*.   
; &b9ca referenced 1 time by &b9df
.loop_cb9ca
    sty zp_text_ptr_off                                               ; b9ca: 84 0a       ..    
    jmp c8b98                                                         ; b9cc: 4c 98 8b    L..   
; &b9cf referenced 1 time by &ba49
.loop_cb9cf
    dec zp_text_ptr_off                                               ; b9cf: c6 0a       ..    
    jsr sub_cbfa9                                                     ; b9d1: 20 a9 bf     ..   
    lda zp_text_ptr2_off                                              ; b9d4: a5 1b       ..    
    sta zp_text_ptr_off                                               ; b9d6: 85 0a       ..    
    sty l004d                                                         ; b9d8: 84 4d       .M    
; &b9da referenced 2 times by &ba16, &ba3c
.cb9da
    jsr skip_spaces                                                   ; b9da: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; b9dd: c9 2c       .,    
    bne loop_cb9ca                                                    ; b9df: d0 e9       ..    
    lda l004d                                                         ; b9e1: a5 4d       .M    
    pha                                                               ; b9e3: 48          H     
    jsr sub_c9582                                                     ; b9e4: 20 82 95     ..   
    beq loop_cb9c7                                                    ; b9e7: f0 de       ..    
    lda zp_text_ptr2_off                                              ; b9e9: a5 1b       ..    
    sta zp_text_ptr_off                                               ; b9eb: 85 0a       ..    
    pla                                                               ; b9ed: 68          h     
    sta l004d                                                         ; b9ee: 85 4d       .M    
    php                                                               ; b9f0: 08          .     
    jsr stack_integer                                                 ; b9f1: 20 94 bd     ..   
    ldy l004d                                                         ; b9f4: a4 4d       .M    
    jsr osbget                                                        ; b9f6: 20 d7 ff     ..   
    sta zp_var_type                                                   ; b9f9: 85 27       .'    
    plp                                                               ; b9fb: 28          (     
    bcc cba19                                                         ; b9fc: 90 1b       ..    
    lda zp_var_type                                                   ; b9fe: a5 27       .'    
    bne cb9c4                                                         ; ba00: d0 c2       ..    
    jsr osbget                                                        ; ba02: 20 d7 ff     ..   
    sta zp_strbuf_len                                                 ; ba05: 85 36       .6    
    tax                                                               ; ba07: aa          .     
    beq cba13                                                         ; ba08: f0 09       ..    
; &ba0a referenced 1 time by &ba11
.loop_cba0a
    jsr osbget                                                        ; ba0a: 20 d7 ff     ..   
    sta l05ff,x                                                       ; ba0d: 9d ff 05    ...   
    dex                                                               ; ba10: ca          .     
    bne loop_cba0a                                                    ; ba11: d0 f7       ..    
; &ba13 referenced 1 time by &ba08
.cba13
    jsr sub_c8c1e                                                     ; ba13: 20 1e 8c     ..   
    jmp cb9da                                                         ; ba16: 4c da b9    L..   
; &ba19 referenced 1 time by &b9fc
.cba19
    lda zp_var_type                                                   ; ba19: a5 27       .'    
    beq cb9c4                                                         ; ba1b: f0 a7       ..    
    bmi cba2b                                                         ; ba1d: 30 0c       0.    
    ldx #3                                                            ; ba1f: a2 03       ..    
; &ba21 referenced 1 time by &ba27
.loop_cba21
    jsr osbget                                                        ; ba21: 20 d7 ff     ..   
    sta zp_iwa,x                                                      ; ba24: 95 2a       .*    
    dex                                                               ; ba26: ca          .     
    bpl loop_cba21                                                    ; ba27: 10 f8       ..    
    bmi cba39                                                         ; ba29: 30 0e       0.    
; &ba2b referenced 1 time by &ba1d
.cba2b
    ldx #4                                                            ; ba2b: a2 04       ..    
; &ba2d referenced 1 time by &ba34
.loop_cba2d
    jsr osbget                                                        ; ba2d: 20 d7 ff     ..   
    sta fp_temp1,x                                                    ; ba30: 9d 6c 04    .l.   
    dex                                                               ; ba33: ca          .     
    bpl loop_cba2d                                                    ; ba34: 10 f7       ..    
    jsr fwa_unpack_temp1                                              ; ba36: 20 b2 a3     ..   
; &ba39 referenced 1 time by &ba29
.cba39
    jsr sub_cb4b4                                                     ; ba39: 20 b4 b4     ..   
    jmp cb9da                                                         ; ba3c: 4c da b9    L..   
; &ba3f referenced 1 time by &ba82
.loop_cba3f
    pla                                                               ; ba3f: 68          h     
    pla                                                               ; ba40: 68          h     
    jmp c8b98                                                         ; ba41: 4c 98 8b    L..   
; ***************************************************************************************
; INPUT
;
; Read values from the keyboard, or a file with #, into variables. INPUT [LINE] [prompt]
; var,...
.stmt_input
    jsr skip_spaces                                                   ; ba44: 20 97 8a     ..   
    cmp #&23 ; '#'                                                    ; ba47: c9 23       .#    
    beq loop_cb9cf                                                    ; ba49: f0 84       ..    
    cmp #&86                                                          ; ba4b: c9 86       ..    
    beq cba52                                                         ; ba4d: f0 03       ..    
    dec zp_text_ptr_off                                               ; ba4f: c6 0a       ..    
    clc                                                               ; ba51: 18          .     
; &ba52 referenced 1 time by &ba4d
.cba52
    ror l004d                                                         ; ba52: 66 4d       fM    
    lsr l004d                                                         ; ba54: 46 4d       FM    
    lda #&ff                                                          ; ba56: a9 ff       ..    
    sta l004e                                                         ; ba58: 85 4e       .N    
; &ba5a referenced 4 times by &ba71, &ba75, &bad9, &bae3
.cba5a
    jsr sub_c8e8a                                                     ; ba5a: 20 8a 8e     ..   
    bcs cba69                                                         ; ba5d: b0 0a       ..    
; &ba5f referenced 1 time by &ba62
.loop_cba5f
    jsr sub_c8e8a                                                     ; ba5f: 20 8a 8e     ..   
    bcc loop_cba5f                                                    ; ba62: 90 fb       ..    
    ldx #&ff                                                          ; ba64: a2 ff       ..    
    stx l004e                                                         ; ba66: 86 4e       .N    
    clc                                                               ; ba68: 18          .     
; &ba69 referenced 1 time by &ba5d
.cba69
    php                                                               ; ba69: 08          .     
    asl l004d                                                         ; ba6a: 06 4d       .M    
    plp                                                               ; ba6c: 28          (     
    ror l004d                                                         ; ba6d: 66 4d       fM    
    cmp #&2c ; ','                                                    ; ba6f: c9 2c       .,    
    beq cba5a                                                         ; ba71: f0 e7       ..    
    cmp #&3b ; ';'                                                    ; ba73: c9 3b       .;    
    beq cba5a                                                         ; ba75: f0 e3       ..    
    dec zp_text_ptr_off                                               ; ba77: c6 0a       ..    
    lda l004d                                                         ; ba79: a5 4d       .M    
    pha                                                               ; ba7b: 48          H     
    lda l004e                                                         ; ba7c: a5 4e       .N    
    pha                                                               ; ba7e: 48          H     
    jsr sub_c9582                                                     ; ba7f: 20 82 95     ..   
    beq loop_cba3f                                                    ; ba82: f0 bb       ..    
    pla                                                               ; ba84: 68          h     
    sta l004e                                                         ; ba85: 85 4e       .N    
    pla                                                               ; ba87: 68          h     
    sta l004d                                                         ; ba88: 85 4d       .M    
    lda zp_text_ptr2_off                                              ; ba8a: a5 1b       ..    
    sta zp_text_ptr_off                                               ; ba8c: 85 0a       ..    
    php                                                               ; ba8e: 08          .     
    bit l004d                                                         ; ba8f: 24 4d       $M    
    bvs cba99                                                         ; ba91: 70 06       p.    
    lda l004e                                                         ; ba93: a5 4e       .N    
    cmp #&ff                                                          ; ba95: c9 ff       ..    
    bne cbab0                                                         ; ba97: d0 17       ..    
; &ba99 referenced 1 time by &ba91
.cba99
    bit l004d                                                         ; ba99: 24 4d       $M    
    bpl cbaa2                                                         ; ba9b: 10 05       ..    
    lda #&3f ; '?'                                                    ; ba9d: a9 3f       .?    
    jsr cb558                                                         ; ba9f: 20 58 b5     X.   
; &baa2 referenced 1 time by &ba9b
.cbaa2
    jsr sub_cbbfc                                                     ; baa2: 20 fc bb     ..   
    sty zp_strbuf_len                                                 ; baa5: 84 36       .6    
    asl l004d                                                         ; baa7: 06 4d       .M    
    clc                                                               ; baa9: 18          .     
    ror l004d                                                         ; baaa: 66 4d       fM    
    bit l004d                                                         ; baac: 24 4d       $M    
    bvs cbacd                                                         ; baae: 70 1d       p.    
; &bab0 referenced 1 time by &ba97
.cbab0
    sta zp_text_ptr2_off                                              ; bab0: 85 1b       ..    
    lda #0                                                            ; bab2: a9 00       ..    
    sta zp_text_ptr2                                                  ; bab4: 85 19       ..    
    lda #6                                                            ; bab6: a9 06       ..    
    sta l001a                                                         ; bab8: 85 1a       ..    
    jsr sub_cadad                                                     ; baba: 20 ad ad     ..   
; &babd referenced 1 time by &bac6
.loop_cbabd
    jsr skip_spaces_ptr2                                              ; babd: 20 8c 8a     ..   
    cmp #&2c ; ','                                                    ; bac0: c9 2c       .,    
    beq cbaca                                                         ; bac2: f0 06       ..    
    cmp #&0d                                                          ; bac4: c9 0d       ..    
    bne loop_cbabd                                                    ; bac6: d0 f5       ..    
    ldy #&fe                                                          ; bac8: a0 fe       ..    
; &baca referenced 1 time by &bac2
.cbaca
    iny                                                               ; baca: c8          .     
    sty l004e                                                         ; bacb: 84 4e       .N    
; &bacd referenced 1 time by &baae
.cbacd
    plp                                                               ; bacd: 28          (     
    bcs cbadc                                                         ; bace: b0 0c       ..    
    jsr stack_integer                                                 ; bad0: 20 94 bd     ..   
    jsr ascii_to_number                                               ; bad3: 20 34 ac     4.   
    jsr sub_cb4b4                                                     ; bad6: 20 b4 b4     ..   
    jmp cba5a                                                         ; bad9: 4c 5a ba    LZ.   
; &badc referenced 1 time by &bace
.cbadc
    lda #0                                                            ; badc: a9 00       ..    
    sta zp_var_type                                                   ; bade: 85 27       .'    
    jsr sub_c8c21                                                     ; bae0: 20 21 8c     !.   
    jmp cba5a                                                         ; bae3: 4c 5a ba    LZ.   
; ***************************************************************************************
; RESTORE
;
; Reset the DATA pointer, optionally to a given line. RESTORE [line].
.stmt_restore
    ldy #0                                                            ; bae6: a0 00       ..    
    sty zp_fwb_exp                                                    ; bae8: 84 3d       .=    
    ldy zp_page                                                       ; baea: a4 18       ..    
    sty zp_fwb_m1                                                     ; baec: 84 3e       .>    
    jsr skip_spaces                                                   ; baee: 20 97 8a     ..   
    dec zp_text_ptr_off                                               ; baf1: c6 0a       ..    
    cmp #&3a ; ':'                                                    ; baf3: c9 3a       .:    
    beq cbb07                                                         ; baf5: f0 10       ..    
    cmp #&0d                                                          ; baf7: c9 0d       ..    
    beq cbb07                                                         ; baf9: f0 0c       ..    
    cmp #&8b                                                          ; bafb: c9 8b       ..    
    beq cbb07                                                         ; bafd: f0 08       ..    
    jsr sub_cb99a                                                     ; baff: 20 9a b9     ..   
    ldy #1                                                            ; bb02: a0 01       ..    
    jsr sub_cbe55                                                     ; bb04: 20 55 be     U.   
; &bb07 referenced 3 times by &baf5, &baf9, &bafd
.cbb07
    jsr check_end_of_statement                                        ; bb07: 20 57 98     W.   
    lda zp_fwb_exp                                                    ; bb0a: a5 3d       .=    
    sta zp_data_ptr                                                   ; bb0c: 85 1c       ..    
    lda zp_fwb_m1                                                     ; bb0e: a5 3e       .>    
    sta l001d                                                         ; bb10: 85 1d       ..    
    jmp statement_loop                                                ; bb12: 4c 9b 8b    L..   
; &bb15 referenced 2 times by &bb22, &bb4d
.cbb15
    jsr skip_spaces                                                   ; bb15: 20 97 8a     ..   
    cmp #&2c ; ','                                                    ; bb18: c9 2c       .,    
    beq stmt_read                                                     ; bb1a: f0 03       ..    
    jmp c8b96                                                         ; bb1c: 4c 96 8b    L..   
; ***************************************************************************************
; READ
;
; Read values from DATA statements into variables. READ var,...
; &bb1f referenced 1 time by &bb1a
.stmt_read
    jsr sub_c9582                                                     ; bb1f: 20 82 95     ..   
    beq cbb15                                                         ; bb22: f0 f1       ..    
    bcs cbb32                                                         ; bb24: b0 0c       ..    
    jsr sub_cbb50                                                     ; bb26: 20 50 bb     P.   
    jsr stack_integer                                                 ; bb29: 20 94 bd     ..   
    jsr sub_cb4b1                                                     ; bb2c: 20 b1 b4     ..   
    jmp cbb40                                                         ; bb2f: 4c 40 bb    L@.   
; &bb32 referenced 1 time by &bb24
.cbb32
    jsr sub_cbb50                                                     ; bb32: 20 50 bb     P.   
    jsr stack_integer                                                 ; bb35: 20 94 bd     ..   
    jsr sub_cadad                                                     ; bb38: 20 ad ad     ..   
    sta zp_var_type                                                   ; bb3b: 85 27       .'    
    jsr sub_c8c1e                                                     ; bb3d: 20 1e 8c     ..   
; &bb40 referenced 1 time by &bb2f
.cbb40
    clc                                                               ; bb40: 18          .     
    lda zp_text_ptr2_off                                              ; bb41: a5 1b       ..    
    adc zp_text_ptr2                                                  ; bb43: 65 19       e.    
    sta zp_data_ptr                                                   ; bb45: 85 1c       ..    
    lda l001a                                                         ; bb47: a5 1a       ..    
    adc #0                                                            ; bb49: 69 00       i.    
    sta l001d                                                         ; bb4b: 85 1d       ..    
    jmp cbb15                                                         ; bb4d: 4c 15 bb    L..   
; &bb50 referenced 2 times by &bb26, &bb32
.sub_cbb50
    lda zp_text_ptr2_off                                              ; bb50: a5 1b       ..    
    sta zp_text_ptr_off                                               ; bb52: 85 0a       ..    
    lda zp_data_ptr                                                   ; bb54: a5 1c       ..    
    sta zp_text_ptr2                                                  ; bb56: 85 19       ..    
    lda l001d                                                         ; bb58: a5 1d       ..    
    sta l001a                                                         ; bb5a: 85 1a       ..    
    ldy #0                                                            ; bb5c: a0 00       ..    
    sty zp_text_ptr2_off                                              ; bb5e: 84 1b       ..    
    jsr skip_spaces_ptr2                                              ; bb60: 20 8c 8a     ..   
    cmp #&2c ; ','                                                    ; bb63: c9 2c       .,    
    beq return_36                                                     ; bb65: f0 49       .I    
    cmp #&dc                                                          ; bb67: c9 dc       ..    
    beq return_36                                                     ; bb69: f0 45       .E    
    cmp #&0d                                                          ; bb6b: c9 0d       ..    
    beq cbb7a                                                         ; bb6d: f0 0b       ..    
; &bb6f referenced 1 time by &bb78
.loop_cbb6f
    jsr skip_spaces_ptr2                                              ; bb6f: 20 8c 8a     ..   
    cmp #&2c ; ','                                                    ; bb72: c9 2c       .,    
    beq return_36                                                     ; bb74: f0 3a       .:    
    cmp #&0d                                                          ; bb76: c9 0d       ..    
    bne loop_cbb6f                                                    ; bb78: d0 f5       ..    
; &bb7a referenced 3 times by &bb6d, &bb96, &bb9a
.cbb7a
    ldy zp_text_ptr2_off                                              ; bb7a: a4 1b       ..    
    lda (zp_text_ptr2),y                                              ; bb7c: b1 19       ..    
    bmi cbb9c                                                         ; bb7e: 30 1c       0.    
    iny                                                               ; bb80: c8          .     
    iny                                                               ; bb81: c8          .     
    lda (zp_text_ptr2),y                                              ; bb82: b1 19       ..    
    tax                                                               ; bb84: aa          .     
; &bb85 referenced 1 time by &bb8a
.loop_cbb85
    iny                                                               ; bb85: c8          .     
    lda (zp_text_ptr2),y                                              ; bb86: b1 19       ..    
    cmp #&20 ; ' '                                                    ; bb88: c9 20       .     
    beq loop_cbb85                                                    ; bb8a: f0 f9       ..    
    cmp #&dc                                                          ; bb8c: c9 dc       ..    
    beq cbbad                                                         ; bb8e: f0 1d       ..    
    txa                                                               ; bb90: 8a          .     
    clc                                                               ; bb91: 18          .     
    adc zp_text_ptr2                                                  ; bb92: 65 19       e.    
    sta zp_text_ptr2                                                  ; bb94: 85 19       ..    
    bcc cbb7a                                                         ; bb96: 90 e2       ..    
    inc l001a                                                         ; bb98: e6 1a       ..    
    bcs cbb7a                                                         ; bb9a: b0 de       ..    
; &bb9c referenced 1 time by &bb7e
.cbb9c
    brk                                                               ; bb9c: 00          .     
    equs "*Out of "                                                   ; bb9d: 2a 4f 75... *Ou...
    equb &dc                                                          ; bba5: dc          .     
; &bba6 referenced 1 time by &bbbc
.loop_cbba6
    brk                                                               ; bba6: 00          .     
    equs "+No "                                                       ; bba7: 2b 4e 6f... +No...
    equb &f5, &00                                                     ; bbab: f5 00       ..    
; &bbad referenced 1 time by &bb8e
.cbbad
    iny                                                               ; bbad: c8          .     
    sty zp_text_ptr2_off                                              ; bbae: 84 1b       ..    
; &bbb0 referenced 3 times by &bb65, &bb69, &bb74
.return_36
    rts                                                               ; bbb0: 60          `     
; ***************************************************************************************
; UNTIL
;
; End a REPEAT loop: loop back unless the condition is true. UNTIL expr.
.stmt_until
    jsr eval_expr                                                     ; bbb1: 20 1d 9b     ..   
    jsr c984c                                                         ; bbb4: 20 4c 98     L.   
    jsr sub_c92ee                                                     ; bbb7: 20 ee 92     ..   
    ldx zp_repeat_level                                               ; bbba: a6 24       .$    
    beq loop_cbba6                                                    ; bbbc: f0 e8       ..    
    lda zp_iwa                                                        ; bbbe: a5 2a       .*    
    ora zp_iwa_1                                                      ; bbc0: 05 2b       .+    
    ora zp_iwa_2                                                      ; bbc2: 05 2c       .,    
    ora zp_iwa_3                                                      ; bbc4: 05 2d       .-    
    beq cbbcd                                                         ; bbc6: f0 05       ..    
    dec zp_repeat_level                                               ; bbc8: c6 24       .$    
    jmp statement_loop                                                ; bbca: 4c 9b 8b    L..   
; &bbcd referenced 1 time by &bbc6
.cbbcd
    ldy l05a3,x                                                       ; bbcd: bc a3 05    ...   
    lda l05b7,x                                                       ; bbd0: bd b7 05    ...   
    jmp cb8dd                                                         ; bbd3: 4c dd b8    L..   
; &bbd6 referenced 1 time by &bbe8
.loop_cbbd6
    brk                                                               ; bbd6: 00          .     
    equs ",Too many "                                                 ; bbd7: 2c 54 6f... ,To...
    equb &f5, &73, &00                                                ; bbe1: f5 73 00    .s.   
; ***************************************************************************************
; REPEAT
;
; Begin a REPEAT...UNTIL loop, stacking the loop position. REPEAT.
.stmt_repeat
    ldx zp_repeat_level                                               ; bbe4: a6 24       .$    
    cpx #&14                                                          ; bbe6: e0 14       ..    
    bcs loop_cbbd6                                                    ; bbe8: b0 ec       ..    
    jsr c986d                                                         ; bbea: 20 6d 98     m.   
    lda zp_text_ptr                                                   ; bbed: a5 0b       ..    
    sta l05a4,x                                                       ; bbef: 9d a4 05    ...   
    lda l000c                                                         ; bbf2: a5 0c       ..    
    sta l05b8,x                                                       ; bbf4: 9d b8 05    ...   
    inc zp_repeat_level                                               ; bbf7: e6 24       .$    
    jmp c8ba3                                                         ; bbf9: 4c a3 8b    L..   
; &bbfc referenced 1 time by &baa2
.sub_cbbfc
    ldy #0                                                            ; bbfc: a0 00       ..    
    lda #6                                                            ; bbfe: a9 06       ..    
    bne cbc09                                                         ; bc00: d0 07       ..    
; &bc02 referenced 2 times by &8b08, &90bd
.sub_cbc02
    jsr cb558                                                         ; bc02: 20 58 b5     X.   
    ldy #0                                                            ; bc05: a0 00       ..    
    lda #7                                                            ; bc07: a9 07       ..    
; &bc09 referenced 1 time by &bc00
.cbc09
    sty zp_general                                                    ; bc09: 84 37       .7    
    sta l0038                                                         ; bc0b: 85 38       .8    
    lda #&ee                                                          ; bc0d: a9 ee       ..    
    sta zp_fileblk                                                    ; bc0f: 85 39       .9    
    lda #&20 ; ' '                                                    ; bc11: a9 20       .     
    sta l003a                                                         ; bc13: 85 3a       .:    
    ldy #&ff                                                          ; bc15: a0 ff       ..    
    sty zp_fwb_sign                                                   ; bc17: 84 3b       .;    
    iny                                                               ; bc19: c8          .     
    ldx #&37 ; '7'                                                    ; bc1a: a2 37       .7    
    tya                                                               ; bc1c: 98          .     
    jsr osword                                                        ; bc1d: 20 f1 ff     ..   
    bcc cbc28                                                         ; bc20: 90 06       ..    
    jmp c9838                                                         ; bc22: 4c 38 98    L8.   
; &bc25 referenced 8 times by &853f, &857b, &8d7d, &8e53, &8e67, &b56e, &b5fc, &bfe7
.sub_cbc25
    jsr osnewl                                                        ; bc25: 20 e7 ff     ..   
; &bc28 referenced 4 times by &8ec7, &93d7, &b55f, &bc20
.cbc28
    lda #0                                                            ; bc28: a9 00       ..    
    sta zp_count                                                      ; bc2a: 85 1e       ..    
    rts                                                               ; bc2c: 60          `     
; &bc2d referenced 2 times by &8f53, &bc8f
.sub_cbc2d
    jsr sub_c9970                                                     ; bc2d: 20 70 99     p.   
    bcs return_37                                                     ; bc30: b0 4e       .N    
    lda zp_fwb_exp                                                    ; bc32: a5 3d       .=    
    sbc #2                                                            ; bc34: e9 02       ..    
    sta zp_general                                                    ; bc36: 85 37       .7    
    sta zp_fwb_exp                                                    ; bc38: 85 3d       .=    
    sta zp_top                                                        ; bc3a: 85 12       ..    
    lda zp_fwb_m1                                                     ; bc3c: a5 3e       .>    
    sbc #0                                                            ; bc3e: e9 00       ..    
    sta l0038                                                         ; bc40: 85 38       .8    
    sta l0013                                                         ; bc42: 85 13       ..    
    sta zp_fwb_m1                                                     ; bc44: 85 3e       .>    
    ldy #3                                                            ; bc46: a0 03       ..    
    lda (zp_general),y                                                ; bc48: b1 37       .7    
    clc                                                               ; bc4a: 18          .     
    adc zp_general                                                    ; bc4b: 65 37       e7    
    sta zp_general                                                    ; bc4d: 85 37       .7    
    bcc cbc53                                                         ; bc4f: 90 02       ..    
    inc l0038                                                         ; bc51: e6 38       .8    
; &bc53 referenced 1 time by &bc4f
.cbc53
    ldy #0                                                            ; bc53: a0 00       ..    
; &bc55 referenced 2 times by &bc5e, &bc64
.cbc55
    lda (zp_general),y                                                ; bc55: b1 37       .7    
    sta (zp_top),y                                                    ; bc57: 91 12       ..    
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
    lda (zp_general),y                                                ; bc6d: b1 37       .7    
    sta (zp_top),y                                                    ; bc6f: 91 12       ..    
    bmi cbc7c                                                         ; bc71: 30 09       0.    
    jsr sub_cbc81                                                     ; bc73: 20 81 bc     ..   
    jsr sub_cbc81                                                     ; bc76: 20 81 bc     ..   
    jmp cbc5d                                                         ; bc79: 4c 5d bc    L].   
; &bc7c referenced 1 time by &bc71
.cbc7c
    jsr sub_cbe92                                                     ; bc7c: 20 92 be     ..   
    clc                                                               ; bc7f: 18          .     
; &bc80 referenced 1 time by &bc30
.return_37
    rts                                                               ; bc80: 60          `     
; &bc81 referenced 2 times by &bc73, &bc76
.sub_cbc81
    iny                                                               ; bc81: c8          .     
    bne cbc88                                                         ; bc82: d0 04       ..    
    inc l0013                                                         ; bc84: e6 13       ..    
    inc l0038                                                         ; bc86: e6 38       .8    
; &bc88 referenced 1 time by &bc82
.cbc88
    lda (zp_general),y                                                ; bc88: b1 37       .7    
    sta (zp_top),y                                                    ; bc8a: 91 12       ..    
    rts                                                               ; bc8c: 60          `     
; &bc8d referenced 2 times by &8b32, &90c6
.sub_cbc8d
    sty zp_fwb_sign                                                   ; bc8d: 84 3b       .;    
    jsr sub_cbc2d                                                     ; bc8f: 20 2d bc     -.   
    ldy #7                                                            ; bc92: a0 07       ..    
    sty zp_fwb_ovf                                                    ; bc94: 84 3c       .<    
    ldy #0                                                            ; bc96: a0 00       ..    
    lda #&0d                                                          ; bc98: a9 0d       ..    
    cmp (zp_fwb_sign),y                                               ; bc9a: d1 3b       .;    
    beq return_38                                                     ; bc9c: f0 72       .r    
; &bc9e referenced 1 time by &bca1
.loop_cbc9e
    iny                                                               ; bc9e: c8          .     
    cmp (zp_fwb_sign),y                                               ; bc9f: d1 3b       .;    
    bne loop_cbc9e                                                    ; bca1: d0 fb       ..    
    iny                                                               ; bca3: c8          .     
    iny                                                               ; bca4: c8          .     
    iny                                                               ; bca5: c8          .     
    sty zp_fwb_m2                                                     ; bca6: 84 3f       .?    
    inc zp_fwb_m2                                                     ; bca8: e6 3f       .?    
    lda zp_top                                                        ; bcaa: a5 12       ..    
    sta zp_fileblk                                                    ; bcac: 85 39       .9    
    lda l0013                                                         ; bcae: a5 13       ..    
    sta l003a                                                         ; bcb0: 85 3a       .:    
    jsr sub_cbe92                                                     ; bcb2: 20 92 be     ..   
    sta zp_general                                                    ; bcb5: 85 37       .7    
    lda l0013                                                         ; bcb7: a5 13       ..    
    sta l0038                                                         ; bcb9: 85 38       .8    
    dey                                                               ; bcbb: 88          .     
    lda zp_himem                                                      ; bcbc: a5 06       ..    
    cmp zp_top                                                        ; bcbe: c5 12       ..    
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
    lda (zp_fileblk),y                                                ; bcd6: b1 39       .9    
    sta (zp_general),y                                                ; bcd8: 91 37       .7    
    tya                                                               ; bcda: 98          .     
    bne cbce1                                                         ; bcdb: d0 04       ..    
    dec l003a                                                         ; bcdd: c6 3a       .:    
    dec l0038                                                         ; bcdf: c6 38       .8    
; &bce1 referenced 1 time by &bcdb
.cbce1
    dey                                                               ; bce1: 88          .     
    tya                                                               ; bce2: 98          .     
    adc zp_fileblk                                                    ; bce3: 65 39       e9    
    ldx l003a                                                         ; bce5: a6 3a       .:    
    bcc cbcea                                                         ; bce7: 90 01       ..    
    inx                                                               ; bce9: e8          .     
; &bcea referenced 1 time by &bce7
.cbcea
    cmp zp_fwb_exp                                                    ; bcea: c5 3d       .=    
    txa                                                               ; bcec: 8a          .     
    sbc zp_fwb_m1                                                     ; bced: e5 3e       .>    
    bcs cbcd6                                                         ; bcef: b0 e5       ..    
    sec                                                               ; bcf1: 38          8     
    ldy #1                                                            ; bcf2: a0 01       ..    
    lda zp_iwa_1                                                      ; bcf4: a5 2b       .+    
    sta (zp_fwb_exp),y                                                ; bcf6: 91 3d       .=    
    iny                                                               ; bcf8: c8          .     
    lda zp_iwa                                                        ; bcf9: a5 2a       .*    
    sta (zp_fwb_exp),y                                                ; bcfb: 91 3d       .=    
    iny                                                               ; bcfd: c8          .     
    lda zp_fwb_m2                                                     ; bcfe: a5 3f       .?    
    sta (zp_fwb_exp),y                                                ; bd00: 91 3d       .=    
    jsr sub_cbe56                                                     ; bd02: 20 56 be     V.   
    ldy #&ff                                                          ; bd05: a0 ff       ..    
; &bd07 referenced 1 time by &bd0e
.loop_cbd07
    iny                                                               ; bd07: c8          .     
    lda (zp_fwb_sign),y                                               ; bd08: b1 3b       .;    
    sta (zp_fwb_exp),y                                                ; bd0a: 91 3d       .=    
    cmp #&0d                                                          ; bd0c: c9 0d       ..    
    bne loop_cbd07                                                    ; bd0e: d0 f7       ..    
; &bd10 referenced 1 time by &bc9c
.return_38
    rts                                                               ; bd10: 60          `     
; ***************************************************************************************
; RUN
;
; Run the current program from the start. RUN.
.stmt_run
    jsr check_end_of_statement                                        ; bd11: 20 57 98     W.   
; &bd14 referenced 1 time by &bf2d
.cbd14
    jsr sub_cbd20                                                     ; bd14: 20 20 bd      .   
    lda zp_page                                                       ; bd17: a5 18       ..    
    sta l000c                                                         ; bd19: 85 0c       ..    
    stx zp_text_ptr                                                   ; bd1b: 86 0b       ..    
    jmp execute_line                                                  ; bd1d: 4c 0b 8b    L..   
; &bd20 referenced 5 times by &8af3, &90c9, &9290, &bcc9, &bd14
.sub_cbd20
    lda zp_top                                                        ; bd20: a5 12       ..    
    sta zp_lomem                                                      ; bd22: 85 00       ..    
    sta zp_vartop                                                     ; bd24: 85 02       ..    
    lda l0013                                                         ; bd26: a5 13       ..    
    sta l0001                                                         ; bd28: 85 01       ..    
    sta zp_vartop_1                                                   ; bd2a: 85 03       ..    
    jsr sub_cbd3a                                                     ; bd2c: 20 3a bd     :.   
; &bd2f referenced 1 time by &927e
.sub_cbd2f
    ldx #&80                                                          ; bd2f: a2 80       ..    
    lda #0                                                            ; bd31: a9 00       ..    
; &bd33 referenced 1 time by &bd37
.loop_cbd33
    sta l047f,x                                                       ; bd33: 9d 7f 04    ...   
    dex                                                               ; bd36: ca          .     
    bne loop_cbd33                                                    ; bd37: d0 fa       ..    
    rts                                                               ; bd39: 60          `     
; &bd3a referenced 3 times by &8b1a, &b41b, &bd2c
.sub_cbd3a
    lda zp_page                                                       ; bd3a: a5 18       ..    
    sta l001d                                                         ; bd3c: 85 1d       ..    
    lda zp_himem                                                      ; bd3e: a5 06       ..    
    sta zp_stack_ptr                                                  ; bd40: 85 04       ..    
    lda l0007                                                         ; bd42: a5 07       ..    
    sta zp_stack_ptr_1                                                ; bd44: 85 05       ..    
    lda #0                                                            ; bd46: a9 00       ..    
    sta zp_repeat_level                                               ; bd48: 85 24       .$    
    sta zp_for_level                                                  ; bd4a: 85 26       .&    
    sta zp_gosub_level                                                ; bd4c: 85 25       .%    
    sta zp_data_ptr                                                   ; bd4e: 85 1c       ..    
    rts                                                               ; bd50: 60          `     
; ***************************************************************************************
; Push the floating-point accumulator onto the BASIC stack
;
; Reserve five bytes on the BASIC stack and copy the packed floating-point accumulator
; onto it.
; &bd51 referenced 12 times by &9a3e, &9a50, &9c8b, &9cac, &9ce1, &9cff, &9d14, &9d20, &9de9, &9e39, &af27, &bd92
.stack_real
    lda zp_stack_ptr                                                  ; bd51: a5 04       ..    
    sec                                                               ; bd53: 38          8     
    sbc #5                                                            ; bd54: e9 05       ..       ; Lower the stack by 5 bytes (a packed real)
    jsr reserve_stack                                                 ; bd56: 20 2e be     ..   
    ldy #0                                                            ; bd59: a0 00       ..    
    lda zp_fwa_exp                                                    ; bd5b: a5 30       .0    
    sta (zp_stack_ptr),y                                              ; bd5d: 91 04       ..    
    iny                                                               ; bd5f: c8          .     
    lda zp_fwa_sign                                                   ; bd60: a5 2e       ..    
    and #&80                                                          ; bd62: 29 80       ).       ; Pack: fold the sign into the mantissa MSB
    sta zp_fwa_sign                                                   ; bd64: 85 2e       ..    
    lda zp_fwa_m1                                                     ; bd66: a5 31       .1    
    and #&7f                                                          ; bd68: 29 7f       ).    
    ora zp_fwa_sign                                                   ; bd6a: 05 2e       ..    
    sta (zp_stack_ptr),y                                              ; bd6c: 91 04       ..    
    iny                                                               ; bd6e: c8          .     
    lda zp_fwa_m2                                                     ; bd6f: a5 32       .2    
    sta (zp_stack_ptr),y                                              ; bd71: 91 04       ..    
    iny                                                               ; bd73: c8          .     
    lda zp_fwa_m3                                                     ; bd74: a5 33       .3    
    sta (zp_stack_ptr),y                                              ; bd76: 91 04       ..    
    iny                                                               ; bd78: c8          .     
    lda zp_fwa_m4                                                     ; bd79: a5 34       .4    
    sta (zp_stack_ptr),y                                              ; bd7b: 91 04       ..    
    rts                                                               ; bd7d: 60          `     
; &bd7e referenced 11 times by &9a47, &9a5c, &9c9b, &9cf1, &9d05, &9d2c, &9df5, &9e4a, &9e6f, &af2d, &b2e7
.sub_cbd7e
    lda zp_stack_ptr                                                  ; bd7e: a5 04       ..    
    clc                                                               ; bd80: 18          .     
    sta zp_fp_ptr                                                     ; bd81: 85 4b       .K    
    adc #5                                                            ; bd83: 69 05       i.    
    sta zp_stack_ptr                                                  ; bd85: 85 04       ..    
    lda zp_stack_ptr_1                                                ; bd87: a5 05       ..    
    sta zp_fp_ptr_1                                                   ; bd89: 85 4c       .L    
    adc #0                                                            ; bd8b: 69 00       i.    
    sta zp_stack_ptr_1                                                ; bd8d: 85 05       ..    
    rts                                                               ; bd8f: 60          `     
; &bd90 referenced 2 times by &b291, &b31c
.sub_cbd90
    beq stack_string                                                  ; bd90: f0 20       .     
    bmi stack_real                                                    ; bd92: 30 bd       0.    
; ***************************************************************************************
; Push the integer accumulator onto the BASIC stack
;
; Reserve four bytes on the BASIC stack (zp_stack_ptr, &04) and copy the integer
; accumulator (zp_iwa) onto it. Errors if the stack would collide with the heap.
; &bd94 referenced 29 times by &85ac, &8beb, &8bfb, &8ed8, &8f36, &8f71, &90b5, &90e8, &9185, &9334, &9400, &96ff, &9744, &9aa2, &9b6f, &9b7e, &9dce, &9e1d, &ab44, &b0c5, &b298, &b329, &b5b0, &b5c8, &b7cb, &b9f1, &bad0, &bb29, &bb35
.stack_integer
    lda zp_stack_ptr                                                  ; bd94: a5 04       ..    
    sec                                                               ; bd96: 38          8     
    sbc #4                                                            ; bd97: e9 04       ..       ; Lower the stack by 4 bytes (an integer)
    jsr reserve_stack                                                 ; bd99: 20 2e be     ..   
    ldy #3                                                            ; bd9c: a0 03       ..    
    lda zp_iwa_3                                                      ; bd9e: a5 2d       .-    
    sta (zp_stack_ptr),y                                              ; bda0: 91 04       ..    
    dey                                                               ; bda2: 88          .     
    lda zp_iwa_2                                                      ; bda3: a5 2c       .,    
    sta (zp_stack_ptr),y                                              ; bda5: 91 04       ..    
    dey                                                               ; bda7: 88          .     
    lda zp_iwa_1                                                      ; bda8: a5 2b       .+    
    sta (zp_stack_ptr),y                                              ; bdaa: 91 04       ..    
    dey                                                               ; bdac: 88          .     
    lda zp_iwa                                                        ; bdad: a5 2a       .*    
    sta (zp_stack_ptr),y                                              ; bdaf: 91 04       ..    
    rts                                                               ; bdb1: 60          `     
; ***************************************************************************************
; Push the current string onto the BASIC stack
;
; Copy the string from the string buffer (length zp_strbuf_len, &36; text at &0600) onto
; the BASIC stack, length last.
; &bdb2 referenced 9 times by &9ae7, &9c15, &abf7, &aced, &ad06, &afd7, &aff9, &b042, &bd90
.stack_string
    clc                                                               ; bdb2: 18          .     
    lda zp_stack_ptr                                                  ; bdb3: a5 04       ..    
    sbc zp_strbuf_len                                                 ; bdb5: e5 36       .6       ; Lower the stack by length+1 bytes (carry clear)
    jsr reserve_stack                                                 ; bdb7: 20 2e be     ..   
    ldy zp_strbuf_len                                                 ; bdba: a4 36       .6    
    beq cbdc6                                                         ; bdbc: f0 08       ..    
; &bdbe referenced 1 time by &bdc4
.loop_cbdbe
    lda l05ff,y                                                       ; bdbe: b9 ff 05    ...   
    sta (zp_stack_ptr),y                                              ; bdc1: 91 04       ..    
    dey                                                               ; bdc3: 88          .     
    bne loop_cbdbe                                                    ; bdc4: d0 f8       ..    
; &bdc6 referenced 1 time by &bdbc
.cbdc6
    lda zp_strbuf_len                                                 ; bdc6: a5 36       .6    
    sta (zp_stack_ptr),y                                              ; bdc8: 91 04       ..    
    rts                                                               ; bdca: 60          `     
; &bdcb referenced 6 times by &9c37, &ad0f, &afe0, &b002, &b061, &b2fd
.sub_cbdcb
    ldy #0                                                            ; bdcb: a0 00       ..    
    lda (zp_stack_ptr),y                                              ; bdcd: b1 04       ..    
    sta zp_strbuf_len                                                 ; bdcf: 85 36       .6    
    beq cbddc                                                         ; bdd1: f0 09       ..    
    tay                                                               ; bdd3: a8          .     
; &bdd4 referenced 1 time by &bdda
.loop_cbdd4
    lda (zp_stack_ptr),y                                              ; bdd4: b1 04       ..    
    sta l05ff,y                                                       ; bdd6: 99 ff 05    ...   
    dey                                                               ; bdd9: 88          .     
    bne loop_cbdd4                                                    ; bdda: d0 f8       ..    
; &bddc referenced 6 times by &8ceb, &9b16, &ac20, &ad39, &ad52, &bdd1
.cbddc
    ldy #0                                                            ; bddc: a0 00       ..    
    lda (zp_stack_ptr),y                                              ; bdde: b1 04       ..    
    sec                                                               ; bde0: 38          8     
; &bde1 referenced 1 time by &8d28
.cbde1
    adc zp_stack_ptr                                                  ; bde1: 65 04       e.    
    sta zp_stack_ptr                                                  ; bde3: 85 04       ..    
    bcc return_39                                                     ; bde5: 90 23       .#    
    inc zp_stack_ptr_1                                                ; bde7: e6 05       ..    
    rts                                                               ; bde9: 60          `     
; ***************************************************************************************
; Pop an integer from the BASIC stack
;
; Copy the four-byte integer on top of the BASIC stack into the integer accumulator
; (zp_iwa) and drop it.
; &bdea referenced 16 times by &8c1e, &8f11, &8f50, &90b2, &90c0, &9a3b, &9ca9, &9cfc, &9d11, &9d78, &ab56, &b0d0, &b2ca, &b2f0, &b5c5, &b5e9
.unstack_integer
    ldy #3                                                            ; bdea: a0 03       ..    
    lda (zp_stack_ptr),y                                              ; bdec: b1 04       ..    
    sta zp_iwa_3                                                      ; bdee: 85 2d       .-    
    dey                                                               ; bdf0: 88          .     
    lda (zp_stack_ptr),y                                              ; bdf1: b1 04       ..    
    sta zp_iwa_2                                                      ; bdf3: 85 2c       .,    
    dey                                                               ; bdf5: 88          .     
    lda (zp_stack_ptr),y                                              ; bdf6: b1 04       ..    
    sta zp_iwa_1                                                      ; bdf8: 85 2b       .+    
    dey                                                               ; bdfa: 88          .     
    lda (zp_stack_ptr),y                                              ; bdfb: b1 04       ..    
    sta zp_iwa                                                        ; bdfd: 85 2a       .*    
; &bdff referenced 2 times by &9b4e, &9b95
.sub_cbdff
    clc                                                               ; bdff: 18          .     
    lda zp_stack_ptr                                                  ; be00: a5 04       ..    
    adc #4                                                            ; be02: 69 04       i.    
    sta zp_stack_ptr                                                  ; be04: 85 04       ..    
    bcc return_39                                                     ; be06: 90 02       ..    
    inc zp_stack_ptr_1                                                ; be08: e6 05       ..    
; &be0a referenced 3 times by &bde5, &be06, &be29
.return_39
    rts                                                               ; be0a: 60          `     
; &be0b referenced 3 times by &9412, &b21c, &b4b4
.sub_cbe0b
    ldx #&37 ; '7'                                                    ; be0b: a2 37       .7    
; &be0d referenced 5 times by &8fa8, &9233, &970d, &9755, &99dd
.sub_cbe0d
    ldy #3                                                            ; be0d: a0 03       ..    
    lda (zp_stack_ptr),y                                              ; be0f: b1 04       ..    
    sta zp_vartop_1,x                                                 ; be11: 95 03       ..    
    dey                                                               ; be13: 88          .     
    lda (zp_stack_ptr),y                                              ; be14: b1 04       ..    
    sta zp_vartop,x                                                   ; be16: 95 02       ..    
    dey                                                               ; be18: 88          .     
    lda (zp_stack_ptr),y                                              ; be19: b1 04       ..    
    sta l0001,x                                                       ; be1b: 95 01       ..    
    dey                                                               ; be1d: 88          .     
    lda (zp_stack_ptr),y                                              ; be1e: b1 04       ..    
    sta zp_lomem,x                                                    ; be20: 95 00       ..    
    clc                                                               ; be22: 18          .     
    lda zp_stack_ptr                                                  ; be23: a5 04       ..    
    adc #4                                                            ; be25: 69 04       i.    
    sta zp_stack_ptr                                                  ; be27: 85 04       ..    
    bcc return_39                                                     ; be29: 90 df       ..    
    inc zp_stack_ptr_1                                                ; be2b: e6 05       ..    
    rts                                                               ; be2d: 60          `     
; ***************************************************************************************
; Set the stack pointer and check for room
;
; Set the BASIC value-stack pointer to a new top (low byte in A, borrow already taken
; into the high byte) and check it has not run down into the top of variable storage
; (zp_vartop). Raises "No room" on collision; otherwise returns with the stack lowered.
;
; On Entry:
;     A: proposed new stack-pointer low byte
;     CARRY: clear if the subtraction borrowed
; &be2e referenced 4 times by &b19e, &bd56, &bd99, &bdb7
.reserve_stack
    sta zp_stack_ptr                                                  ; be2e: 85 04       ..    
    bcs cbe34                                                         ; be30: b0 02       ..    
    dec zp_stack_ptr_1                                                ; be32: c6 05       ..    
; &be34 referenced 1 time by &be30
.cbe34
    ldy zp_stack_ptr_1                                                ; be34: a4 05       ..    
    cpy zp_vartop_1                                                   ; be36: c4 03       ..       ; Compare the new top against the heap top
    bcc cbe41                                                         ; be38: 90 07       ..    
    bne return_40                                                     ; be3a: d0 04       ..    
    cmp zp_vartop                                                     ; be3c: c5 02       ..    
    bcc cbe41                                                         ; be3e: 90 01       ..    
; &be40 referenced 1 time by &be3a
.return_40
    rts                                                               ; be40: 60          `     
; &be41 referenced 2 times by &be38, &be3e
.cbe41
    jmp err_no_room                                                   ; be41: 4c b7 8c    L..      ; Stack meets heap: No room
; ***************************************************************************************
; Store the accumulator into a zero-page integer variable
;
; Copy IWA into a 4-byte zero-page integer variable.
; &be44 referenced 5 times by &885f, &9d75, &af41, &b2e0, &b315
.iwa_store_zp
    lda zp_iwa                                                        ; be44: a5 2a       .*    
    sta zp_lomem,x                                                    ; be46: 95 00       ..    
    lda zp_iwa_1                                                      ; be48: a5 2b       .+    
    sta l0001,x                                                       ; be4a: 95 01       ..    
    lda zp_iwa_2                                                      ; be4c: a5 2c       .,    
    sta zp_vartop,x                                                   ; be4e: 95 02       ..    
    lda zp_iwa_3                                                      ; be50: a5 2d       .-    
    sta zp_vartop_1,x                                                 ; be52: 95 03       ..    
    rts                                                               ; be54: 60          `     
; &be55 referenced 1 time by &bb04
.sub_cbe55
    clc                                                               ; be55: 18          .     
; &be56 referenced 1 time by &bd02
.sub_cbe56
    tya                                                               ; be56: 98          .     
    adc zp_fwb_exp                                                    ; be57: 65 3d       e=    
    sta zp_fwb_exp                                                    ; be59: 85 3d       .=    
    bcc cbe5f                                                         ; be5b: 90 02       ..    
    inc zp_fwb_m1                                                     ; be5d: e6 3e       .>    
; &be5f referenced 1 time by &be5b
.cbe5f
    ldy #1                                                            ; be5f: a0 01       ..    
    rts                                                               ; be61: 60          `     
; &be62 referenced 2 times by &bf24, &bf2a
.sub_cbe62
    jsr sub_cbedd                                                     ; be62: 20 dd be     ..   
    tay                                                               ; be65: a8          .     
    lda #osfile_load                                                  ; be66: a9 ff       ..    
    sty zp_fwb_exp                                                    ; be68: 84 3d       .=    
    ldx #&37 ; '7'                                                    ; be6a: a2 37       .7    
    jsr osfile                                                        ; be6c: 20 dd ff     ..      ; osfile: load file
; &be6f referenced 6 times by &8ac3, &8acb, &8fab, &b5e6, &bcc6, &bef3
.sub_cbe6f
    lda zp_page                                                       ; be6f: a5 18       ..    
    sta l0013                                                         ; be71: 85 13       ..    
    ldy #0                                                            ; be73: a0 00       ..    
    sty zp_top                                                        ; be75: 84 12       ..    
    iny                                                               ; be77: c8          .     
; &be78 referenced 1 time by &be8e
.loop_cbe78
    dey                                                               ; be78: 88          .     
    lda (zp_top),y                                                    ; be79: b1 12       ..    
    cmp #&0d                                                          ; be7b: c9 0d       ..    
    bne cbe9e                                                         ; be7d: d0 1f       ..    
    iny                                                               ; be7f: c8          .     
    lda (zp_top),y                                                    ; be80: b1 12       ..    
    bmi cbe90                                                         ; be82: 30 0c       0.    
    ldy #3                                                            ; be84: a0 03       ..    
    lda (zp_top),y                                                    ; be86: b1 12       ..    
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
    adc zp_top                                                        ; be93: 65 12       e.    
    sta zp_top                                                        ; be95: 85 12       ..    
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
    equb &0d, &ea, &4c, &f6, &8a                                      ; bead: 0d ea 4c... ..L...
; &beb2 referenced 1 time by &bed7
.sub_cbeb2
    lda #0                                                            ; beb2: a9 00       ..    
    sta zp_general                                                    ; beb4: 85 37       .7    
    lda #6                                                            ; beb6: a9 06       ..    
    sta l0038                                                         ; beb8: 85 38       .8    
; &beba referenced 2 times by &8ca2, &bf88
.sub_cbeba
    ldy zp_strbuf_len                                                 ; beba: a4 36       .6    
    lda #&0d                                                          ; bebc: a9 0d       ..    
    sta string_work,y                                                 ; bebe: 99 00 06    ...   
    rts                                                               ; bec1: 60          `     
; ***************************************************************************************
; OSCLI
;
; Pass a string to the OS command-line interpreter. OSCLI string.
.stmt_oscli
    jsr sub_cbed2                                                     ; bec2: 20 d2 be     ..   
    ldx #0                                                            ; bec5: a2 00       ..    
    ldy #6                                                            ; bec7: a0 06       ..    
    jsr oscli                                                         ; bec9: 20 f7 ff     ..   
    jmp statement_loop                                                ; becc: 4c 9b 8b    L..   
; &becf referenced 1 time by &bed5
.loop_cbecf
    jmp c8c0e                                                         ; becf: 4c 0e 8c    L..   
; &bed2 referenced 2 times by &bec2, &bedd
.sub_cbed2
    jsr eval_expr                                                     ; bed2: 20 1d 9b     ..   
    bne loop_cbecf                                                    ; bed5: d0 f8       ..    
    jsr sub_cbeb2                                                     ; bed7: 20 b2 be     ..   
    jmp c984c                                                         ; beda: 4c 4c 98    LL.   
; &bedd referenced 2 times by &be62, &bf0a
.sub_cbedd
    jsr sub_cbed2                                                     ; bedd: 20 d2 be     ..   
    dey                                                               ; bee0: 88          .     
    sty zp_fileblk                                                    ; bee1: 84 39       .9    
    lda zp_page                                                       ; bee3: a5 18       ..    
    sta l003a                                                         ; bee5: 85 3a       .:    
; &bee7 referenced 1 time by &93a3
.sub_cbee7
    lda #osbyte_read_high_order_address                               ; bee7: a9 82       ..    
    jsr osbyte                                                        ; bee9: 20 f4 ff     ..      ; Read high-order address (machine high word)
    stx zp_fwb_sign                                                   ; beec: 86 3b       .;    
    sty zp_fwb_ovf                                                    ; beee: 84 3c       .<    
    lda #0                                                            ; bef0: a9 00       ..    
    rts                                                               ; bef2: 60          `     
; ***************************************************************************************
; SAVE
;
; Save the current program to the filing system. SAVE string.
.stmt_save
    jsr sub_cbe6f                                                     ; bef3: 20 6f be     o.   
    lda zp_top                                                        ; bef6: a5 12       ..    
    sta l0045                                                         ; bef8: 85 45       .E    
    lda l0013                                                         ; befa: a5 13       ..    
    sta l0046                                                         ; befc: 85 46       .F    
    lda #&23 ; '#'                                                    ; befe: a9 23       .#    
    sta zp_fwb_exp                                                    ; bf00: 85 3d       .=    
    lda #&80                                                          ; bf02: a9 80       ..    
    sta zp_fwb_m1                                                     ; bf04: 85 3e       .>    
    lda zp_page                                                       ; bf06: a5 18       ..    
    sta zp_fwb_rnd                                                    ; bf08: 85 42       .B    
    jsr sub_cbedd                                                     ; bf0a: 20 dd be     ..   
    stx zp_fwb_m2                                                     ; bf0d: 86 3f       .?    
    sty zp_fwb_m3                                                     ; bf0f: 84 40       .@    
    stx zp_fp_temp                                                    ; bf11: 86 43       .C    
    sty l0044                                                         ; bf13: 84 44       .D    
    stx l0047                                                         ; bf15: 86 47       .G    
    sty l0048                                                         ; bf17: 84 48       .H    
    sta zp_fwb_m4                                                     ; bf19: 85 41       .A    
    tay                                                               ; bf1b: a8          .     
    ldx #&37 ; '7'                                                    ; bf1c: a2 37       .7    
    jsr osfile                                                        ; bf1e: 20 dd ff     ..   
    jmp statement_loop                                                ; bf21: 4c 9b 8b    L..   
; ***************************************************************************************
; LOAD
;
; Load a BASIC program without running it. LOAD string.
.stmt_load
    jsr sub_cbe62                                                     ; bf24: 20 62 be     b.   
    jmp c8af3                                                         ; bf27: 4c f3 8a    L..   
; ***************************************************************************************
; CHAIN
;
; Load a BASIC program and run it. CHAIN string.
.stmt_chain
    jsr sub_cbe62                                                     ; bf2a: 20 62 be     b.   
    jmp cbd14                                                         ; bf2d: 4c 14 bd    L..   
; ***************************************************************************************
; PTR#=
;
; Set the sequential pointer of an open file. PTR#channel = position.
.stmt_ptr
    jsr sub_cbfa9                                                     ; bf30: 20 a9 bf     ..   
    pha                                                               ; bf33: 48          H     
    jsr c9813                                                         ; bf34: 20 13 98     ..   
    jsr sub_c92ee                                                     ; bf37: 20 ee 92     ..   
    pla                                                               ; bf3a: 68          h     
    tay                                                               ; bf3b: a8          .     
    ldx #&2a ; '*'                                                    ; bf3c: a2 2a       .*    
    lda #1                                                            ; bf3e: a9 01       ..    
    jsr osargs                                                        ; bf40: 20 da ff     ..      ; Write sequential file pointer from zero page address X (A=1)
    jmp statement_loop                                                ; bf43: 4c 9b 8b    L..   
; ***************************************************************************************
; EXT
;
; Length (extent) of an open file. EXT#channel.
.fn_ext
    sec                                                               ; bf46: 38          8     
; ***************************************************************************************
; =PTR
;
; Read the sequential pointer of an open file. PTR#channel.
.fn_ptr
    lda #0                                                            ; bf47: a9 00       ..    
    rol a                                                             ; bf49: 2a          *     
    rol a                                                             ; bf4a: 2a          *     
    pha                                                               ; bf4b: 48          H     
    jsr sub_cbfb5                                                     ; bf4c: 20 b5 bf     ..   
    ldx #&2a ; '*'                                                    ; bf4f: a2 2a       .*    
    pla                                                               ; bf51: 68          h     
    jsr osargs                                                        ; bf52: 20 da ff     ..   
    lda #&40 ; '@'                                                    ; bf55: a9 40       .@    
    rts                                                               ; bf57: 60          `     
; ***************************************************************************************
; BPUT
;
; Write a byte to an open file. BPUT#channel, value.
.stmt_bput
    jsr sub_cbfa9                                                     ; bf58: 20 a9 bf     ..   
    pha                                                               ; bf5b: 48          H     
    jsr skip_spaces_expect_comma                                      ; bf5c: 20 ae 8a     ..   
    jsr c9849                                                         ; bf5f: 20 49 98     I.   
    jsr sub_c92ee                                                     ; bf62: 20 ee 92     ..   
    pla                                                               ; bf65: 68          h     
    tay                                                               ; bf66: a8          .     
    lda zp_iwa                                                        ; bf67: a5 2a       .*    
    jsr osbput                                                        ; bf69: 20 d4 ff     ..   
    jmp statement_loop                                                ; bf6c: 4c 9b 8b    L..   
; ***************************************************************************************
; BGET
;
; Read a byte from an open file. BGET#channel.
.fn_bget
    jsr sub_cbfb5                                                     ; bf6f: 20 b5 bf     ..   
    jsr osbget                                                        ; bf72: 20 d7 ff     ..   
    jmp caed8                                                         ; bf75: 4c d8 ae    L..   
; ***************************************************************************************
; OPENIN
;
; Open a file for input, returning its channel (0 if not found). OPENIN string.
.fn_openin
    lda #&40 ; '@'                                                    ; bf78: a9 40       .@    
    bne cbf82                                                         ; bf7a: d0 06       ..    
; ***************************************************************************************
; OPENOUT
;
; Create a file for output, returning its channel. OPENOUT string.
.fn_openout
    lda #&80                                                          ; bf7c: a9 80       ..    
    bne cbf82                                                         ; bf7e: d0 02       ..    
; ***************************************************************************************
; OPENUP
;
; Open a file for update (read and write), returning its channel. OPENUP string.
.fn_openup
    lda #&c0                                                          ; bf80: a9 c0       ..    
; &bf82 referenced 2 times by &bf7a, &bf7e
.cbf82
    pha                                                               ; bf82: 48          H     
    jsr eval_factor                                                   ; bf83: 20 ec ad     ..   
    bne cbf96                                                         ; bf86: d0 0e       ..    
    jsr sub_cbeba                                                     ; bf88: 20 ba be     ..   
    ldx #0                                                            ; bf8b: a2 00       ..    
    ldy #6                                                            ; bf8d: a0 06       ..    
    pla                                                               ; bf8f: 68          h     
    jsr osfind                                                        ; bf90: 20 ce ff     ..   
    jmp caed8                                                         ; bf93: 4c d8 ae    L..   
; &bf96 referenced 1 time by &bf86
.cbf96
    jmp c8c0e                                                         ; bf96: 4c 0e 8c    L..   
; ***************************************************************************************
; CLOSE
;
; Close an open file, or all files with #0. CLOSE#channel.
.stmt_close
    jsr sub_cbfa9                                                     ; bf99: 20 a9 bf     ..   
    jsr sub_c9852                                                     ; bf9c: 20 52 98     R.   
    ldy zp_iwa                                                        ; bf9f: a4 2a       .*    
    lda #osfind_close                                                 ; bfa1: a9 00       ..    
    jsr osfind                                                        ; bfa3: 20 ce ff     ..      ; osfind: close one or all files
    jmp statement_loop                                                ; bfa6: 4c 9b 8b    L..   
; &bfa9 referenced 5 times by &8d2d, &b9d1, &bf30, &bf58, &bf99
.sub_cbfa9
    lda zp_text_ptr_off                                               ; bfa9: a5 0a       ..    
    sta zp_text_ptr2_off                                              ; bfab: 85 1b       ..    
    lda zp_text_ptr                                                   ; bfad: a5 0b       ..    
    sta zp_text_ptr2                                                  ; bfaf: 85 19       ..    
    lda l000c                                                         ; bfb1: a5 0c       ..    
    sta l001a                                                         ; bfb3: 85 1a       ..    
; &bfb5 referenced 3 times by &acb8, &bf4c, &bf6f
.sub_cbfb5
    jsr skip_spaces_ptr2                                              ; bfb5: 20 8c 8a     ..   
    cmp #&23 ; '#'                                                    ; bfb8: c9 23       .#    
    bne cbfc3                                                         ; bfba: d0 07       ..    
    jsr sub_c92e3                                                     ; bfbc: 20 e3 92     ..   
    ldy zp_iwa                                                        ; bfbf: a4 2a       .*    
    tya                                                               ; bfc1: 98          .     
    rts                                                               ; bfc2: 60          `     
; &bfc3 referenced 1 time by &bfba
.cbfc3
    brk                                                               ; bfc3: 00          .     
    equs "-Missing #"                                                 ; bfc4: 2d 4d 69... -Mi...
    equb &00                                                          ; bfce: 00          .     
; &bfcf referenced 2 times by &9080, &be9e
.sub_cbfcf
    pla                                                               ; bfcf: 68          h     
    sta zp_general                                                    ; bfd0: 85 37       .7    
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
    jmp (zp_general)                                                  ; bfe1: 6c 37 00    l7.   
; ***************************************************************************************
; REPORT
;
; Print the message for the last error. REPORT.
.stmt_report
    jsr check_end_of_statement                                        ; bfe4: 20 57 98     W.   
    jsr sub_cbc25                                                     ; bfe7: 20 25 bc     %.   
    ldy #1                                                            ; bfea: a0 01       ..    
; &bfec referenced 1 time by &bff4
.loop_cbfec
    lda (l00fd),y                                                     ; bfec: b1 fd       ..    
    beq cbff6                                                         ; bfee: f0 06       ..    
    jsr sub_cb50e                                                     ; bff0: 20 0e b5     ..   
    iny                                                               ; bff3: c8          .     
    bne loop_cbfec                                                    ; bff4: d0 f6       ..    
; &bff6 referenced 1 time by &bfee
.cbff6
    jmp statement_loop                                                ; bff6: 4c 9b 8b    L..   
    equb &00                                                          ; bff9: 00          .     
    equs "Roger"                                                      ; bffa: 52 6f 67... Rog...
    equb &00                                                          ; bfff: 00          .     
.pydis_end

save pydis_start, pydis_end

; Label references by decreasing frequency:
;     zp_iwa:                    187
;     zp_general:                142
;     zp_iwa_1:                  111
;     zp_text_ptr_off:            92
;     zp_text_ptr2_off:           90
;     zp_stack_ptr:               85
;     zp_text_ptr:                75
;     zp_fwa_m1:                  72
;     zp_iwa_2:                   70
;     l0038:                      66
;     zp_fwb_exp:                 65
;     zp_fileblk:                 62
;     zp_fwa_m2:                  61
;     zp_fwa_m4:                  61
;     zp_iwa_3:                   61
;     zp_fwb_sign:                59
;     zp_fwa_m3:                  58
;     zp_fwa_exp:                 55
;     zp_fwb_m1:                  55
;     zp_fwb_m2:                  55
;     zp_strbuf_len:              52
;     skip_spaces:                48
;     zp_fwa_sign:                48
;     zp_text_ptr2:               48
;     l003a:                      45
;     zp_fwa_rnd:                 42
;     l000c:                      41
;     zp_var_type:                41
;     zp_fwb_ovf:                 39
;     zp_fwb_m3:                  37
;     zp_fp_ptr:                  31
;     stack_integer:              29
;     l004d:                      28
;     zp_vartop:                  28
;     string_work:                27
;     check_end_of_statement:     25
;     zp_fwb_m4:                  25
;     statement_loop:             23
;     eval_expr_to_integer:       22
;     l001a:                      22
;     coerce_to_integer:          21
;     l0049:                      21
;     skip_spaces_ptr2:           21
;     zp_stack_ptr_1:             21
;     zp_top:                     21
;     l004a:                      20
;     zp_fwa_ovf:                 20
;     zp_vartop_1:                20
;     l004e:                      19
;     c8c0e:                      18
;     caed8:                      18
;     fwa_sign:                   17
;     zp_fwb_rnd:                 17
;     sub_c9b29:                  16
;     unstack_integer:            16
;     zp_page:                    16
;     l0013:                      15
;     zp_for_level:               15
;     zp_fp_ptr_1:                14
;     cb558:                      13
;     eval_factor:                13
;     fwa_mul_var:                12
;     int_to_fwa:                 12
;     oswrch:                     12
;     stack_real:                 12
;     ca066:                      11
;     cae56:                      11
;     eval_expr:                  11
;     iwa_from_ya:                11
;     osbyte:                     11
;     sub_c92fa:                  11
;     sub_cbd7e:                  11
;     zp_opt_flag:                11
;     c8ba3:                      10
;     fwa_add_var:                10
;     fwa_unpack_var:             10
;     sub_c92e3:                  10
;     sub_c97df:                  10
;     cb565:                       9
;     fwa_pack_temp1:              9
;     l0048:                       9
;     stack_string:                9
;     sub_c9582:                   9
;     zp_print_flag:               9
;     c870d:                       8
;     c9127:                       8
;     c986d:                       8
;     ca099:                       8
;     fwa_clear:                   8
;     fwa_normalise:               8
;     inc_ptr_general:             8
;     l0007:                       8
;     l05ff:                       8
;     sub_c92dd:                   8
;     sub_c9852:                   8
;     sub_cbc25:                   8
;     zp_himem:                    8
;     zp_print_bytes:              8
;     c862b:                       7
;     c8b96:                       7
;     c982a:                       7
;     c9bb5:                       7
;     fwa_pack_var:                7
;     fwb_unpack_var:              7
;     sub_c882c:                   7
;     sub_c92fd:                   7
;     zp_count:                    7
;     c8af3:                       6
;     c9bb4:                       6
;     c9c88:                       6
;     cae43:                       6
;     cb2b5:                       6
;     cbddc:                       6
;     fwa_pack_temp3:              6
;     fwa_set_one:                 6
;     immediate_loop:              6
;     l0001:                       6
;     l0017:                       6
;     osbget:                      6
;     osbput:                      6
;     sub_c92ee:                   6
;     sub_ca7f5:                   6
;     sub_cb4b4:                   6
;     sub_cbdcb:                   6
;     sub_cbe6f:                   6
;     zp_error_vec:                6
;     zp_fp_temp:                  6
;     zp_lomem:                    6
;     c8735:                       5
;     c8957:                       5
;     c8961:                       5
;     c8e6a:                       5
;     c9a93:                       5
;     c9fe6:                       5
;     ca208:                       5
;     cac9b:                       5
;     cb741:                       5
;     cb97d:                       5
;     fp_mantissas_sub:            5
;     fwa_negate:                  5
;     fwa_to_int:                  5
;     fwb_copy_from_fwa:           5
;     iwa_store_zp:                5
;     l0044:                       5
;     osword:                      5
;     resint_at:                   5
;     return_22:                   5
;     skip_spaces_expect_comma:    5
;     sub_c8926:                   5
;     sub_c9a9d:                   5
;     sub_ca242:                   5
;     sub_cbd20:                   5
;     sub_cbe0d:                   5
;     sub_cbfa9:                   5
;     zp_gosub_level:              5
;     zp_repeat_level:             5
;     zp_trace_flag:               5
;     c8604:                       4
;     c88d5:                       4
;     c8aa2:                       4
;     c8b98:                       4
;     c8d30:                       4
;     c9372:                       4
;     c9479:                       4
;     c94b3:                       4
;     c9641:                       4
;     c9813:                       4
;     c984c:                       4
;     c9877:                       4
;     c9c45:                       4
;     ca46c:                       4
;     cb036:                       4
;     cb751:                       4
;     cba5a:                       4
;     cbc28:                       4
;     find_variable:               4
;     fwa_rdiv_var:                4
;     fwa_to_int2:                 4
;     iwa_abs:                     4
;     l000f:                       4
;     l0011:                       4
;     l001d:                       4
;     l0045:                       4
;     l0046:                       4
;     l0441:                       4
;     read_via_ptr_general:        4
;     reserve_stack:               4
;     resint_p:                    4
;     return_23:                   4
;     sub_c9222:                   4
;     sub_c92da:                   4
;     sub_c92eb:                   4
;     sub_c9456:                   4
;     sub_c9531:                   4
;     sub_c9c42:                   4
;     sub_c9e20:                   4
;     sub_ca7e9:                   4
;     sub_ca897:                   4
;     sub_cb99a:                   4
;     zp_asm_opcode:               4
;     zp_data_ptr:                 4
;     zp_rnd_seed:                 4
;     c8620:                       3
;     c8738:                       3
;     c8858:                       3
;     c8924:                       3
;     c8936:                       3
;     c89b5:                       3
;     c8d7d:                       3
;     c8d80:                       3
;     c8dbb:                       3
;     c8dc3:                       3
;     c8e0e:                       3
;     c8f2e:                       3
;     c91fc:                       3
;     c9218:                       3
;     c92f7:                       3
;     c9453:                       3
;     c961b:                       3
;     c9960:                       3
;     c99a4:                       3
;     c9d0e:                       3
;     c9d1d:                       3
;     c9dd4:                       3
;     c9ed1:                       3
;     ca0e8:                       3
;     ca387:                       3
;     ca590:                       3
;     ca6e7:                       3
;     ca724:                       3
;     ca76c:                       3
;     ca7f7:                       3
;     ca99e:                       3
;     caad1:                       3
;     caea2:                       3
;     cb033:                       3
;     cb32c:                       3
;     cb8d2:                       3
;     cbb07:                       3
;     cbb7a:                       3
;     err_no_room:                 3
;     fn_true:                     3
;     fwa_add_fwb:                 3
;     fwa_div10:                   3
;     fwb_clear:                   3
;     iwa_negate:                  3
;     l0009:                       3
;     l000e:                       3
;     l00fd:                       3
;     l0401:                       3
;     return_12:                   3
;     return_19:                   3
;     return_25:                   3
;     return_33:                   3
;     return_36:                   3
;     return_39:                   3
;     return_8:                    3
;     sub_c8827:                   3
;     sub_c882f:                   3
;     sub_c8832:                   3
;     sub_c894b:                   3
;     sub_c8c1e:                   3
;     sub_c909f:                   3
;     sub_c94fc:                   3
;     sub_c97ba:                   3
;     sub_c9970:                   3
;     sub_c9dd1:                   3
;     sub_ca07b:                   3
;     sub_ca7ed:                   3
;     sub_ca9d3:                   3
;     sub_cab12:                   3
;     sub_cb50e:                   3
;     sub_cb577:                   3
;     sub_cbd3a:                   3
;     sub_cbe0b:                   3
;     sub_cbfb5:                   3
;     zp_erl:                      3
;     zp_listo:                    3
;     zp_width:                    3
;     c8556:                       2
;     c8650:                       2
;     c866f:                       2
;     c8691:                       2
;     c86a6:                       2
;     c86a8:                       2
;     c86c5:                       2
;     c86c8:                       2
;     c879a:                       2
;     c87ed:                       2
;     c8810:                       2
;     c889d:                       2
;     c88da:                       2
;     c896a:                       2
;     c89c2:                       2
;     c89d0:                       2
;     c89d2:                       2
;     c89e3:                       2
;     c8a0d:                       2
;     c8a19:                       2
;     c8a37:                       2
;     c8a54:                       2
;     c8b59:                       2
;     c8b87:                       2
;     c8c43:                       2
;     c8c5f:                       2
;     c8c84:                       2
;     c8d26:                       2
;     c8e5f:                       2
;     c8e98:                       2
;     c8ea4:                       2
;     c8fdf:                       2
;     c901a:                       2
;     c901c:                       2
;     c903a:                       2
;     c9043:                       2
;     c9071:                       2
;     c90b5:                       2
;     c916b:                       2
;     c928a:                       2
;     c9365:                       2
;     c93d7:                       2
;     c93da:                       2
;     c946f:                       2
;     c9501:                       2
;     c9556:                       2
;     c955b:                       2
;     c956d:                       2
;     c957f:                       2
;     c95ff:                       2
;     c9677:                       2
;     c96d7:                       2
;     c97d1:                       2
;     c9838:                       2
;     c9849:                       2
;     c9859:                       2
;     c98bc:                       2
;     c98e3:                       2
;     c9978:                       2
;     c99a7:                       2
;     c9a9a:                       2
;     c9c03:                       2
;     c9c9b:                       2
;     c9ca1:                       2
;     c9d39:                       2
;     c9e23:                       2
;     c9eb7:                       2
;     c9ef9:                       2
;     c9efb:                       2
;     c9f39:                       2
;     c9f5c:                       2
;     ca072:                       2
;     ca111:                       2
;     ca118:                       2
;     ca170:                       2
;     ca174:                       2
;     ca197:                       2
;     ca313:                       2
;     ca336:                       2
;     ca40c:                       2
;     ca43c:                       2
;     ca450:                       2
;     ca659:                       2
;     ca67c:                       2
;     ca6bb:                       2
;     ca8ea:                       2
;     ca8fe:                       2
;     ca904:                       2
;     ca91b:                       2
;     ca936:                       2
;     ca9aa:                       2
;     ca9c3:                       2
;     caa4e:                       2
;     caab8:                       2
;     cab9d:                       2
;     caba0:                       2
;     cabb8:                       2
;     cabe6:                       2
;     cac73:                       2
;     cac95:                       2
;     cad3c:                       2
;     cad52:                       2
;     cad67:                       2
;     cad89:                       2
;     cadc9:                       2
;     cafc2:                       2
;     cb02e:                       2
;     cb0bf:                       2
;     cb0f5:                       2
;     cb11a:                       2
;     cb12d:                       2
;     cb24d:                       2
;     cb2ca:                       2
;     cb329:                       2
;     cb354:                       2
;     cb48f:                       2
;     cb4ae:                       2
;     cb4e9:                       2
;     cb51e:                       2
;     cb5d8:                       2
;     cb639:                       2
;     cb678:                       2
;     cb688:                       2
;     cb68e:                       2
;     cb6be:                       2
;     cb6d7:                       2
;     cb7a4:                       2
;     cb944:                       2
;     cb9af:                       2
;     cb9c4:                       2
;     cb9da:                       2
;     cbb15:                       2
;     cbc55:                       2
;     cbcd6:                       2
;     cbe41:                       2
;     cbe9e:                       2
;     cbf82:                       2
;     dispatch_token:              2
;     err_too_big:                 2
;     fp_temp1:                    2
;     fwa_add_fwb_raw:             2
;     fwa_copy_from_fwb:           2
;     fwa_mul10:                   2
;     fwa_mul_var_raw:             2
;     fwa_pack_temp2:              2
;     fwa_reciprocal:              2
;     fwa_round:                   2
;     fwa_rsub_var:                2
;     fwa_unpack_temp1:            2
;     iwa_load_zp:                 2
;     l0010:                       2
;     l0022:                       2
;     l0100:                       2
;     l01ff:                       2
;     l0402:                       2
;     l0403:                       2
;     l043d:                       2
;     l04f1:                       2
;     l04f2:                       2
;     l04f3:                       2
;     l04f5:                       2
;     l04f7:                       2
;     l04fc:                       2
;     l06ff:                       2
;     number_to_ascii:             2
;     osargs:                      2
;     oscli:                       2
;     osfile:                      2
;     osfind:                      2
;     osrdch:                      2
;     resint_o:                    2
;     return_1:                    2
;     return_10:                   2
;     return_13:                   2
;     return_2:                    2
;     return_21:                   2
;     return_26:                   2
;     return_28:                   2
;     return_3:                    2
;     return_31:                   2
;     return_35:                   2
;     return_9:                    2
;     rnd_fraction:                2
;     stmt_data:                   2
;     sub_c887c:                   2
;     sub_c8c21:                   2
;     sub_c8e70:                   2
;     sub_c8e8a:                   2
;     sub_c8f1e:                   2
;     sub_c8f69:                   2
;     sub_c8f92:                   2
;     sub_c9236:                   2
;     sub_c95c9:                   2
;     sub_c95dd:                   2
;     sub_c96df:                   2
;     sub_c97eb:                   2
;     sub_c9841:                   2
;     sub_c9890:                   2
;     sub_c9905:                   2
;     sub_c991f:                   2
;     sub_c9923:                   2
;     sub_c99be:                   2
;     sub_c9b6b:                   2
;     sub_c9b9c:                   2
;     sub_c9dce:                   2
;     sub_c9e1d:                   2
;     sub_ca064:                   2
;     sub_ca178:                   2
;     sub_ca23f:                   2
;     sub_ca486:                   2
;     sub_ca4d0:                   2
;     sub_ca7f1:                   2
;     sub_caa48:                   2
;     sub_caa4c:                   2
;     sub_caa55:                   2
;     sub_cadad:                   2
;     sub_caf87:                   2
;     sub_cafad:                   2
;     sub_cb30d:                   2
;     sub_cb4b1:                   2
;     sub_cb545:                   2
;     sub_cb562:                   2
;     sub_cbb50:                   2
;     sub_cbc02:                   2
;     sub_cbc2d:                   2
;     sub_cbc81:                   2
;     sub_cbc8d:                   2
;     sub_cbd90:                   2
;     sub_cbdff:                   2
;     sub_cbe62:                   2
;     sub_cbe92:                   2
;     sub_cbeba:                   2
;     sub_cbed2:                   2
;     sub_cbedd:                   2
;     sub_cbfcf:                   2
;     try_variable_assignment:     2
;     wrchv:                       2
;     zp_trace_max:                2
;     ascii_to_number:             1
;     assembler_exit:              1
;     brkv:                        1
;     brkv+1:                      1
;     c8063:                       1
;     c8504:                       1
;     c8508:                       1
;     c8536:                       1
;     c854c:                       1
;     c8565:                       1
;     c8577:                       1
;     c857b:                       1
;     c857e:                       1
;     c858c:                       1
;     c859f:                       1
;     c85a2:                       1
;     c85f1:                       1
;     c8601:                       1
;     c8607:                       1
;     c8643:                       1
;     c865b:                       1
;     c8665:                       1
;     c8673:                       1
;     c86a5:                       1
;     c86ad:                       1
;     c86b2:                       1
;     c86b7:                       1
;     c86cc:                       1
;     c86d3:                       1
;     c86da:                       1
;     c86fb:                       1
;     c8715:                       1
;     c873f:                       1
;     c8750:                       1
;     c8767:                       1
;     c876e:                       1
;     c8780:                       1
;     c8782:                       1
;     c8788:                       1
;     c8797:                       1
;     c879c:                       1
;     c879f:                       1
;     c87b2:                       1
;     c87cc:                       1
;     c87de:                       1
;     c87f0:                       1
;     c8813:                       1
;     c883a:                       1
;     c886a:                       1
;     c8966:                       1
;     c897c:                       1
;     c898c:                       1
;     c8996:                       1
;     c89a3:                       1
;     c89df:                       1
;     c89e9:                       1
;     c89ec:                       1
;     c89f8:                       1
;     c8a18:                       1
;     c8a25:                       1
;     c8a30:                       1
;     c8a48:                       1
;     c8a66:                       1
;     c8a6d:                       1
;     c8a72:                       1
;     c8a7f:                       1
;     c8a81:                       1
;     c8a86:                       1
;     c8b38:                       1
;     c8bdf:                       1
;     c8be9:                       1
;     c8bfb:                       1
;     c8c0b:                       1
;     c8ca2:                       1
;     c8cb4:                       1
;     c8ce5:                       1
;     c8cee:                       1
;     c8cff:                       1
;     c8d03:                       1
;     c8d57:                       1
;     c8d64:                       1
;     c8d77:                       1
;     c8dd2:                       1
;     c8e5b:                       1
;     c8ea7:                       1
;     c8ecc:                       1
;     c8ee0:                       1
;     c8f0c:                       1
;     c8f1b:                       1
;     c8f8d:                       1
;     c8fd6:                       1
;     c8fe7:                       1
;     c900d:                       1
;     c903d:                       1
;     c9080:                       1
;     c90df:                       1
;     c913c:                       1
;     c915e:                       1
;     c9168:                       1
;     c91b7:                       1
;     c91d2:                       1
;     c9203:                       1
;     c920b:                       1
;     c9215:                       1
;     c924b:                       1
;     c925a:                       1
;     c92a5:                       1
;     c92b7:                       1
;     c92c0:                       1
;     c92f4:                       1
;     c9341:                       1
;     c9353:                       1
;     c936b:                       1
;     c93ea:                       1
;     c93fd:                       1
;     c949a:                       1
;     c94a7:                       1
;     c94d4:                       1
;     c94e1:                       1
;     c9516:                       1
;     c9541:                       1
;     c954d:                       1
;     c9571:                       1
;     c957a:                       1
;     c95a5:                       1
;     c95a7:                       1
;     c95b0:                       1
;     c95bf:                       1
;     c960e:                       1
;     c9615:                       1
;     c962d:                       1
;     c9635:                       1
;     c9654:                       1
;     c9661:                       1
;     c9665:                       1
;     c9673:                       1
;     c967b:                       1
;     c967f:                       1
;     c9681:                       1
;     c969f:                       1
;     c96a6:                       1
;     c96af:                       1
;     c96c9:                       1
;     c976c:                       1
;     c977d:                       1
;     c979b:                       1
;     c97a3:                       1
;     c97ad:                       1
;     c9805:                       1
;     c9861:                       1
;     c98ac:                       1
;     c98b7:                       1
;     c98cc:                       1
;     c98e1:                       1
;     c98f1:                       1
;     c9902:                       1
;     c9925:                       1
;     c9943:                       1
;     c994f:                       1
;     c998e:                       1
;     c9a33:                       1
;     c9a35:                       1
;     c9a62:                       1
;     c9ae5:                       1
;     c9ae7:                       1
;     c9aff:                       1
;     c9b11:                       1
;     c9b15:                       1
;     c9b3a:                       1
;     c9b55:                       1
;     c9b7a:                       1
;     c9ba8:                       1
;     c9bc0:                       1
;     c9bd4:                       1
;     c9bdf:                       1
;     c9be8:                       1
;     c9bfa:                       1
;     c9c4e:                       1
;     c9c77:                       1
;     c9c8b:                       1
;     c9ca7:                       1
;     c9cb5:                       1
;     c9ce1:                       1
;     c9cf1:                       1
;     c9cfa:                       1
;     c9d2c:                       1
;     c9d3c:                       1
;     c9d4e:                       1
;     c9d69:                       1
;     c9da6:                       1
;     c9dbb:                       1
;     c9dbd:                       1
;     c9dc6:                       1
;     c9de5:                       1
;     c9e35:                       1
;     c9e59:                       1
;     c9e88:                       1
;     c9e96:                       1
;     c9ebf:                       1
;     c9ee8:                       1
;     c9ef5:                       1
;     c9f0f:                       1
;     c9f1d:                       1
;     c9f25:                       1
;     c9f31:                       1
;     c9f34:                       1
;     c9f71:                       1
;     c9f92:                       1
;     c9f9c:                       1
;     c9fa0:                       1
;     c9fad:                       1
;     c9fc3:                       1
;     c9fcf:                       1
;     c9fe4:                       1
;     c9ff4:                       1
;     ca00f:                       1
;     ca011:                       1
;     ca015:                       1
;     ca028:                       1
;     ca038:                       1
;     ca063:                       1
;     ca0a0:                       1
;     ca0a8:                       1
;     ca0c2:                       1
;     ca0c8:                       1
;     ca0e1:                       1
;     ca11b:                       1
;     ca11f:                       1
;     ca14e:                       1
;     ca1ed:                       1
;     ca1ff:                       1
;     ca20b:                       1
;     ca258:                       1
;     ca2cd:                       1
;     ca2fd:                       1
;     ca33a:                       1
;     ca37a:                       1
;     ca3e1:                       1
;     ca466:                       1
;     ca468:                       1
;     ca491:                       1
;     ca4ae:                       1
;     ca4b0:                       1
;     ca4b3:                       1
;     ca53d:                       1
;     ca552:                       1
;     ca579:                       1
;     ca58c:                       1
;     ca5e3:                       1
;     ca613:                       1
;     ca61d:                       1
;     ca625:                       1
;     ca652:                       1
;     ca676:                       1
;     ca6f1:                       1
;     ca701:                       1
;     ca70a:                       1
;     ca726:                       1
;     ca73f:                       1
;     ca76e:                       1
;     ca787:                       1
;     ca7b7:                       1
;     ca7e6:                       1
;     ca808:                       1
;     ca814:                       1
;     ca82a:                       1
;     ca82c:                       1
;     ca8aa:                       1
;     ca90a:                       1
;     ca916:                       1
;     ca927:                       1
;     caa0e:                       1
;     caa35:                       1
;     caa38:                       1
;     caa5d:                       1
;     caaa2:                       1
;     caaac:                       1
;     cab1e:                       1
;     cab25:                       1
;     caba2:                       1
;     caba5:                       1
;     cac0f:                       1
;     cac23:                       1
;     cac5e:                       1
;     cac66:                       1
;     cad03:                       1
;     cad06:                       1
;     cad12:                       1
;     cad1a:                       1
;     cad4d:                       1
;     cad59:                       1
;     cad77:                       1
;     cad83:                       1
;     cadaa:                       1
;     cadc5:                       1
;     cade1:                       1
;     cade9:                       1
;     cae05:                       1
;     cae10:                       1
;     cae20:                       1
;     cae2a:                       1
;     cae30:                       1
;     cae61:                       1
;     cae6d:                       1
;     cae8d:                       1
;     caeaa:                       1
;     cafeb:                       1
;     cb023:                       1
;     cb061:                       1
;     cb06f:                       1
;     cb07f:                       1
;     cb0a1:                       1
;     cb0b9:                       1
;     cb0f8:                       1
;     cb0fb:                       1
;     cb112:                       1
;     cb13c:                       1
;     cb14d:                       1
;     cb1ca:                       1
;     cb1e9:                       1
;     cb1f4:                       1
;     cb202:                       1
;     cb226:                       1
;     cb24a:                       1
;     cb2f0:                       1
;     cb2f3:                       1
;     cb2f9:                       1
;     cb303:                       1
;     cb318:                       1
;     cb34f:                       1
;     cb37f:                       1
;     cb384:                       1
;     cb3a7:                       1
;     cb3ba:                       1
;     cb3c0:                       1
;     cb3f9:                       1
;     cb413:                       1
;     cb4e0:                       1
;     cb536:                       1
;     cb542:                       1
;     cb556:                       1
;     cb567:                       1
;     cb571:                       1
;     cb5cf:                       1
;     cb5db:                       1
;     cb602:                       1
;     cb60f:                       1
;     cb61d:                       1
;     cb637:                       1
;     cb651:                       1
;     cb668:                       1
;     cb66e:                       1
;     cb67e:                       1
;     cb6a3:                       1
;     cb73f:                       1
;     cb766:                       1
;     cb79d:                       1
;     cb7a1:                       1
;     cb81f:                       1
;     cb837:                       1
;     cb84f:                       1
;     cb875:                       1
;     cb88b:                       1
;     cb8a2:                       1
;     cb8d9:                       1
;     cb8dd:                       1
;     cb931:                       1
;     cb95c:                       1
;     cb96a:                       1
;     cb977:                       1
;     cb995:                       1
;     cb9b5:                       1
;     cba13:                       1
;     cba19:                       1
;     cba2b:                       1
;     cba39:                       1
;     cba52:                       1
;     cba69:                       1
;     cba99:                       1
;     cbaa2:                       1
;     cbab0:                       1
;     cbaca:                       1
;     cbacd:                       1
;     cbadc:                       1
;     cbb32:                       1
;     cbb40:                       1
;     cbb9c:                       1
;     cbbad:                       1
;     cbbcd:                       1
;     cbc09:                       1
;     cbc53:                       1
;     cbc5d:                       1
;     cbc66:                       1
;     cbc6d:                       1
;     cbc7c:                       1
;     cbc88:                       1
;     cbce1:                       1
;     cbcea:                       1
;     cbd14:                       1
;     cbdc6:                       1
;     cbde1:                       1
;     cbe34:                       1
;     cbe5f:                       1
;     cbe90:                       1
;     cbe9b:                       1
;     cbf96:                       1
;     cbfc3:                       1
;     cbfdc:                       1
;     cbff6:                       1
;     check_eq_star_bracket:       1
;     exec_star_command:           1
;     execute_line:                1
;     find_proc_fn:                1
;     fn_asn:                      1
;     fn_ln:                       1
;     for_gosub_stack:             1
;     fp_mantissas_add:            1
;     fwa_round_carry:             1
;     fwa_swap_var:                1
;     iwa_div:                     1
;     iwa_mod:                     1
;     iwa_store_var:               1
;     l0047:                       1
;     l0061:                       1
;     l0064:                       1
;     l00c9:                       1
;     l00ff:                       1
;     l0106:                       1
;     l047f:                       1
;     l04f4:                       1
;     l04f6:                       1
;     l04f9:                       1
;     l04fa:                       1
;     l04fb:                       1
;     l04fe:                       1
;     l04ff:                       1
;     l0501:                       1
;     l0502:                       1
;     l0503:                       1
;     l0504:                       1
;     l0505:                       1
;     l0506:                       1
;     l0508:                       1
;     l0509:                       1
;     l050a:                       1
;     l050b:                       1
;     l050d:                       1
;     l050e:                       1
;     l05a3:                       1
;     l05a4:                       1
;     l05b7:                       1
;     l05b8:                       1
;     l05cb:                       1
;     l05cc:                       1
;     l05e5:                       1
;     l05e6:                       1
;     l3185:                       1
;     l6142:                       1
;     l7461:                       1
;     l82df:                       1
;     l8351:                       1
;     l8450:                       1
;     l848a:                       1
;     l84c4:                       1
;     l996b:                       1
;     l99b9:                       1
;     language_startup:            1
;     loop_c853c:                  1
;     loop_c8544:                  1
;     loop_c8567:                  1
;     loop_c8571:                  1
;     loop_c8581:                  1
;     loop_c85a5:                  1
;     loop_c85d5:                  1
;     loop_c85e6:                  1
;     loop_c85f5:                  1
;     loop_c872f:                  1
;     loop_c8864:                  1
;     loop_c8867:                  1
;     loop_c888d:                  1
;     loop_c88ec:                  1
;     loop_c8980:                  1
;     loop_c89cb:                  1
;     loop_c89fe:                  1
;     loop_c8b41:                  1
;     loop_c8b44:                  1
;     loop_c8b47:                  1
;     loop_c8b82:                  1
;     loop_c8c97:                  1
;     loop_c8ca9:                  1
;     loop_c8cdd:                  1
;     loop_c8ce9:                  1
;     loop_c8cf5:                  1
;     loop_c8d2b:                  1
;     loop_c8d4d:                  1
;     loop_c8d59:                  1
;     loop_c8d6c:                  1
;     loop_c8d83:                  1
;     loop_c8da6:                  1
;     loop_c8dad:                  1
;     loop_c8db5:                  1
;     loop_c8dc1:                  1
;     loop_c8e08:                  1
;     loop_c8e14:                  1
;     loop_c8e21:                  1
;     loop_c8e24:                  1
;     loop_c8e40:                  1
;     loop_c8e58:                  1
;     loop_c8e67:                  1
;     loop_c8f53:                  1
;     loop_c8fb1:                  1
;     loop_c8fea:                  1
;     loop_c90dc:                  1
;     loop_c9185:                  1
;     loop_c923a:                  1
;     loop_c92ae:                  1
;     loop_c92b2:                  1
;     loop_c931b:                  1
;     loop_c942a:                  1
;     loop_c9432:                  1
;     loop_c9495:                  1
;     loop_c94cf:                  1
;     loop_c9507:                  1
;     loop_c9527:                  1
;     loop_c9533:                  1
;     loop_c9595:                  1
;     loop_c95d4:                  1
;     loop_c96ff:                  1
;     loop_c97dd:                  1
;     loop_c9821:                  1
;     loop_c985a:                  1
;     loop_c98bf:                  1
;     loop_c98de:                  1
;     loop_c98f3:                  1
;     loop_c9929:                  1
;     loop_c992e:                  1
;     loop_c9948:                  1
;     loop_c995a:                  1
;     loop_c9980:                  1
;     loop_c99f4:                  1
;     loop_c9a01:                  1
;     loop_c9a39:                  1
;     loop_c9a50:                  1
;     loop_c9b03:                  1
;     loop_c9b2c:                  1
;     loop_c9b43:                  1
;     loop_c9b4e:                  1
;     loop_c9b5e:                  1
;     loop_c9b75:                  1
;     loop_c9b8a:                  1
;     loop_c9c15:                  1
;     loop_c9c2d:                  1
;     loop_c9d11:                  1
;     loop_c9d20:                  1
;     loop_c9d8b:                  1
;     loop_c9dcb:                  1
;     loop_c9e24:                  1
;     loop_c9e6c:                  1
;     loop_c9e90:                  1
;     loop_c9e9a:                  1
;     loop_c9eb0:                  1
;     loop_c9ec8:                  1
;     loop_c9f20:                  1
;     loop_c9f6b:                  1
;     loop_c9f7e:                  1
;     loop_c9fdb:                  1
;     loop_c9fe8:                  1
;     loop_ca002:                  1
;     loop_ca055:                  1
;     loop_ca0f5:                  1
;     loop_ca108:                  1
;     loop_ca139:                  1
;     loop_ca2e6:                  1
;     loop_ca3f8:                  1
;     loop_ca528:                  1
;     loop_ca543:                  1
;     loop_ca564:                  1
;     loop_ca57f:                  1
;     loop_ca629:                  1
;     loop_ca63a:                  1
;     loop_ca70c:                  1
;     loop_ca754:                  1
;     loop_ca7a9:                  1
;     loop_ca7cf:                  1
;     loop_ca8b5:                  1
;     loop_cab7f:                  1
;     loop_cacaa:                  1
;     loop_cacd6:                  1
;     loop_cad42:                  1
;     loop_cad4f:                  1
;     loop_cad55:                  1
;     loop_cad8c:                  1
;     loop_cadb6:                  1
;     loop_cadcb:                  1
;     loop_cadcc:                  1
;     loop_cae79:                  1
;     loop_cae93:                  1
;     loop_caec7:                  1
;     loop_caece:                  1
;     loop_caf0a:                  1
;     loop_caf78:                  1
;     loop_caf89:                  1
;     loop_cb017:                  1
;     loop_cb083:                  1
;     loop_cb0df:                  1
;     loop_cb0e1:                  1
;     loop_cb0fe:                  1
;     loop_cb122:                  1
;     loop_cb158:                  1
;     loop_cb18a:                  1
;     loop_cb1a6:                  1
;     loop_cb21c:                  1
;     loop_cb236:                  1
;     loop_cb28e:                  1
;     loop_cb39d:                  1
;     loop_cb3ad:                  1
;     loop_cb3d9:                  1
;     loop_cb451:                  1
;     loop_cb477:                  1
;     loop_cb520:                  1
;     loop_cb538:                  1
;     loop_cb580:                  1
;     loop_cb58a:                  1
;     loop_cb5fc:                  1
;     loop_cb64b:                  1
;     loop_cb6a0:                  1
;     loop_cb6a9:                  1
;     loop_cb7b0:                  1
;     loop_cb7bd:                  1
;     loop_cb8af:                  1
;     loop_cb8e4:                  1
;     loop_cb8f2:                  1
;     loop_cb90a:                  1
;     loop_cb96c:                  1
;     loop_cb980:                  1
;     loop_cb9c7:                  1
;     loop_cb9ca:                  1
;     loop_cb9cf:                  1
;     loop_cba0a:                  1
;     loop_cba21:                  1
;     loop_cba2d:                  1
;     loop_cba3f:                  1
;     loop_cba5f:                  1
;     loop_cbabd:                  1
;     loop_cbb6f:                  1
;     loop_cbb85:                  1
;     loop_cbba6:                  1
;     loop_cbbd6:                  1
;     loop_cbc9e:                  1
;     loop_cbd07:                  1
;     loop_cbd33:                  1
;     loop_cbdbe:                  1
;     loop_cbdd4:                  1
;     loop_cbe78:                  1
;     loop_cbecf:                  1
;     loop_cbfd9:                  1
;     loop_cbfec:                  1
;     osasci:                      1
;     osnewl:                      1
;     resint_a:                    1
;     resint_c:                    1
;     resint_x:                    1
;     resint_y:                    1
;     return_11:                   1
;     return_14:                   1
;     return_15:                   1
;     return_16:                   1
;     return_17:                   1
;     return_18:                   1
;     return_20:                   1
;     return_24:                   1
;     return_27:                   1
;     return_29:                   1
;     return_30:                   1
;     return_32:                   1
;     return_34:                   1
;     return_37:                   1
;     return_38:                   1
;     return_4:                    1
;     return_40:                   1
;     return_5:                    1
;     return_6:                    1
;     return_7:                    1
;     rnd_range:                   1
;     rnd_repeat:                  1
;     rnd_seed:                    1
;     start_new_program:           1
;     stmt_dim:                    1
;     stmt_local:                  1
;     stmt_next:                   1
;     stmt_read:                   1
;     stmt_vdu:                    1
;     sub_c85ba:                   1
;     sub_c8897:                   1
;     sub_c88f5:                   1
;     sub_c893d:                   1
;     sub_c8955:                   1
;     sub_c8cc1:                   1
;     sub_c8f9a:                   1
;     sub_c9231:                   1
;     sub_c94ed:                   1
;     sub_c9539:                   1
;     sub_c9559:                   1
;     sub_c95d5:                   1
;     sub_c9807:                   1
;     sub_c987b:                   1
;     sub_c9880:                   1
;     sub_c9a5f:                   1
;     sub_c9a9e:                   1
;     sub_c9b72:                   1
;     sub_ca040:                   1
;     sub_ca052:                   1
;     sub_ca140:                   1
;     sub_ca14b:                   1
;     sub_ca2ed:                   1
;     sub_ca3e7:                   1
;     sub_ca4b6:                   1
;     sub_ca4c7:                   1
;     sub_ca4e8:                   1
;     sub_ca801:                   1
;     sub_ca9b1:                   1
;     sub_caa94:                   1
;     sub_caada:                   1
;     sub_cad8f:                   1
;     sub_cae02:                   1
;     sub_cae3a:                   1
;     sub_cb197:                   1
;     sub_cb1c8:                   1
;     sub_cb3c5:                   1
;     sub_cb4b7:                   1
;     sub_cb550:                   1
;     sub_cbbfc:                   1
;     sub_cbd2f:                   1
;     sub_cbe55:                   1
;     sub_cbe56:                   1
;     sub_cbe93:                   1
;     sub_cbeb2:                   1
;     sub_cbee7:                   1
;     tokenise_line:               1

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
;     c8aa2
;     c8af3
;     c8b38
;     c8b59
;     c8b87
;     c8b96
;     c8b98
;     c8ba3
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
;     c8ce5
;     c8cee
;     c8cff
;     c8d03
;     c8d26
;     c8d30
;     c8d57
;     c8d64
;     c8d77
;     c8d7d
;     c8d80
;     c8dbb
;     c8dc3
;     c8dd2
;     c8e0e
;     c8e5b
;     c8e5f
;     c8e6a
;     c8e98
;     c8ea4
;     c8ea7
;     c8ecc
;     c8ee0
;     c8f0c
;     c8f1b
;     c8f2e
;     c8f8d
;     c8fd6
;     c8fdf
;     c8fe7
;     c900d
;     c901a
;     c901c
;     c903a
;     c903d
;     c9043
;     c9071
;     c9080
;     c90b5
;     c90df
;     c9127
;     c913c
;     c915e
;     c9168
;     c916b
;     c91b7
;     c91d2
;     c91fc
;     c9203
;     c920b
;     c9215
;     c9218
;     c924b
;     c925a
;     c928a
;     c92a5
;     c92b7
;     c92c0
;     c92f4
;     c92f7
;     c9341
;     c9353
;     c9365
;     c936b
;     c9372
;     c93d7
;     c93da
;     c93ea
;     c93fd
;     c9453
;     c946f
;     c9479
;     c949a
;     c94a7
;     c94b3
;     c94d4
;     c94e1
;     c9501
;     c9516
;     c9541
;     c954d
;     c9556
;     c955b
;     c956d
;     c9571
;     c957a
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
;     c9859
;     c9861
;     c986d
;     c9877
;     c98ac
;     c98b7
;     c98bc
;     c98cc
;     c98e1
;     c98e3
;     c98f1
;     c9902
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
;     c9c03
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
;     c9e23
;     c9e35
;     c9e59
;     c9e88
;     c9e96
;     c9eb7
;     c9ebf
;     c9ed1
;     c9ee8
;     c9ef5
;     c9ef9
;     c9efb
;     c9f0f
;     c9f1d
;     c9f25
;     c9f31
;     c9f34
;     c9f39
;     c9f5c
;     c9f71
;     c9f92
;     c9f9c
;     c9fa0
;     c9fad
;     c9fc3
;     c9fcf
;     c9fe4
;     c9fe6
;     c9ff4
;     ca00f
;     ca011
;     ca015
;     ca028
;     ca038
;     ca063
;     ca066
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
;     ca197
;     ca1ed
;     ca1ff
;     ca208
;     ca20b
;     ca258
;     ca2cd
;     ca2fd
;     ca313
;     ca336
;     ca33a
;     ca37a
;     ca387
;     ca3e1
;     ca40c
;     ca43c
;     ca450
;     ca466
;     ca468
;     ca46c
;     ca491
;     ca4ae
;     ca4b0
;     ca4b3
;     ca53d
;     ca552
;     ca579
;     ca58c
;     ca590
;     ca5e3
;     ca613
;     ca61d
;     ca625
;     ca652
;     ca659
;     ca676
;     ca67c
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
;     ca7b7
;     ca7e6
;     ca7f7
;     ca808
;     ca814
;     ca82a
;     ca82c
;     ca8aa
;     ca8ea
;     ca8fe
;     ca904
;     ca90a
;     ca916
;     ca91b
;     ca927
;     ca936
;     ca99e
;     ca9aa
;     ca9c3
;     caa0e
;     caa35
;     caa38
;     caa4e
;     caa5d
;     caaa2
;     caaac
;     caab8
;     caad1
;     cab1e
;     cab25
;     cab9d
;     caba0
;     caba2
;     caba5
;     cabb8
;     cabe6
;     cac0f
;     cac23
;     cac5e
;     cac66
;     cac73
;     cac95
;     cac9b
;     cad03
;     cad06
;     cad12
;     cad1a
;     cad3c
;     cad4d
;     cad52
;     cad59
;     cad67
;     cad77
;     cad83
;     cad89
;     cadaa
;     cadc5
;     cadc9
;     cade1
;     cade9
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
;     caed8
;     cafc2
;     cafeb
;     cb023
;     cb02e
;     cb033
;     cb036
;     cb061
;     cb06f
;     cb07f
;     cb0a1
;     cb0b9
;     cb0bf
;     cb0f5
;     cb0f8
;     cb0fb
;     cb112
;     cb11a
;     cb12d
;     cb13c
;     cb14d
;     cb1ca
;     cb1e9
;     cb1f4
;     cb202
;     cb226
;     cb24a
;     cb24d
;     cb2b5
;     cb2ca
;     cb2f0
;     cb2f3
;     cb2f9
;     cb303
;     cb318
;     cb329
;     cb32c
;     cb34f
;     cb354
;     cb37f
;     cb384
;     cb3a7
;     cb3ba
;     cb3c0
;     cb3f9
;     cb413
;     cb48f
;     cb4ae
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
;     cb5cf
;     cb5d8
;     cb5db
;     cb602
;     cb60f
;     cb61d
;     cb637
;     cb639
;     cb651
;     cb668
;     cb66e
;     cb678
;     cb67e
;     cb688
;     cb68e
;     cb6a3
;     cb6be
;     cb6d7
;     cb73f
;     cb741
;     cb751
;     cb766
;     cb79d
;     cb7a1
;     cb7a4
;     cb81f
;     cb837
;     cb84f
;     cb875
;     cb88b
;     cb8a2
;     cb8d2
;     cb8d9
;     cb8dd
;     cb931
;     cb944
;     cb95c
;     cb96a
;     cb977
;     cb97d
;     cb995
;     cb9af
;     cb9b5
;     cb9c4
;     cb9da
;     cba13
;     cba19
;     cba2b
;     cba39
;     cba52
;     cba5a
;     cba69
;     cba99
;     cbaa2
;     cbab0
;     cbaca
;     cbacd
;     cbadc
;     cbb07
;     cbb15
;     cbb32
;     cbb40
;     cbb7a
;     cbb9c
;     cbbad
;     cbbcd
;     cbc09
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
;     cbd14
;     cbdc6
;     cbddc
;     cbde1
;     cbe34
;     cbe41
;     cbe5f
;     cbe90
;     cbe9b
;     cbe9e
;     cbf82
;     cbf96
;     cbfc3
;     cbfdc
;     cbff6
;     l0001
;     l0007
;     l0009
;     l000c
;     l000e
;     l000f
;     l0010
;     l0011
;     l0013
;     l0017
;     l001a
;     l001d
;     l0022
;     l0038
;     l003a
;     l0044
;     l0045
;     l0046
;     l0047
;     l0048
;     l0049
;     l004a
;     l004d
;     l004e
;     l0061
;     l0064
;     l00c9
;     l00fd
;     l00ff
;     l0100
;     l0106
;     l01ff
;     l0401
;     l0402
;     l0403
;     l043d
;     l0441
;     l047f
;     l04f1
;     l04f2
;     l04f3
;     l04f4
;     l04f5
;     l04f6
;     l04f7
;     l04f9
;     l04fa
;     l04fb
;     l04fc
;     l04fe
;     l04ff
;     l0501
;     l0502
;     l0503
;     l0504
;     l0505
;     l0506
;     l0508
;     l0509
;     l050a
;     l050b
;     l050d
;     l050e
;     l05a3
;     l05a4
;     l05b7
;     l05b8
;     l05cb
;     l05cc
;     l05e5
;     l05e6
;     l05ff
;     l06ff
;     l3185
;     l6142
;     l7461
;     l82df
;     l8351
;     l8450
;     l848a
;     l84c4
;     l996b
;     l99b9
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
;     loop_c8b82
;     loop_c8c97
;     loop_c8ca9
;     loop_c8cdd
;     loop_c8ce9
;     loop_c8cf5
;     loop_c8d2b
;     loop_c8d4d
;     loop_c8d59
;     loop_c8d6c
;     loop_c8d83
;     loop_c8da6
;     loop_c8dad
;     loop_c8db5
;     loop_c8dc1
;     loop_c8e08
;     loop_c8e14
;     loop_c8e21
;     loop_c8e24
;     loop_c8e40
;     loop_c8e58
;     loop_c8e67
;     loop_c8f53
;     loop_c8fb1
;     loop_c8fea
;     loop_c90dc
;     loop_c9185
;     loop_c923a
;     loop_c92ae
;     loop_c92b2
;     loop_c931b
;     loop_c942a
;     loop_c9432
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
;     loop_c98bf
;     loop_c98de
;     loop_c98f3
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
;     loop_c9c15
;     loop_c9c2d
;     loop_c9d11
;     loop_c9d20
;     loop_c9d8b
;     loop_c9dcb
;     loop_c9e24
;     loop_c9e6c
;     loop_c9e90
;     loop_c9e9a
;     loop_c9eb0
;     loop_c9ec8
;     loop_c9f20
;     loop_c9f6b
;     loop_c9f7e
;     loop_c9fdb
;     loop_c9fe8
;     loop_ca002
;     loop_ca055
;     loop_ca0f5
;     loop_ca108
;     loop_ca139
;     loop_ca2e6
;     loop_ca3f8
;     loop_ca528
;     loop_ca543
;     loop_ca564
;     loop_ca57f
;     loop_ca629
;     loop_ca63a
;     loop_ca70c
;     loop_ca754
;     loop_ca7a9
;     loop_ca7cf
;     loop_ca8b5
;     loop_cab7f
;     loop_cacaa
;     loop_cacd6
;     loop_cad42
;     loop_cad4f
;     loop_cad55
;     loop_cad8c
;     loop_cadb6
;     loop_cadcb
;     loop_cadcc
;     loop_cae79
;     loop_cae93
;     loop_caec7
;     loop_caece
;     loop_caf0a
;     loop_caf78
;     loop_caf89
;     loop_cb017
;     loop_cb083
;     loop_cb0df
;     loop_cb0e1
;     loop_cb0fe
;     loop_cb122
;     loop_cb158
;     loop_cb18a
;     loop_cb1a6
;     loop_cb21c
;     loop_cb236
;     loop_cb28e
;     loop_cb39d
;     loop_cb3ad
;     loop_cb3d9
;     loop_cb451
;     loop_cb477
;     loop_cb520
;     loop_cb538
;     loop_cb580
;     loop_cb58a
;     loop_cb5fc
;     loop_cb64b
;     loop_cb6a0
;     loop_cb6a9
;     loop_cb7b0
;     loop_cb7bd
;     loop_cb8af
;     loop_cb8e4
;     loop_cb8f2
;     loop_cb90a
;     loop_cb96c
;     loop_cb980
;     loop_cb9c7
;     loop_cb9ca
;     loop_cb9cf
;     loop_cba0a
;     loop_cba21
;     loop_cba2d
;     loop_cba3f
;     loop_cba5f
;     loop_cbabd
;     loop_cbb6f
;     loop_cbb85
;     loop_cbba6
;     loop_cbbd6
;     loop_cbc9e
;     loop_cbd07
;     loop_cbd33
;     loop_cbdbe
;     loop_cbdd4
;     loop_cbe78
;     loop_cbecf
;     loop_cbfd9
;     loop_cbfec
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
;     return_29
;     return_3
;     return_30
;     return_31
;     return_32
;     return_33
;     return_34
;     return_35
;     return_36
;     return_37
;     return_38
;     return_39
;     return_4
;     return_40
;     return_5
;     return_6
;     return_7
;     return_8
;     return_9
;     sub_c834e
;     sub_c847b
;     sub_c85ba
;     sub_c8827
;     sub_c882c
;     sub_c882f
;     sub_c8832
;     sub_c887c
;     sub_c8897
;     sub_c88f5
;     sub_c8926
;     sub_c893d
;     sub_c894b
;     sub_c8955
;     sub_c8c1e
;     sub_c8c21
;     sub_c8cc1
;     sub_c8e70
;     sub_c8e8a
;     sub_c8f1e
;     sub_c8f69
;     sub_c8f92
;     sub_c8f9a
;     sub_c909f
;     sub_c9222
;     sub_c9231
;     sub_c9236
;     sub_c92da
;     sub_c92dd
;     sub_c92e3
;     sub_c92eb
;     sub_c92ee
;     sub_c92fa
;     sub_c92fd
;     sub_c9456
;     sub_c94ed
;     sub_c94fc
;     sub_c9531
;     sub_c9539
;     sub_c9559
;     sub_c9582
;     sub_c95c9
;     sub_c95d5
;     sub_c95dd
;     sub_c96df
;     sub_c97ba
;     sub_c97df
;     sub_c97eb
;     sub_c9807
;     sub_c9841
;     sub_c9852
;     sub_c987b
;     sub_c9880
;     sub_c9890
;     sub_c9905
;     sub_c991f
;     sub_c9923
;     sub_c9970
;     sub_c99be
;     sub_c9a5f
;     sub_c9a9d
;     sub_c9a9e
;     sub_c9b29
;     sub_c9b6b
;     sub_c9b72
;     sub_c9b9c
;     sub_c9c42
;     sub_c9dce
;     sub_c9dd1
;     sub_c9e1d
;     sub_c9e20
;     sub_ca040
;     sub_ca052
;     sub_ca064
;     sub_ca07b
;     sub_ca140
;     sub_ca14b
;     sub_ca178
;     sub_ca23f
;     sub_ca242
;     sub_ca2ed
;     sub_ca3e7
;     sub_ca486
;     sub_ca4b6
;     sub_ca4c7
;     sub_ca4d0
;     sub_ca4e8
;     sub_ca7e9
;     sub_ca7ed
;     sub_ca7f1
;     sub_ca7f5
;     sub_ca801
;     sub_ca897
;     sub_ca9b1
;     sub_ca9d3
;     sub_caa48
;     sub_caa4c
;     sub_caa55
;     sub_caa94
;     sub_caada
;     sub_cab12
;     sub_cad8f
;     sub_cadad
;     sub_cae02
;     sub_cae3a
;     sub_caf87
;     sub_cafad
;     sub_cb197
;     sub_cb1c8
;     sub_cb30d
;     sub_cb3c5
;     sub_cb4b1
;     sub_cb4b4
;     sub_cb4b7
;     sub_cb50e
;     sub_cb545
;     sub_cb550
;     sub_cb562
;     sub_cb577
;     sub_cb99a
;     sub_cbb50
;     sub_cbbfc
;     sub_cbc02
;     sub_cbc25
;     sub_cbc2d
;     sub_cbc81
;     sub_cbc8d
;     sub_cbd20
;     sub_cbd2f
;     sub_cbd3a
;     sub_cbd7e
;     sub_cbd90
;     sub_cbdcb
;     sub_cbdff
;     sub_cbe0b
;     sub_cbe0d
;     sub_cbe55
;     sub_cbe56
;     sub_cbe62
;     sub_cbe6f
;     sub_cbe92
;     sub_cbe93
;     sub_cbeb2
;     sub_cbeba
;     sub_cbed2
;     sub_cbedd
;     sub_cbee7
;     sub_cbfa9
;     sub_cbfb5
;     sub_cbfcf

; Stats:
;     Total size (Code + Data) = 16384 bytes
;     Code                     = 14424 bytes (88%)
;     Data                     = 1960 bytes (12%)
;
;     Number of instructions   = 7131
;     Number of data bytes     = 945 bytes
;     Number of data words     = 0 bytes
;     Number of string bytes   = 1015 bytes
;     Number of strings        = 189
