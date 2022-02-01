import matplotlib.pyplot as plt
import numpy as np
import person_detection as pd

FIGURE = 'test_data/newfigure.jpg'

class heatmap_visualisations:
    def __init__(self, imageData):
        self.imageData = imageData
        self.backgroundTempPar = np.array([[16.6709062, 17.09161765, 18.34942799, 19.41754636, 18.72287926, 19.04444098
, 19.07292414, 19.23124633, 19.16825413, 19.1536862, 18.98958895, 19.42954068
, 19.32348875, 19.25924788, 18.87288388, 19.0478082, 19.08957563, 19.1388281
, 18.79265369, 19.38465747, 18.86217906, 18.79575978, 18.07482788, 18.88722127
, 18.34647321, 18.54096001, 18.00152206, 18.77458168, 18.35033894, 18.17770941
, 16.88020037, 16.94098329]
, [16.95136138, 18.02720417, 18.69269346, 18.54933577, 18.70284987, 18.89268124
, 18.71616305, 19.33622475, 19.53180217, 19.29398874, 19.18724113, 19.50012522
, 19.04817899, 19.68250418, 19.3176526, 19.42161686, 18.86778826, 19.05224613
, 19.19820697, 18.87540652, 19.06926707, 18.8270567, 18.30042709, 18.80987075
, 17.99186676, 18.61896624, 18.11810616, 18.09719915, 18.3277685, 17.84571447
, 17.32091067, 17.06248326]
, [18.5097159, 18.45341604, 18.72781798, 19.0668296, 19.17505873, 19.69564863
, 18.92874121, 19.84118524, 20.06592085, 19.62965253, 19.40115401, 19.88101934
, 19.60382525, 19.78472253, 19.55687791, 19.44523743, 19.35999116, 19.75302398
, 18.9210884, 19.39628107, 18.35823243, 19.05900701, 18.56979302, 18.63124391
, 18.03432938, 18.69585758, 17.77008727, 18.60074965, 18.21942295, 18.02457387
, 17.07478454, 17.58716185]
, [17.59072418, 18.42747072, 18.73455818, 19.22706618, 19.25330222, 19.16611263
, 19.58436043, 19.37373173, 19.92929323, 19.85968521, 19.81101008, 19.68155766
, 19.84485166, 19.68834332, 19.43878531, 19.54120209, 19.60013819, 19.20458634
, 18.85251688, 18.77760922, 18.63103344, 18.80860718, 18.71600624, 18.30942479
, 18.12701469, 18.06651671, 18.04962206, 17.94451071, 17.39736777, 17.99068403
, 17.65124751, 17.06651324]
, [18.11696142, 18.30585902, 18.68332068, 19.20373504, 19.48011606, 19.62824111
, 19.37737016, 20.01165917, 20.03237593, 19.99213928, 19.39275814, 20.10046579
, 19.95436644, 20.06567577, 19.71043381, 19.91969073, 19.20444712, 19.02853404
, 18.49308139, 18.9816159, 18.00497088, 18.53982375, 18.06086314, 18.42406933
, 18.18505651, 18.30108831, 17.70753559, 18.31605191, 17.895251, 17.90943609
, 17.36923091, 17.4174458]
, [18.37430787, 18.97076815, 18.49274478, 18.90273834, 19.56377197, 19.44713119
, 19.71088737, 19.59208481, 19.68950273, 19.81838326, 20.10934268, 20.03933122
, 19.78674655, 19.84167507, 19.87174361, 19.92755, 19.46934804, 19.26468253
, 18.79022834, 18.78684548, 18.19805337, 18.46843841, 18.24540018, 18.40796331
, 18.54040278, 18.76732559, 18.30629006, 17.85740373, 17.95308249, 17.78213763
, 18.26765797, 18.26452386]
, [18.79121642, 18.95101687, 18.95137349, 19.2393917, 19.36669915, 19.3259148
, 19.52318333, 19.78829607, 19.80949909, 19.92800751, 20.02724664, 20.16185172
, 20.24979384, 19.79460261, 19.59735253, 20.16431252, 19.44780752, 19.53947125
, 18.90777109, 19.35599797, 18.96804439, 18.91378713, 18.9486942, 19.23602956
, 19.06125513, 19.06815604, 18.18654332, 18.55533739, 18.3196198, 17.90478992
, 19.89568103, 20.32778902]
, [18.54231879, 18.88047911, 19.03157848, 19.44707386, 19.26619633, 19.12935244
, 19.65439976, 19.85836487, 19.56540008, 19.70499942, 19.81288188, 20.07233246
, 19.93311354, 20.04296706, 19.85712351, 19.75817909, 19.24003213, 19.62726952
, 19.37582729, 19.33392726, 19.35534355, 19.62172055, 19.49394343, 19.38125095
, 19.23980104, 19.42868013, 18.37149432, 18.5667761, 18.33145148, 18.7897973
, 21.32487567, 21.47628519]
, [18.71936397, 19.23920484, 18.62292454, 19.37865786, 19.33995058, 19.2726965
, 19.44802141, 19.83943067, 19.53453264, 19.81504039, 19.56308081, 19.94262413
, 19.94029084, 19.9719431, 19.8236295, 19.84901786, 19.93262369, 19.67695676
, 19.56751338, 19.97759981, 19.60535071, 19.53517006, 19.24362837, 19.62399063
, 19.24429687, 19.24337209, 18.34135159, 18.78580504, 18.06057174, 18.18728785
, 20.32927016, 21.71669753]
, [18.21836172, 19.01326379, 19.03639309, 18.99993596, 19.5146844, 19.21646341
, 20.04758522, 19.87697772, 19.95085761, 19.92036276, 19.76897584, 19.85918829
, 19.76749041, 19.77549901, 19.94767615, 19.8617713, 19.79367924, 19.75633498
, 19.66320373, 19.73114106, 19.62250054, 19.81138604, 19.34399657, 19.51447876
, 19.2306811, 19.38030141, 18.73400109, 18.53641612, 18.3943509, 18.90548643
, 20.96706651, 21.91846875]
, [18.5242532, 18.82746044, 18.32928179, 19.03398727, 19.09622385, 19.32731985
, 19.66940706, 20.04185531, 19.8939092, 19.78034107, 19.12810801, 19.89782373
, 19.8533504, 19.99855459, 19.46332063, 19.71624577, 19.53520501, 19.58809357
, 19.56954737, 19.4081559, 19.51270911, 19.78485062, 19.15551499, 19.80897899
, 19.5259134, 19.66812356, 18.70883429, 18.54572592, 18.78864439, 19.14551947
, 20.74962124, 21.73875197]
, [18.03831219, 18.71777525, 18.71364075, 18.63380799, 18.80790283, 19.39393955
, 19.75455634, 19.89422583, 19.40688964, 19.72449547, 19.41454587, 19.60952686
, 19.81648145, 20.02667833, 19.61287606, 19.73794192, 19.61094143, 19.73289375
, 19.53187689, 19.42427436, 19.40519372, 19.7633085, 19.28745811, 19.6134599
, 19.15010191, 19.42704899, 18.81246663, 18.35282345, 18.36324556, 19.2115445
, 20.96858414, 21.8114385]
, [18.29499011, 18.76148738, 18.50790539, 18.98098268, 18.96993076, 19.19992416
, 19.33246678, 19.51106363, 19.28880316, 19.32598997, 19.47355147, 19.82141432
, 19.93419024, 19.94351516, 19.69329629, 19.8509915, 19.49386203, 19.66731765
, 19.31553346, 19.80910967, 19.6851658, 19.65951672, 19.46087325, 19.78661799
, 19.42826571, 19.72022053, 18.74413691, 18.97109495, 19.06330046, 19.19185027
, 19.34019422, 20.6309014]
, [17.69306607, 18.52307191, 18.53138322, 18.96416124, 18.84490461, 19.282277
, 19.43009508, 19.26390751, 19.18629331, 19.64408905, 19.73774257, 19.65357413
, 19.85812687, 19.85072984, 19.69321249, 20.01894685, 19.68333964, 19.75700979
, 19.40411467, 19.61053131, 19.58494744, 19.4911324, 19.64956121, 19.79257503
, 19.58421541, 19.73220663, 19.30138619, 19.46157998, 19.16405015, 19.24304816
, 19.28440774, 19.64976535]
, [17.99736482, 18.51130807, 18.30727101, 18.69732349, 19.25063994, 19.04671734
, 19.61584284, 20.20480673, 19.47970556, 19.78589608, 19.55204428, 19.94942979
, 19.92653446, 19.9581151, 19.63275114, 19.9260678, 19.65081755, 20.04119512
, 19.82102306, 20.07485408, 19.84071861, 19.67711688, 19.58263161, 19.80313955
, 19.54896877, 19.56319045, 18.73379116, 18.76951869, 18.98193166, 19.14346977
, 19.10060798, 20.03089283]
, [17.67938118, 18.12831064, 18.64162556, 19.20832462, 19.30585784, 19.25446667
, 19.6642762, 19.91547238, 19.50932734, 19.79467327, 19.78934516, 19.55719039
, 19.9191366, 20.12445299, 20.11984372, 20.12264948, 20.12762307, 20.19048395
, 20.14871155, 20.1226275, 19.95426115, 19.82557848, 20.0508258, 19.74474767
, 19.45820906, 19.91110205, 19.15445933, 18.64191849, 18.86133842, 18.97150421
, 19.13811404, 20.230665]
, [18.01938212, 18.17114128, 18.05422466, 18.71436097, 18.85734843, 18.95075014
, 18.9319764, 19.65442003, 20.34950512, 20.6037294, 20.25622681, 20.90970034
, 21.07281013, 21.25765572, 21.05256676, 21.45243072, 21.32449834, 21.31934117
, 20.99289969, 21.31987067, 21.26928291, 21.14402837, 20.82656962, 20.51655893
, 19.87727506, 19.98630555, 19.07141757, 19.72772382, 19.49008548, 19.20686897
, 18.8892995, 19.67390067]
, [17.43930953, 17.96302126, 18.44502168, 18.51547086, 18.15931405, 18.82214044
, 19.02467875, 19.51857732, 20.43195938, 20.63011267, 20.96774403, 21.18495219
, 20.9934796, 21.50496369, 21.24828623, 21.24419753, 21.17873211, 21.33035505
, 20.87464899, 21.13989685, 20.88952162, 20.89358816, 20.83561952, 20.46470839
, 20.15681079, 20.0920591, 19.99421967, 19.71076119, 19.40551919, 19.22405447
, 18.91193192, 19.20476076]
, [17.81566336, 17.79367894, 17.99882155, 18.45415415, 18.41112171, 18.43391018
, 18.75819024, 19.55463026, 19.39572936, 19.61668139, 19.90791297, 20.38636654
, 21.13639938, 21.34614537, 21.05826422, 21.28698412, 20.97928469, 21.30653737
, 20.96727599, 21.15320159, 20.9366147, 21.09324043, 20.79207801, 20.70831949
, 20.31950001, 20.45387329, 19.75888066, 19.93090714, 19.57012889, 19.75876209
, 18.63845451, 19.67957792]
, [16.88672922, 18.16402147, 18.13018049, 17.87904873, 18.13648016, 18.43215908
, 18.85929482, 18.821552, 18.97918147, 19.68489376, 20.03545744, 20.35843275
, 20.4811448, 21.05095806, 20.92769273, 21.08050656, 20.95669378, 21.30524373
, 21.02525132, 20.9518877, 21.08247751, 21.00650755, 20.96005234, 20.52583118
, 20.42400045, 20.56928694, 20.36658343, 20.58037359, 19.7303925, 20.27737626
, 19.82888612, 19.7971012]
, [17.0629544, 16.79838918, 17.0734562, 17.79979035, 18.39473023, 18.1081544
, 18.01041409, 18.65380935, 18.78817197, 19.36980092, 19.34614356, 20.56175711
, 21.02620802, 21.00267679, 20.73855933, 21.18697038, 20.999129, 21.22042299
, 20.83932148, 21.31718496, 20.90877139, 20.9332258, 20.47801074, 21.28539867
, 20.79704142, 20.70984451, 20.40179612, 20.98467959, 20.47696219, 20.04886742
, 19.86095804, 20.04616511]
, [16.61617006, 17.90311989, 17.31974714, 17.6333652, 17.67824157, 18.25977458
, 17.98100615, 18.58792055, 18.58938127, 19.20219022, 19.42108775, 20.17318622
, 20.90581463, 21.08726426, 21.12065901, 21.1205743, 20.89128874, 21.18321784
, 20.84462993, 21.24360544, 21.06789957, 20.70089001, 20.74932501, 20.88387347
, 20.48217288, 20.85465056, 20.56012726, 20.84823578, 19.95961892, 20.45164654
, 20.33481108, 20.21198613]
, [16.82166124, 17.90668773, 17.25755399, 17.62155791, 17.62256804, 18.38722238
, 17.8616314, 18.57807634, 18.24195334, 18.4284024, 19.00202577, 19.39088268
, 20.26571811, 20.68561683, 20.63982187, 21.34566025, 21.05560658, 20.84267661
, 20.85979132, 21.06443266, 20.6188402, 20.60107218, 20.46028334, 20.90890527
, 20.50813661, 20.47766486, 20.19679393, 20.65041232, 20.31321793, 20.48300169
, 19.84220455, 20.29253702]
, [16.49147433, 17.27618614, 16.97248015, 17.58324397, 17.06381809, 18.49854654
, 17.77084349, 18.31806351, 18.35090458, 18.54702201, 18.40796687, 18.86349936
, 19.36041346, 19.77751003, 20.47144923, 20.91484877, 21.01421444, 21.0714054
, 20.87538698, 20.95377927, 20.46009762, 20.9774684, 20.70515933, 20.67449891
, 20.23841894, 20.44827457, 20.4384111, 20.54270623, 20.23164631, 20.7128333
, 20.50287062, 21.25368099]])
        self.backgroundTempDel = np.array([[6.81739901, 6.97458325, 7.03065754, 7.1592326, 7.17752869, 7.19672629
, 7.18108764, 7.20427243, 7.1974497, 7.2112473, 7.20096772, 7.24808941
, 7.21321786, 7.20897333, 7.21574884, 7.22595269, 7.25683155, 7.19726041
, 7.19149123, 7.24586148, 7.22188439, 7.23678818, 7.22302722, 7.22910617
, 7.17636532, 7.2151376, 7.16540079, 7.17839112, 7.12061503, 7.09351447
, 7.01668446, 6.94826739]
, [7.00991846, 6.9759833, 7.16099123, 7.14495389, 7.16938414, 7.15223116
, 7.18298885, 7.1917466, 7.20741737, 7.2261145, 7.21521122, 7.20975835
, 7.20077919, 7.20478236, 7.20699164, 7.25555366, 7.23128429, 7.24045991
, 7.25555436, 7.23531424, 7.21738003, 7.21471244, 7.23593138, 7.24113558
, 7.18621145, 7.20332951, 7.17686111, 7.22610219, 7.18048867, 7.11900275
, 7.1138233, 7.06366746]
, [7.07258865, 7.1306146, 7.17425603, 7.18175146, 7.15020331, 7.18880973
, 7.17796074, 7.22150203, 7.21902564, 7.23239917, 7.25112221, 7.26076225
, 7.2313928, 7.24985032, 7.22484585, 7.25534867, 7.2299878, 7.24403029
, 7.2519321, 7.26423389, 7.2396993, 7.23878224, 7.21483521, 7.23208146
, 7.207147, 7.21139931, 7.16754859, 7.17491359, 7.13931431, 7.15330392
, 7.11984678, 7.13251261]
, [7.08008785, 7.04247151, 7.18796375, 7.19630551, 7.21748519, 7.19096188
, 7.22074283, 7.20477935, 7.21449297, 7.20857015, 7.25313334, 7.23689117
, 7.25186636, 7.23372235, 7.25102416, 7.24931039, 7.24979224, 7.23828738
, 7.23179145, 7.25091306, 7.25708487, 7.26659483, 7.21750116, 7.24278199
, 7.17751865, 7.19778288, 7.1919468, 7.183977, 7.14069505, 7.13662746
, 7.09945181, 7.12287198]
, [7.11547831, 7.08548966, 7.17419579, 7.20657092, 7.16818181, 7.19385453
, 7.21853585, 7.22497809, 7.24859085, 7.25113141, 7.25970433, 7.27381944
, 7.27475541, 7.27531381, 7.26727768, 7.27617325, 7.25369819, 7.25931647
, 7.26248387, 7.31166174, 7.2452518, 7.27668046, 7.22336352, 7.25695052
, 7.21721644, 7.21738192, 7.18824411, 7.21221963, 7.179545, 7.14872658
, 7.14040406, 7.10591259]
, [7.10338932, 7.12157067, 7.17220613, 7.16885763, 7.16235014, 7.19680707
, 7.26970539, 7.24770686, 7.2782209, 7.27616104, 7.27220322, 7.28383149
, 7.28002333, 7.26557513, 7.26587367, 7.27755889, 7.24960548, 7.24278273
, 7.25129851, 7.250139, 7.23064955, 7.22777465, 7.24469711, 7.24159851
, 7.1979507, 7.22022906, 7.21878094, 7.19144494, 7.15189682, 7.15896999
, 7.16478503, 7.1603892]
, [7.09401111, 7.12523577, 7.12389066, 7.16020721, 7.15575634, 7.18344025
, 7.21824466, 7.25667986, 7.2424403, 7.25347935, 7.23724005, 7.2393572
, 7.22300794, 7.24873676, 7.23779732, 7.26322017, 7.240654, 7.2390554
, 7.21940003, 7.23211547, 7.20504226, 7.20424851, 7.21656613, 7.25162809
, 7.2207392, 7.21987194, 7.19086009, 7.21253631, 7.18659168, 7.14036289
, 7.13766294, 7.15298879]
, [7.12809924, 7.14236959, 7.13442839, 7.18498382, 7.18513346, 7.19583062
, 7.20105711, 7.20941922, 7.22556624, 7.21319036, 7.25426657, 7.23492067
, 7.23588141, 7.22277109, 7.25361143, 7.24252852, 7.25264746, 7.23047439
, 7.24474187, 7.21069328, 7.19938275, 7.23352738, 7.24681492, 7.23788324
, 7.21398562, 7.22730048, 7.208356, 7.20485403, 7.14483626, 7.17686599
, 7.13117836, 7.17888348]
, [7.11150558, 7.10948333, 7.15197525, 7.15743116, 7.17441058, 7.20663231
, 7.18154343, 7.20137044, 7.18725878, 7.2298841, 7.22359652, 7.22906208
, 7.21159649, 7.22955251, 7.21490527, 7.23595197, 7.22724093, 7.21506026
, 7.2052443, 7.23607132, 7.23747882, 7.20451844, 7.2082493, 7.23403752
, 7.20530749, 7.21454518, 7.17486558, 7.23105394, 7.20091109, 7.16430423
, 7.14601195, 7.17102489]
, [7.10192105, 7.13774102, 7.18479151, 7.19130583, 7.16570754, 7.19227245
, 7.17772968, 7.23035922, 7.19999426, 7.20972281, 7.21931844, 7.20630566
, 7.22199575, 7.21095246, 7.22593583, 7.22310077, 7.21762203, 7.22266891
, 7.20282808, 7.21124652, 7.2113594, 7.22165845, 7.2033521, 7.21627725
, 7.20687308, 7.21213637, 7.20399351, 7.20947031, 7.17332787, 7.17124083
, 7.15009901, 7.17625003]
, [7.1308046, 7.17998096, 7.14588527, 7.19132271, 7.18795989, 7.18985311
, 7.19482809, 7.20557438, 7.22079509, 7.23208791, 7.18078054, 7.21260701
, 7.19331455, 7.20805202, 7.21310147, 7.23237145, 7.23133921, 7.22351122
, 7.20550232, 7.21262084, 7.20142901, 7.21773309, 7.21785697, 7.22522368
, 7.22121721, 7.21793024, 7.19239748, 7.18844106, 7.18962455, 7.15425969
, 7.1646035, 7.13492101]
, [7.19009902, 7.1424559, 7.14813238, 7.16732397, 7.17624688, 7.1758348
, 7.20627572, 7.20756956, 7.20104013, 7.21060566, 7.19875647, 7.21369607
, 7.21006367, 7.19703145, 7.21507932, 7.21850644, 7.22786203, 7.21174139
, 7.23101976, 7.22408538, 7.20678286, 7.2018263, 7.20135515, 7.20858998
, 7.20949987, 7.19959477, 7.21312697, 7.1768159, 7.15991443, 7.19572801
, 7.1356048, 7.18537415]
, [7.20978385, 7.20819381, 7.24189505, 7.27972524, 7.2291468, 7.20373192
, 7.20841462, 7.22805363, 7.21369818, 7.19969471, 7.2162887, 7.25178247
, 7.22267425, 7.22351122, 7.19300384, 7.2102819, 7.22122298, 7.23349658
, 7.22328643, 7.21762937, 7.20462478, 7.20437148, 7.21072322, 7.21872262
, 7.18433264, 7.21391979, 7.19202826, 7.21600815, 7.15658193, 7.16692362
, 7.14515144, 7.15461183]
, [7.18654542, 7.22818092, 7.26719092, 7.25626373, 7.26129804, 7.25270436
, 7.25231046, 7.24023557, 7.21835686, 7.22120004, 7.23488559, 7.22267906
, 7.23434682, 7.23327803, 7.20994615, 7.22763073, 7.22384048, 7.24491353
, 7.22110398, 7.20040189, 7.22782811, 7.18680162, 7.22659837, 7.22497002
, 7.20035674, 7.20326235, 7.21396988, 7.16612361, 7.17305208, 7.16968848
, 7.11248226, 7.2047369]
, [7.12609983, 7.17546065, 7.18064193, 7.20585649, 7.19464318, 7.20112421
, 7.18512118, 7.21700381, 7.19781275, 7.21966843, 7.2103705, 7.23866769
, 7.25434823, 7.24140824, 7.22893767, 7.24251193, 7.2240955, 7.23428955
, 7.22065351, 7.21383835, 7.20219249, 7.20313701, 7.20045767, 7.22919774
, 7.21484691, 7.18137833, 7.19367431, 7.20187541, 7.1627208, 7.15988685
, 7.10902699, 7.15515845]
, [7.11939573, 7.12179012, 7.16609473, 7.16604368, 7.15279532, 7.19001944
, 7.18026877, 7.17103828, 7.19978467, 7.21011745, 7.21545945, 7.21396253
, 7.24065813, 7.23201671, 7.25064305, 7.2558606, 7.22743787, 7.21569223
, 7.2136255, 7.23525766, 7.22278181, 7.20995699, 7.26120544, 7.22339872
, 7.19576655, 7.19963171, 7.15278786, 7.20664785, 7.1789557, 7.15925234
, 7.18672525, 7.1977581]
, [7.08922698, 7.13275392, 7.13242473, 7.15058385, 7.13267552, 7.16214894
, 7.15200311, 7.19774176, 7.15726013, 7.19212376, 7.21239898, 7.21256216
, 7.22882839, 7.24571864, 7.27495059, 7.29462926, 7.25890278, 7.25433506
, 7.24603574, 7.25941919, 7.24866794, 7.24826202, 7.26907137, 7.26271668
, 7.19386475, 7.2135492, 7.18648301, 7.21765087, 7.20431988, 7.17971313
, 7.16111695, 7.16658254]
, [7.0628258, 7.0565359, 7.11337205, 7.10550886, 7.13546101, 7.14691697
, 7.15545793, 7.17138645, 7.17957225, 7.19835253, 7.20504838, 7.21609701
, 7.21905797, 7.24038871, 7.27523042, 7.28038123, 7.28185432, 7.26805329
, 7.27523042, 7.26185602, 7.2658306, 7.2599316, 7.2808469, 7.24548964
, 7.22622029, 7.18652345, 7.22539957, 7.20758552, 7.19186268, 7.21529007
, 7.12175286, 7.13741721]
, [7.10538743, 7.13075047, 7.07712634, 7.14604119, 7.14088646, 7.17482072
, 7.16757463, 7.14521748, 7.15822979, 7.16748083, 7.19473179, 7.21372096
, 7.21967155, 7.24233639, 7.27765772, 7.31687845, 7.28883326, 7.2873778
, 7.27057263, 7.29022335, 7.26757084, 7.26082836, 7.25442483, 7.26725716
, 7.22528767, 7.22249693, 7.20775857, 7.21598928, 7.19209682, 7.1941524
, 7.12355221, 7.14561341]
, [7.12638516, 7.12766976, 7.1419693, 7.18031161, 7.1268083, 7.1213374
, 7.16011059, 7.16920489, 7.14311529, 7.18211893, 7.21582985, 7.20727846
, 7.22589803, 7.22438115, 7.25952446, 7.27821024, 7.27631647, 7.270553
, 7.28026839, 7.26237224, 7.25466113, 7.25480068, 7.26478839, 7.256458
, 7.24304346, 7.23680171, 7.23499617, 7.21813954, 7.18005117, 7.15872504
, 7.13015163, 7.15606022]
, [7.09689678, 7.16320804, 7.19255134, 7.23609747, 7.19091654, 7.19019303
, 7.14936121, 7.20369545, 7.18306481, 7.21871275, 7.17806303, 7.21773075
, 7.24543467, 7.22685449, 7.26857438, 7.28084958, 7.26843512, 7.28350373
, 7.27052616, 7.29430339, 7.27974442, 7.28151853, 7.23836196, 7.27082977
, 7.24540795, 7.22132664, 7.19396142, 7.21689201, 7.15199452, 7.18669298
, 7.16576098, 7.12738909]
, [7.08001509, 7.12691068, 7.20087906, 7.18326033, 7.19141428, 7.18789518
, 7.22974408, 7.20517591, 7.21413507, 7.21014682, 7.23320835, 7.25859764
, 7.22708896, 7.22911143, 7.2881316, 7.30723304, 7.25345098, 7.26579669
, 7.28947115, 7.27979888, 7.27651845, 7.26175673, 7.2395462, 7.27118696
, 7.21797323, 7.18891308, 7.20675377, 7.1921164, 7.16371801, 7.11961812
, 7.11831993, 7.17457141]
, [7.07944315, 7.11580304, 7.1418889, 7.17925645, 7.22956939, 7.1959462
, 7.18796638, 7.27497603, 7.24439362, 7.26407731, 7.22702478, 7.26340247
, 7.23449651, 7.29995256, 7.24714052, 7.30356909, 7.2733887, 7.26600182
, 7.27942111, 7.26027987, 7.25041966, 7.23720468, 7.22068841, 7.2611945
, 7.18119149, 7.18150997, 7.15467106, 7.19504459, 7.1447221, 7.16893481
, 7.08705136, 7.14366338]
, [7.12667027, 7.11963731, 7.19111745, 7.17750764, 7.17287662, 7.18347477
, 7.21333327, 7.22745236, 7.20584289, 7.23837332, 7.2285077, 7.25843246
, 7.26659791, 7.21717549, 7.24843322, 7.25164991, 7.25010085, 7.24688706
, 7.24909292, 7.25060806, 7.21718262, 7.2194742, 7.23819051, 7.20326351
, 7.17955392, 7.18993586, 7.16126602, 7.18878054, 7.11470798, 7.15067327
, 7.09334597, 7.1112902]]
)

    def show_HeatmapVid(self):
        plt.ion()
        
        fig, ax = plt.subplots()
        im = ax.imshow(np.subtract(self.imageData, self.backgroundTempDel), interpolation='bicubic', cmap='hot') ##interpolation='bicubic', 

        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("", rotation=-90, va="bottom")

        return fig, im, self.backgroundTempDel


    def show_HeatmapImg(self):     
        fig, ax = plt.subplots()

        plt.axis('off')

        # im = ax.imshow(self.imageData, cmap='hot') #, interpolation='bicubic', cmap='hot') 
        im = ax.imshow(np.subtract(self.imageData, self.backgroundTempDel), interpolation='bicubic', cmap='hot') ##interpolation='bicubic', 

        plt.tight_layout()
        plt.savefig(FIGURE, bbox_inches='tight',pad_inches = 0)
        pd.person_detection(FIGURE).contour_detection()


    def show_HMIntOpt(self):
        methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

        fig, ax = plt.subplots(nrows=3, ncols=6, figsize=(18,12))
        for ax, interp_method in zip(ax.flat, methods):
            ax.imshow(np.subtract(self.imageData, self.backgroundTempDel), interpolation=interp_method, cmap='hot')
            ax.set_title(str(interp_method))

        plt.tight_layout()
        plt.show()