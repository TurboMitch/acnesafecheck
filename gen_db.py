#!/usr/bin/env python3
# Generates checker.js (engine + comedogenicity database, 500+ ingredients).
import json, re

# ---- CORE: rated ingredients (name, rating 0-5, category, [aliases]) ----
CORE = [
 ("Coconut Oil",4,"Oil",["coconut oil","cocos nucifera oil"]),
 ("Coconut Butter",4,"Butter",["coconut butter"]),
 ("Coconut Alkanes",3,"Oil",["coconut alkanes"]),
 ("Cocoa Butter",4,"Butter",["cocoa butter","theobroma cacao seed butter","theobroma cacao"]),
 ("Wheat Germ Oil",5,"Oil",["wheat germ oil","triticum vulgare germ oil"]),
 ("Wheat Germ Glyceride",3,"Oil",["wheat germ glyceride"]),
 ("Cotton Seed Oil",3,"Oil",["cottonseed oil","cotton seed oil","gossypium oil"]),
 ("Soybean Oil",3,"Oil",["soybean oil","glycine soja oil"]),
 ("Linseed / Flaxseed Oil",4,"Oil",["linseed oil","flaxseed oil","linum usitatissimum seed oil"]),
 ("Corn Oil",3,"Oil",["corn oil","zea mays oil"]),
 ("Sesame Oil",3,"Oil",["sesame oil","sesamum indicum seed oil"]),
 ("Avocado Oil",3,"Oil",["avocado oil","persea gratissima oil"]),
 ("Olive Oil",2,"Oil",["olive oil","olea europaea fruit oil"]),
 ("Sweet Almond Oil",2,"Oil",["almond oil","prunus amygdalus dulcis oil","sweet almond oil"]),
 ("Peanut Oil",2,"Oil",["peanut oil","arachis hypogaea oil"]),
 ("Apricot Kernel Oil",2,"Oil",["apricot kernel oil","prunus armeniaca kernel oil"]),
 ("Grapeseed Oil",1,"Oil",["grapeseed oil","grape seed oil","vitis vinifera seed oil"]),
 ("Jojoba Oil",2,"Oil",["jojoba oil","simmondsia chinensis seed oil"]),
 ("Argan Oil",0,"Oil",["argan oil","argania spinosa kernel oil"]),
 ("Hemp Seed Oil",0,"Oil",["hemp seed oil","cannabis sativa seed oil"]),
 ("Rosehip Oil",1,"Oil",["rosehip oil","rosa canina fruit oil","rosehip seed oil"]),
 ("Sunflower Oil",0,"Oil",["sunflower oil","helianthus annuus seed oil"]),
 ("Safflower Oil",0,"Oil",["safflower oil","carthamus tinctorius seed oil"]),
 ("Castor Oil",1,"Oil",["castor oil","ricinus communis seed oil"]),
 ("Hydrogenated Castor Oil",1,"Oil",["hydrogenated castor oil"]),
 ("Marula Oil",1,"Oil",["marula oil","sclerocarya birrea seed oil"]),
 ("Squalane",1,"Oil",["squalane"]),
 ("Squalene",1,"Oil",["squalene"]),
 ("Shark Liver Oil",3,"Oil",["shark liver oil"]),
 ("Mink Oil",3,"Oil",["mink oil"]),
 ("Mineral Oil",1,"Oil",["mineral oil","paraffinum liquidum"]),
 ("Petrolatum",0,"Occlusive",["petrolatum","petroleum jelly"]),
 ("Shea Butter",0,"Butter",["shea butter","butyrospermum parkii butter"]),
 ("Mango Butter",0,"Butter",["mango butter","mangifera indica seed butter"]),
 ("Kokum Butter",1,"Butter",["kokum butter","garcinia indica seed butter"]),
 ("Cupuacu Butter",1,"Butter",["cupuacu butter","theobroma grandiflorum seed butter"]),
 ("Tamanu Oil",2,"Oil",["tamanu oil","calophyllum inophyllum seed oil"]),
 ("Evening Primrose Oil",2,"Oil",["evening primrose oil","oenothera biennis oil"]),
 ("Borage Oil",2,"Oil",["borage oil","borago officinalis seed oil"]),
 ("Camellia / Tsubaki Oil",1,"Oil",["camellia oil","camellia japonica seed oil","tsubaki oil"]),
 ("Meadowfoam Seed Oil",1,"Oil",["meadowfoam seed oil","limnanthes alba seed oil"]),
 ("Pomegranate Seed Oil",1,"Oil",["pomegranate seed oil","punica granatum seed oil"]),
 ("Macadamia Oil",2,"Oil",["macadamia oil","macadamia integrifolia seed oil"]),
 ("Wheat Bran Lipids",2,"Oil",["wheat bran lipids"]),
 # Esters
 ("Isopropyl Myristate",5,"Ester",["isopropyl myristate"]),
 ("Isopropyl Palmitate",4,"Ester",["isopropyl palmitate"]),
 ("Isopropyl Isostearate",5,"Ester",["isopropyl isostearate"]),
 ("Isopropyl Linoleate",5,"Ester",["isopropyl linoleate"]),
 ("Myristyl Myristate",5,"Ester",["myristyl myristate"]),
 ("Myristyl Lactate",4,"Ester",["myristyl lactate"]),
 ("Octyl Palmitate",4,"Ester",["octyl palmitate","ethylhexyl palmitate"]),
 ("Octyl Stearate",5,"Ester",["octyl stearate","ethylhexyl stearate"]),
 ("Isocetyl Stearate",5,"Ester",["isocetyl stearate"]),
 ("Isostearyl Isostearate",4,"Ester",["isostearyl isostearate"]),
 ("Isostearyl Neopentanoate",4,"Ester",["isostearyl neopentanoate"]),
 ("Butyl Stearate",3,"Ester",["butyl stearate"]),
 ("Decyl Oleate",3,"Ester",["decyl oleate"]),
 ("Cetyl Acetate",3,"Ester",["cetyl acetate"]),
 ("Glyceryl Stearate SE",3,"Ester",["glyceryl stearate se"]),
 ("Glyceryl Stearate",1,"Ester",["glyceryl stearate"]),
 ("Glyceryl Oleate",2,"Ester",["glyceryl oleate"]),
 ("PPG-2 Myristyl Ether Propionate",3,"Ester",["ppg-2 myristyl ether propionate"]),
 ("Caprylic/Capric Triglyceride",1,"Ester",["caprylic/capric triglyceride","caprylic capric triglyceride"]),
 ("Cetearyl Ethylhexanoate",1,"Ester",["cetearyl ethylhexanoate"]),
 ("Diisopropyl Adipate",1,"Ester",["diisopropyl adipate"]),
 ("Isononyl Isononanoate",1,"Ester",["isononyl isononanoate"]),
 ("Isohexadecane",1,"Ester",["isohexadecane"]),
 ("Coco-Caprylate",1,"Ester",["coco-caprylate","coco caprylate"]),
 # Fatty acids / alcohols
 ("Lauric Acid",4,"Fatty acid",["lauric acid"]),
 ("Myristic Acid",3,"Fatty acid",["myristic acid"]),
 ("Palmitic Acid",2,"Fatty acid",["palmitic acid"]),
 ("Stearic Acid",2,"Fatty acid",["stearic acid"]),
 ("Oleic Acid",2,"Fatty acid",["oleic acid"]),
 ("Linoleic Acid",0,"Fatty acid",["linoleic acid"]),
 ("Hexadecyl Alcohol",5,"Fatty alcohol",["hexadecyl alcohol"]),
 ("Cetyl Alcohol",2,"Fatty alcohol",["cetyl alcohol"]),
 ("Cetearyl Alcohol",2,"Fatty alcohol",["cetearyl alcohol"]),
 ("Stearyl Alcohol",2,"Fatty alcohol",["stearyl alcohol"]),
 ("Behenyl Alcohol",1,"Fatty alcohol",["behenyl alcohol"]),
 # Emulsifiers / surfactants
 ("Laureth-4",5,"Emulsifier",["laureth-4","laureth 4"]),
 ("Laureth-23",3,"Emulsifier",["laureth-23"]),
 ("Sodium Lauryl Sulfate",5,"Surfactant",["sodium lauryl sulfate","sls"]),
 ("Sodium Laureth Sulfate",3,"Surfactant",["sodium laureth sulfate","sles"]),
 ("PEG-16 Lanolin",4,"Emulsifier",["peg-16 lanolin","peg 16 lanolin"]),
 ("PEG-8 Stearate",3,"Emulsifier",["peg-8 stearate","peg 8 stearate"]),
 ("PEG-100 Stearate",1,"Emulsifier",["peg-100 stearate"]),
 ("PEG-40 Stearate",1,"Emulsifier",["peg-40 stearate"]),
 ("PEG-150 Distearate",1,"Emulsifier",["peg-150 distearate"]),
 ("Steareth-2",2,"Emulsifier",["steareth-2"]),
 ("Steareth-10",4,"Emulsifier",["steareth-10"]),
 ("Steareth-20",2,"Emulsifier",["steareth-20"]),
 ("Ceteareth-20",4,"Emulsifier",["ceteareth-20","cetearyl alcohol ceteareth-20"]),
 ("Ceteareth-25",2,"Emulsifier",["ceteareth-25"]),
 ("Sorbitan Oleate",3,"Emulsifier",["sorbitan oleate"]),
 ("Sorbitan Sesquioleate",3,"Emulsifier",["sorbitan sesquioleate"]),
 ("Sorbitan Stearate",1,"Emulsifier",["sorbitan stearate"]),
 ("Polyglyceryl-3 Diisostearate",4,"Emulsifier",["polyglyceryl-3 diisostearate"]),
 ("Lecithin",4,"Emulsifier",["lecithin"]),
 ("Hydrogenated Lecithin",1,"Emulsifier",["hydrogenated lecithin"]),
 ("Polysorbate 80",1,"Emulsifier",["polysorbate 80"]),
 ("Polysorbate 20",0,"Emulsifier",["polysorbate 20"]),
 ("Cetearyl Glucoside",0,"Emulsifier",["cetearyl glucoside"]),
 ("Coco-Glucoside",0,"Surfactant",["coco-glucoside","coco glucoside"]),
 ("Decyl Glucoside",0,"Surfactant",["decyl glucoside"]),
 ("Cocamidopropyl Betaine",1,"Surfactant",["cocamidopropyl betaine"]),
 # Algae / thickeners / waxes
 ("Algae Extract",5,"Marine",["algae extract","algae"]),
 ("Red Algae",5,"Marine",["red algae"]),
 ("Carrageenan",5,"Thickener",["carrageenan","chondrus crispus"]),
 ("Algin",4,"Thickener",["algin"]),
 ("Laminaria Digitata Extract",4,"Marine",["laminaria digitata extract"]),
 ("Xanthan Gum",0,"Thickener",["xanthan gum"]),
 ("Carbomer",0,"Thickener",["carbomer"]),
 ("Hydroxyethylcellulose",0,"Thickener",["hydroxyethylcellulose"]),
 ("Sclerotium Gum",0,"Thickener",["sclerotium gum"]),
 ("Beeswax",2,"Wax",["beeswax","cera alba"]),
 ("Candelilla Wax",1,"Wax",["candelilla wax","euphorbia cerifera wax"]),
 ("Carnauba Wax",1,"Wax",["carnauba wax","copernicia cerifera wax"]),
 ("Lanolin",2,"Occlusive",["lanolin"]),
 ("Acetylated Lanolin",4,"Occlusive",["acetylated lanolin"]),
 ("Acetylated Lanolin Alcohol",4,"Occlusive",["acetylated lanolin alcohol"]),
 ("Lanolin Alcohol",2,"Occlusive",["lanolin alcohol"]),
 # Dyes
 ("D&C Red 6",3,"Colorant",["d&c red 6","red 6","ci 15850"]),
 ("D&C Red 7",3,"Colorant",["d&c red 7","red 7"]),
 ("D&C Red 9",3,"Colorant",["d&c red 9","red 9"]),
 ("D&C Red 17",3,"Colorant",["d&c red 17","red 17"]),
 ("D&C Red 21",3,"Colorant",["d&c red 21","red 21"]),
 ("D&C Red 27",2,"Colorant",["d&c red 27","red 27"]),
 ("D&C Red 30",3,"Colorant",["d&c red 30","red 30"]),
 ("D&C Red 33",2,"Colorant",["d&c red 33","red 33"]),
 ("D&C Red 36",3,"Colorant",["d&c red 36","red 36"]),
 ("Iron Oxides",0,"Colorant",["iron oxides","ci 77491","ci 77492","ci 77499"]),
 ("Titanium Dioxide",1,"Sunscreen",["titanium dioxide","ci 77891"]),
 ("Mica",0,"Colorant",["mica","ci 77019"]),
 # Silicones
 ("Dimethicone",1,"Silicone",["dimethicone"]),
 ("Cyclopentasiloxane",0,"Silicone",["cyclopentasiloxane"]),
 ("Cyclomethicone",0,"Silicone",["cyclomethicone"]),
 ("Cyclohexasiloxane",0,"Silicone",["cyclohexasiloxane"]),
 ("Dimethicone Crosspolymer",1,"Silicone",["dimethicone crosspolymer"]),
 ("Phenyl Trimethicone",1,"Silicone",["phenyl trimethicone"]),
 ("Amodimethicone",1,"Silicone",["amodimethicone"]),
 # Humectants
 ("Glycerin",0,"Humectant",["glycerin","glycerine","glycerol"]),
 ("Hyaluronic Acid",0,"Humectant",["hyaluronic acid","sodium hyaluronate"]),
 ("Propylene Glycol",0,"Humectant",["propylene glycol"]),
 ("Butylene Glycol",0,"Humectant",["butylene glycol"]),
 ("Pentylene Glycol",0,"Humectant",["pentylene glycol"]),
 ("Sodium PCA",0,"Humectant",["sodium pca"]),
 ("Urea",0,"Humectant",["urea"]),
 ("Betaine",0,"Humectant",["betaine"]),
 ("Glycereth-26",0,"Humectant",["glycereth-26"]),
 ("Sorbitol",0,"Humectant",["sorbitol"]),
 ("Trehalose",0,"Humectant",["trehalose"]),
 ("Panthenol",0,"Soothing",["panthenol","provitamin b5"]),
 ("Allantoin",0,"Soothing",["allantoin"]),
 # Actives
 ("Niacinamide",0,"Active",["niacinamide","vitamin b3","nicotinamide"]),
 ("Salicylic Acid",0,"Active",["salicylic acid","bha"]),
 ("Glycolic Acid",0,"Active",["glycolic acid"]),
 ("Lactic Acid",0,"Active",["lactic acid"]),
 ("Mandelic Acid",0,"Active",["mandelic acid"]),
 ("Azelaic Acid",0,"Active",["azelaic acid"]),
 ("Retinol",1,"Active",["retinol"]),
 ("Retinyl Palmitate",2,"Active",["retinyl palmitate"]),
 ("Bakuchiol",0,"Active",["bakuchiol"]),
 ("Ascorbic Acid",0,"Active",["ascorbic acid","vitamin c"]),
 ("Magnesium Ascorbyl Phosphate",0,"Active",["magnesium ascorbyl phosphate"]),
 ("Tetrahexyldecyl Ascorbate",2,"Active",["tetrahexyldecyl ascorbate"]),
 ("Tocopherol",2,"Active",["tocopherol","tocopheryl acetate","vitamin e"]),
 ("Benzoyl Peroxide",0,"Active",["benzoyl peroxide"]),
 ("Adapalene",0,"Active",["adapalene"]),
 ("Zinc Oxide",1,"Sunscreen",["zinc oxide"]),
 ("Avobenzone",0,"Sunscreen",["avobenzone","butyl methoxydibenzoylmethane"]),
 ("Octocrylene",1,"Sunscreen",["octocrylene"]),
 ("Homosalate",1,"Sunscreen",["homosalate"]),
 ("Octinoxate",1,"Sunscreen",["octinoxate","ethylhexyl methoxycinnamate"]),
 # Essential oils / fragrance
 ("Spearmint Oil",3,"Essential oil",["spearmint oil","mentha viridis leaf oil"]),
 ("Peppermint Oil",2,"Essential oil",["peppermint oil","mentha piperita oil"]),
 ("Tea Tree Oil",1,"Essential oil",["tea tree oil","melaleuca alternifolia leaf oil"]),
 ("Lavender Oil",1,"Essential oil",["lavender oil","lavandula angustifolia oil"]),
 ("Fragrance",1,"Fragrance",["fragrance","parfum"]),
 ("Limonene",1,"Fragrance",["limonene"]),
 ("Linalool",1,"Fragrance",["linalool"]),
 # Misc / minerals / solvents
 ("Sodium Chloride",0,"Misc",["sodium chloride","sea salt"]),
 ("Water",0,"Solvent",["water","aqua","eau"]),
 ("Alcohol Denat.",0,"Solvent",["alcohol denat","alcohol denat.","denatured alcohol"]),
 ("Talc",1,"Mineral",["talc"]),
 ("Kaolin",0,"Clay",["kaolin"]),
 ("Bentonite",0,"Clay",["bentonite"]),
 ("Silica",0,"Mineral",["silica"]),
 ("Colloidal Oatmeal",0,"Soothing",["colloidal oatmeal"]),
 ("Charcoal",0,"Misc",["charcoal","activated charcoal"]),
]

# ---- BOTANICAL EXTRACTS: non-comedogenic (rating 0) ----
EXTRACTS = [
 "Aloe Barbadensis Leaf Juice","Aloe Vera","Green Tea Extract","Camellia Sinensis Leaf Extract",
 "Centella Asiatica Extract","Cica","Chamomile Extract","Chamomilla Recutita Flower Extract",
 "Calendula Officinalis Flower Extract","Cucumber Extract","Cucumis Sativus Fruit Extract",
 "Witch Hazel","Hamamelis Virginiana Water","Licorice Root Extract","Glycyrrhiza Glabra Root Extract",
 "Ginseng Extract","Panax Ginseng Root Extract","Ginkgo Biloba Leaf Extract","Rosemary Extract",
 "Rosmarinus Officinalis Leaf Extract","Sage Extract","Salvia Officinalis Leaf Extract",
 "Thyme Extract","Nettle Extract","Urtica Dioica Extract","Burdock Root Extract","Echinacea Extract",
 "Horsetail Extract","Equisetum Arvense Extract","Marshmallow Root Extract","Comfrey Extract",
 "Elderflower Extract","Sambucus Nigra Flower Extract","Hibiscus Extract","Lavender Extract",
 "Lavandula Angustifolia Flower Extract","Rose Extract","Rosa Damascena Flower Extract",
 "Rose Water","Jasmine Extract","Neroli Extract","Orange Blossom Water","Lemon Peel Extract",
 "Citrus Limon Peel Extract","Grapefruit Extract","Bergamot Extract","Mandarin Orange Extract",
 "Bilberry Extract","Vaccinium Myrtillus Fruit Extract","Blueberry Extract","Raspberry Extract",
 "Strawberry Extract","Blackberry Extract","Cranberry Extract","Acai Extract","Goji Berry Extract",
 "Pomegranate Extract","Punica Granatum Extract","Grape Extract","Vitis Vinifera Fruit Extract",
 "Apple Extract","Pyrus Malus Fruit Extract","Pear Extract","Peach Extract","Apricot Extract",
 "Papaya Extract","Carica Papaya Fruit Extract","Pineapple Extract","Mango Extract","Banana Extract",
 "Watermelon Extract","Lemon Balm Extract","Melissa Officinalis Leaf Extract","Peppermint Leaf Extract",
 "Spearmint Leaf Extract","Basil Extract","Oregano Extract","Fennel Extract","Dill Extract",
 "Parsley Extract","Cilantro Extract","Ginger Root Extract","Zingiber Officinale Root Extract",
 "Turmeric Extract","Curcuma Longa Root Extract","Cinnamon Extract","Clove Extract","Cardamom Extract",
 "Vanilla Extract","Cocoa Extract","Coffee Extract","Coffea Arabica Seed Extract","Matcha Extract",
 "White Tea Extract","Black Tea Extract","Rooibos Extract","Hops Extract","Barley Extract",
 "Oat Extract","Avena Sativa Kernel Extract","Rice Extract","Oryza Sativa Bran Extract",
 "Soy Extract","Glycine Soja Seed Extract","Wheat Protein","Hydrolyzed Wheat Protein",
 "Silk Protein","Hydrolyzed Silk","Collagen","Hydrolyzed Collagen","Elastin","Keratin",
 "Sea Kelp Extract","Spirulina Extract","Chlorella Extract","Sea Salt Extract","Seawater",
 "Bamboo Extract","Bambusa Vulgaris Extract","Aloe Ferox Leaf Extract","Cactus Extract",
 "Opuntia Ficus-Indica Extract","Snow Mushroom Extract","Tremella Fuciformis Extract",
 "Reishi Mushroom Extract","Shiitake Extract","Mushroom Extract","Yeast Extract",
 "Saccharomyces Ferment","Galactomyces Ferment Filtrate","Bifida Ferment Lysate",
 "Lactobacillus Ferment","Fermented Rice Water","Willow Bark Extract","Salix Alba Bark Extract",
 "Birch Extract","Pine Bark Extract","Pinus Pinaster Bark Extract","Maritime Pine Extract",
 "Oak Bark Extract","Cedarwood Extract","Eucalyptus Extract","Sandalwood Extract",
 "Frankincense Extract","Boswellia Serrata Extract","Myrrh Extract","Aloe Extract",
 "Mallow Extract","Linden Extract","Cornflower Extract","Centaurea Cyanus Flower Water",
 "Helichrysum Extract","Arnica Extract","Arnica Montana Flower Extract","St. Johns Wort Extract",
 "Gotu Kola Extract","Tiger Grass Extract","Madecassoside","Asiaticoside","Allium Cepa Extract",
 "Garlic Extract","Cucurbita Pepo Seed Extract","Pumpkin Extract","Carrot Extract",
 "Daucus Carota Sativa Root Extract","Tomato Extract","Solanum Lycopersicum Fruit Extract",
 "Beetroot Extract","Spinach Extract","Kale Extract","Broccoli Extract","Celery Extract",
 "Cabbage Extract","Lettuce Extract","Artichoke Leaf Extract","Asparagus Extract",
 "Mugwort Extract","Artemisia Vulgaris Extract","Houttuynia Cordata Extract","Heartleaf Extract",
 "Snail Secretion Filtrate","Propolis Extract","Royal Jelly Extract","Honey Extract","Manuka Honey",
 "Aloe Powder","Caffeine","Resveratrol","Ferulic Acid","Ectoin","Beta-Glucan","Allantoin Extract",
 "Lotus Extract","Nelumbo Nucifera Flower Extract","Camellia Japonica Leaf Extract","Yarrow Extract",
 "Dandelion Extract","Taraxacum Officinale Extract","Plantain Extract","Cleavers Extract",
 "Red Clover Extract","Chickweed Extract","Calendula Extract","Marigold Extract","Daisy Extract",
 "Edelweiss Extract","Leontopodium Alpinum Extract","Sea Buckthorn Extract","Hippophae Rhamnoides Extract",
 "Baobab Extract","Adansonia Digitata Extract","Moringa Extract","Neem Extract","Azadirachta Indica Extract",
 "Amla Extract","Shikakai Extract","Brahmi Extract","Ashwagandha Extract","Holy Basil Extract",
 "Cha de Bugre Extract","Guarana Extract","Yerba Mate Extract","Mate Leaf Extract","Hawthorn Extract",
 "Olive Leaf Extract","Olea Europaea Leaf Extract","Fig Extract","Date Extract","Aloe Juice Powder",
]

# ---- FUNCTIONAL: preservatives, peptides, pH adjusters, etc. (rating 0) ----
FUNCTIONAL = [
 "Phenoxyethanol","Ethylhexylglycerin","Caprylyl Glycol","Sodium Benzoate","Potassium Sorbate",
 "Benzyl Alcohol","Dehydroacetic Acid","Chlorphenesin","Sorbic Acid","Methylparaben","Propylparaben",
 "Sodium Hydroxide","Citric Acid","Sodium Citrate","Lactic Acid Bacteria","Triethanolamine",
 "Aminomethyl Propanol","Tetrasodium EDTA","Disodium EDTA","Tetrasodium Glutamate Diacetate",
 "Sodium Phytate","Phytic Acid","Sodium Metabisulfite","Sodium Sulfite","BHT","BHA Preservative",
 "Tocopheryl Acetate","Sodium Ascorbyl Phosphate","Ascorbyl Glucoside","Ascorbyl Palmitate",
 "Copper Tripeptide-1","Palmitoyl Tripeptide-1","Palmitoyl Tripeptide-5","Palmitoyl Pentapeptide-4",
 "Acetyl Hexapeptide-8","Argireline","Matrixyl","Palmitoyl Hexapeptide-12","Tripeptide-1",
 "Hexapeptide-9","Oligopeptide-1","Copper PCA","Zinc PCA","Zinc Gluconate","Zinc Sulfate",
 "Magnesium Sulfate","Magnesium Chloride","Potassium Chloride","Calcium Chloride","Manganese PCA",
 "Sodium Lactate","Ammonium Lactate","Sodium Hyaluronate Crosspolymer","Hydrolyzed Hyaluronic Acid",
 "Sodium Acetylated Hyaluronate","Hydroxypropyl Cyclodextrin","Polyglutamic Acid","Sodium Polyglutamate",
 "Inositol","Adenosine","Carnosine","Glutathione","N-Acetyl Glucosamine","Acetyl Glucosamine",
 "Ergothioneine","Coenzyme Q10","Ubiquinone","Idebenone","Alpha Lipoic Acid","Pyridoxine",
 "Biotin","Folic Acid","Riboflavin","Thiamine","Cyanocobalamin","Calcium Pantothenate",
 "PCA","Lactobionic Acid","Gluconolactone","Polyhydroxy Acid","Tartaric Acid","Malic Acid",
 "Phytic Acid Complex","Kojic Acid","Arbutin","Alpha-Arbutin","Tranexamic Acid","Ferulate",
 "Sodium Cocoyl Isethionate","Sodium Cocoyl Glycinate","Disodium Cocoamphodiacetate",
 "Lauryl Glucoside","Sodium Methyl Cocoyl Taurate","Sodium Lauroyl Sarcosinate","Sodium Lauroyl Lactylate",
 "Glyceryl Caprylate","Glyceryl Undecylenate","Levulinic Acid","Sodium Levulinate","Anisic Acid",
 "p-Anisic Acid","Sodium Anisate","Caprylhydroxamic Acid","Propanediol","Methylpropanediol",
 "Dipropylene Glycol","Hexylene Glycol","Isopentyldiol","Ethanol","Isopropyl Alcohol",
 "Polyacrylate Crosspolymer-6","Acrylates/C10-30 Alkyl Acrylate Crosspolymer","Polyquaternium-10",
 "Guar Hydroxypropyltrimonium Chloride","Hydroxypropyl Guar","Cellulose Gum","Agar","Gellan Gum",
 "Pullulan","Maltodextrin","Inulin","Cyclodextrin","Trisodium Ethylenediamine Disuccinate",
 "Sodium Gluconate","Glucose","Fructose","Sucrose","Sodium Starch Octenylsuccinate",
 "Tapioca Starch","Corn Starch","Aluminum Starch Octenylsuccinate","Boron Nitride",
 "Calcium Carbonate","Magnesium Stearate","Zinc Stearate","Hydrated Silica","Perlite",
 "Sodium Silicate","Polymethylsilsesquioxane","Nylon-12","Polyethylene","HDI/Trimethylol Hexyllactone Crosspolymer",
]

def aliases_for(name):
    a = {name.lower()}
    # strip trailing descriptors that don't change identity
    a.add(re.sub(r"\s*\(.*?\)\s*", " ", name).strip().lower())
    return [x for x in a if x]

entries = {}
def add(name, r, cat, al):
    key = name
    if key in entries: return
    entries[key] = {"n": name, "r": r, "c": cat, "a": sorted(set(a.lower() for a in al))}

for name, r, cat, al in CORE:
    add(name, r, cat, al)
for name in EXTRACTS:
    add(name, 0, "Botanical extract", aliases_for(name))
for name in FUNCTIONAL:
    add(name, 0, "Functional", aliases_for(name))

def slugify(n):
    return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
_seen_slugs = {}
for e in entries.values():
    base = slugify(e["n"]); s = base; i = 2
    while s in _seen_slugs:
        s = f"{base}-{i}"; i += 1
    _seen_slugs[s] = True; e["s"] = s

# Fungal-acne (Malassezia) trigger flag. General guidance: Malassezia feeds on fatty acids C11-C24,
# many esters, polysorbates and fermented ingredients. Hydrocarbons (squalane, mineral oil) are safe.
FA_TRIGGER_CATS = {"Oil", "Butter", "Ester", "Fatty acid", "Fatty alcohol"}
FA_SAFE_OVERRIDE = {"Squalane", "Squalene", "Mineral Oil", "Petrolatum", "Caprylic/Capric Triglyceride",
                    "Coconut Alkanes", "Isohexadecane"}
FA_TRIGGER_SUBSTR = ("stearate", "oleate", "laurate", "laureth", "steareth", "ceteareth", "sorbitan",
                     "polysorbate", "lecithin", "ferment", "tocopher", "myristate", "palmitate", "isostearate")
def fa_trigger(e):
    if e["n"] in FA_SAFE_OVERRIDE: return False
    if e["c"] in FA_TRIGGER_CATS: return True
    n = e["n"].lower()
    return any(sub in n for sub in FA_TRIGGER_SUBSTR)
for e in entries.values():
    e["fa"] = fa_trigger(e)

DB = sorted(entries.values(), key=lambda x: (-x["r"], x["n"]))
db_json = "[\n" + ",\n".join("  " + json.dumps(e, ensure_ascii=False) for e in DB) + "\n]"
json.dump(DB, open("db.json", "w"), ensure_ascii=False)

ENGINE = r'''
const lookup = {};
DB.forEach(item => item.a.forEach(al => lookup[al] = item));
function normalize(s){return s.toLowerCase().replace(/\([^)]*\)/g,' ').replace(/[^a-z0-9&/\-\s]/g,' ').replace(/\s+/g,' ').trim();}
function parseList(raw){return raw.split(/[,;\n•·]+/).map(x=>x.trim()).filter(Boolean);}
function match(token){
  const norm = normalize(token);
  if(lookup[norm]) return lookup[norm];
  for(const al in lookup){ if(norm === al) return lookup[al]; }
  for(const al in lookup){ if(al.length>5 && norm.includes(al)) return lookup[al]; }
  return null;
}
function pill(r){
  if(r>=3) return '<span class="pill bad">Clogging risk · '+r+'/5</span>';
  if(r>=1) return '<span class="pill low">Low risk · '+r+'/5</span>';
  return '<span class="pill safe">Acne safe · 0/5</span>';
}
function riskText(r){
  if(r>=4) return 'High likelihood of clogging pores — a common breakout trigger for acne-prone skin.';
  if(r===3) return 'Moderate pore-clogging potential; many acne-prone people avoid this.';
  if(r===2) return 'Mild — usually fine, but sensitive skin may want to patch test.';
  if(r===1) return 'Very low risk of clogging pores.';
  return 'Considered non-comedogenic.';
}
function escapeHtml(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function checkIngredients(){
  const ta = document.getElementById('ingredients'); const res = document.getElementById('results');
  if(!ta || !res) return; const raw = ta.value;
  if(!raw.trim()){ res.classList.add('hidden'); return; }
  const tokens = parseList(raw); const bad=[], low=[], safe=[], unknown=[]; const seen = new Set();
  tokens.forEach(t=>{ const m = match(t);
    if(m){ if(seen.has(m.n)) return; seen.add(m.n); if(m.r>=3) bad.push(m); else if(m.r>=1) low.push(m); else safe.push(m); }
    else { const key=normalize(t); if(key && !seen.has(key)){ seen.add(key); unknown.push(t.trim()); } } });
  let cls='ok', headline='Looks acne safe', sub='No high-risk pore-clogging ingredients found.';
  if(bad.length){ cls='bad'; headline=bad.length+' pore-clogging ingredient'+(bad.length>1?'s':'')+' found'; sub='These have a comedogenicity rating of 3 or higher.'; }
  else if(low.length){ cls='warn'; headline='Mostly fine — '+low.length+' low-risk ingredient'+(low.length>1?'s':''); sub='Nothing high-risk, but a few mild ones to watch.'; }
  let html = '<div class="score '+cls+'"><div class="big">'+(bad.length||low.length||'✓')+'</div><div><div class="lbl"><strong>'+headline+'</strong></div><div class="muted" style="font-size:13px">'+sub+'</div></div></div>';
  const section = (title, arr) => { if(!arr.length) return ''; let s = '<h3 style="margin:18px 0 4px;font-size:15px">'+title+'</h3>';
    arr.sort((a,b)=>b.r-a.r).forEach(m=>{ s += '<div class="flag"><div><div class="name">'+m.n+'</div><div class="why">'+riskText(m.r)+'</div></div>'+pill(m.r)+'</div>'; }); return s; };
  html += section('🔴 Pore-clogging risk', bad); html += section('🟡 Low risk', low); html += section('🟢 Acne safe', safe);
  if(unknown.length){ html += '<h3 style="margin:18px 0 4px;font-size:15px">⚪ Not in database ('+unknown.length+')</h3>';
    html += '<p class="muted" style="font-size:13px">Not on common pore-clogging lists — not necessarily safe or unsafe: '+unknown.map(u=>escapeHtml(u)).join(', ')+'</p>'; }
  res.innerHTML = html; res.classList.remove('hidden'); res.scrollIntoView({behavior:'smooth', block:'start'});
}
function clearAll(){const ta=document.getElementById('ingredients');if(ta)ta.value='';const r=document.getElementById('results');if(r)r.classList.add('hidden');}
function loadSample(){ const ta=document.getElementById('ingredients'); if(!ta) return;
  ta.value="Water, Glycerin, Coconut Oil, Niacinamide, Isopropyl Myristate, Cocoa Butter, Hyaluronic Acid, Squalane, Cetyl Alcohol, Tocopherol, Algae Extract, Fragrance"; checkIngredients(); }
function checkFungal(){
  const ta = document.getElementById('ingredients'); const res = document.getElementById('results');
  if(!ta || !res) return; const raw = ta.value; if(!raw.trim()){ res.classList.add('hidden'); return; }
  const tokens = parseList(raw); const bad=[], safe=[], unknown=[]; const seen=new Set();
  tokens.forEach(t=>{ const m=match(t);
    if(m){ if(seen.has(m.n)) return; seen.add(m.n); if(m.fa) bad.push(m); else safe.push(m); }
    else { const k=normalize(t); if(k && !seen.has(k)){ seen.add(k); unknown.push(t.trim()); } } });
  const cls = bad.length ? 'bad' : 'ok';
  const headline = bad.length ? (bad.length+' possible fungal-acne trigger'+(bad.length>1?'s':'')+' found') : 'No common fungal-acne triggers found';
  const sub = bad.length ? 'These can feed Malassezia yeast (fatty acids C11–C24, many esters, polysorbates, ferments).' : 'No ingredients on common Malassezia-trigger lists.';
  let html = '<div class="score '+cls+'"><div class="big">'+(bad.length||'✓')+'</div><div><div class="lbl"><strong>'+headline+'</strong></div><div class="muted" style="font-size:13px">'+sub+'</div></div></div>';
  const section = (title, arr, trig) => { if(!arr.length) return ''; let s='<h3 style="margin:18px 0 4px;font-size:15px">'+title+'</h3>';
    arr.sort((a,b)=>a.n.localeCompare(b.n)).forEach(m=>{ s+='<div class="flag"><div><div class="name">'+m.n+'</div><div class="why">'+(trig?'Can feed Malassezia — avoid if you have fungal acne.':'Not a common fungal-acne trigger.')+'</div></div>'+(trig?'<span class="pill bad">FA trigger</span>':'<span class="pill safe">FA safe</span>')+'</div>'; }); return s; };
  html += section('🔴 Possible fungal-acne triggers', bad, true);
  html += section('🟢 Fungal-acne safe', safe, false);
  if(unknown.length){ html += '<h3 style="margin:18px 0 4px;font-size:15px">⚪ Not in database ('+unknown.length+')</h3><p class="muted" style="font-size:13px">'+unknown.map(u=>escapeHtml(u)).join(', ')+'</p>'; }
  res.innerHTML = html; res.classList.remove('hidden'); res.scrollIntoView({behavior:'smooth', block:'start'});
}
function renderTable(){ const tb = document.getElementById('dbtable'); if(!tb) return;
  const rows = DB.slice().sort((a,b)=> b.r-a.r || a.n.localeCompare(b.n));
  tb.innerHTML = rows.map(m=>'<tr data-name="'+m.n.toLowerCase()+'"><td><a href="/ingredient/'+m.s+'.html">'+m.n+'</a></td><td>'+m.c+'</td><td>'+pill(m.r)+'</td></tr>').join('');
  const c=document.getElementById('count'); if(c) c.textContent = DB.length; }
function filterTable(){ const q = document.getElementById('dbsearch').value.toLowerCase();
  document.querySelectorAll('#dbtable tr').forEach(tr=>{ tr.style.display = tr.getAttribute('data-name').includes(q) ? '' : 'none'; }); }
'''

out = "/* AcneSafeCheck — comedogenicity engine + database (auto-generated). rating 0..5. */\n"
out += "const DB = " + db_json + ";\n" + ENGINE
with open("checker.js","w") as f:
    f.write(out)
print("DB entries:", len(DB))

# Server-render the ingredient table into the list page so crawlers/AI see content without JS
import re as _re
def _pill(r):
    if r>=3: return f'<span class="pill bad">Clogging risk · {r}/5</span>'
    if r>=1: return f'<span class="pill low">Low risk · {r}/5</span>'
    return '<span class="pill safe">Acne safe · 0/5</span>'
_rows = sorted(DB, key=lambda x: (-x["r"], x["n"]))
_rows_html = "".join(
    f'<tr data-name="{e["n"].lower()}"><td><a href="/ingredient/{e["s"]}.html">{e["n"]}</a></td><td>{e["c"]}</td><td>{_pill(e["r"])}</td></tr>'
    for e in _rows
)
_p = "comedogenic-ingredients-list.html"
_h = open(_p, encoding="utf-8").read()
_h = _re.sub(r'<tbody id="dbtable">.*?</tbody>', '<tbody id="dbtable">' + _rows_html + '</tbody>', _h, flags=_re.S)
_h = _re.sub(r'<span id="count">[^<]*</span>', f'<span id="count">{len(DB)}</span>', _h)
open(_p, "w", encoding="utf-8").write(_h)
print("Injected", len(DB), "static rows into", _p)
