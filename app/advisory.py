"""Disease-aware screening follow-up guidance for the LeafCheck demo.

The classifier supplies a crop/disease class, not lesion localization or a
confirmed diagnosis. Wording below is therefore phrased as signs to compare
and practical IPM actions, with pesticide decisions referred to local labels
and agricultural advisers.
"""


_SOURCES = {
    "plant_diseases": ("UC IPM plant disease guides", "https://ipm.ucanr.edu/PMG/diseases/diseaseslist.html"),
    "tomato": ("Penn State: tomato diseases and disorders", "https://extension.psu.edu/tomato-diseases-and-disorders-in-the-home-garden"),
    "bacterial_spot": ("University of Minnesota Extension: bacterial spot", "https://extension.umn.edu/agriculture/specialty-crops/vegetable-farming/disease-management/bacterial-spot-of-tomato-and-pepper"),
    "early_blight": ("University of Minnesota Extension: early blight", "https://extension.umn.edu/agriculture/specialty-crops/vegetable-farming/disease-management/early-blight-in-tomato-and-potato"),
    "late_blight": ("University of Minnesota Extension: late blight", "https://extension.umn.edu/agriculture/specialty-crops/vegetable-farming/disease-management/late-blight"),
    "strawberry_scorch": ("UC IPM: strawberry leaf scorch", "https://ipm.ucanr.edu/home-and-landscape/leaf-scorch-of-strawberries/"),
    "citrus_hlb": ("UC IPM: citrus greening and psyllid", "https://ipm.ucanr.edu/agriculture/citrus/asian-citrus-psyllid/"),
    "grape_esca": ("UC IPM: grape Esca (black measles)", "https://ipm.ucanr.edu/agriculture/grape/esca-black-measles/"),
    "apple_scab": ("UC IPM: apple scab", "https://ipm.ucanr.edu/agriculture/apple/apple-scab/"),
    "rust": ("UC IPM: cedar and apple rusts", "https://ipm.ucanr.edu/home-and-landscape/cedar-cypress-and-juniper-rusts/"),
    "mites": ("University of Minnesota Extension: spider mites", "https://extension.umn.edu/garden-and-home/yard-and-garden/yard-and-garden-insects/spider-mites"),
    "mildew": ("Penn State Extension: powdery and downy mildew", "https://extension.psu.edu/addressing-downy-mildew-and-powdery-mildew-in-the-home-garden"),
    "pesticide_labels": ("India: PPQS registered pesticide products", "https://ppqs.gov.in/divisions/cib-rc/registered-products"),
    "pesticide_safety": ("India: PPQS registered pesticide products", "https://ppqs.gov.in/divisions/cib-rc/registered-products"),
}


_PROFILES = {
    "applescab": {
        "type": "Fungal leaf and fruit disease",
        "what": "Apple scab is a fungal disease that can affect apple leaves, fruit, and sometimes young shoots. Infection risk rises when susceptible tissue stays wet during mild weather.",
        "signs": ["Look for olive-brown to dark, slightly velvety spots on leaves; young leaves may pucker or twist.", "Fruit may develop rough, dark scab-like patches or become misshapen."],
        "spread": "The fungus survives in infected fallen leaves; spring rain releases spores, and repeated wet periods can start new infections.",
        "first_steps": ["Check several leaves and fruit across the tree, including new growth; photograph both leaf surfaces.", "Collect fallen infected leaves and remove them from beneath the canopy.", "Water at soil level and prune only as needed for airflow; avoid making large cuts during wet weather."],
        "prevention": ["Clear fallen leaves after the season and keep the canopy open.", "Choose a locally recommended scab-resistant variety when replacing a tree.", "Keep a simple record of wet weather and new symptoms."],
        "watch": "Rapid leaf drop, widespread fruit spotting, or symptoms returning each spring warrant a local orchard adviser’s review.",
        "source_keys": ["apple_scab", "pesticide_safety"],
    },
    "appleblackrot": {
        "type": "Fungal disease",
        "what": "Apple black rot is a fungal disease that can affect leaves, branches, and fruit. It may also be associated with dead or cankered wood, so inspect the whole tree rather than one leaf alone.",
        "signs": ["Leaf spots may have a tan center with a darker margin.", "Fruit can develop a brown, expanding rot; dead twigs or sunken bark areas may occur."],
        "spread": "Infected or dead wood and dried, shriveled fruit can carry the fungus between seasons; wounds and wet weather can contribute to infection.",
        "first_steps": ["Inspect fruit, dead twigs, and trunk/branch bark for cankers; take overview and close-up photos.", "Remove fallen or mummified fruit and dead material where practical; bag and discard rather than leaving it under the tree.", "Avoid pruning wet plants and clean tools between trees."],
        "prevention": ["Prune dead wood during a dry period using sound pruning practice.", "Reduce tree stress with appropriate watering and avoid bark injuries.", "Ask an orchard adviser to check any expanding canker before cutting major limbs."],
        "watch": "A spreading canker, branch dieback, or repeated fruit rot needs prompt in-person assessment.",
        "source_keys": ["plant_diseases", "pesticide_safety"],
    },
    "cedarapplerust": {
        "type": "Fungal rust disease",
        "what": "Cedar-apple rust is a rust fungus that alternates between apple-family trees and certain junipers/cedars. A leaf result alone cannot confirm which rust species is present.",
        "signs": ["Compare for bright orange or yellow-orange spots on the upper leaf surface.", "Later in the season, small tube-like structures may form on the underside of affected apple leaves."],
        "spread": "Rust spores move between susceptible hosts; weather and nearby alternate-host plants affect local risk.",
        "first_steps": ["Check multiple leaves and nearby apple-family trees; photograph spots on both sides.", "Do not remove a nearby tree based only on this AI result.", "Record whether symptoms are limited to a few leaves or recurring across the canopy."],
        "prevention": ["Use resistant apple varieties where locally suitable.", "Remove fallen infected leaves and maintain a healthy, open canopy.", "Ask local extension whether alternate-host management is useful in your area."],
        "watch": "Severe yearly defoliation or fruit lesions should be reviewed by an orchard adviser; many rust infections on apple are limited in impact.",
        "source_keys": ["rust", "pesticide_safety"],
    },
    "cherrypowderymildew": {
        "type": "Fungal disease",
        "what": "Powdery mildew is a fungal disease that grows on leaf surfaces and can distort new growth. Conditions that favor it vary by crop and local climate.",
        "signs": ["Look for pale, powder-like patches on leaves or shoots.", "Young leaves may curl, narrow, or become distorted."],
        "spread": "The pathogen can spread from infected growth by spores; dense canopies and susceptible new tissue can increase risk.",
        "first_steps": ["Inspect the top and underside of several leaves and check whether the white material rubs off.", "Remove a small amount of badly affected material only if the plant can tolerate it; avoid stripping the canopy.", "Improve airflow and avoid overhead watering late in the day."],
        "prevention": ["Space/prune plants for airflow and remove infected debris after the season.", "Choose resistant varieties where available and monitor tender new growth."],
        "watch": "Widespread distortion, fruit injury, or a diagnosis that does not match powdery patches should be checked by a horticulture adviser.",
        "source_keys": ["mildew", "pesticide_safety"],
    },
    "cercosporaleafspotgrayleafspot": {
        "type": "Fungal leaf disease",
        "what": "Corn gray leaf spot is a fungal leaf disease that can reduce green leaf area, especially in susceptible hybrids and humid, dense stands.",
        "signs": ["Check for long, narrow tan-to-gray lesions with roughly parallel sides that are limited by leaf veins.", "Lesions can merge on older leaves as disease advances."],
        "spread": "The fungus can persist in crop residue; spores spread within a canopy when conditions are humid and leaves remain wet.",
        "first_steps": ["Walk several rows and note how high symptoms have moved in the canopy and whether lesions are increasing.", "Photograph lesions alongside the leaf veins and note the hybrid and crop stage.", "Avoid making an application decision from a single leaf or image result."],
        "prevention": ["Use locally adapted resistant/tolerant hybrids where available.", "Use rotation and residue practices recommended for your field; maintain balanced fertility and avoid unnecessary canopy density."],
        "watch": "If lesions are moving onto upper leaves before grain fill or the crop is losing green leaf area quickly, ask an agronomist to scout the field and calculate whether treatment is worthwhile.",
        "source_keys": ["plant_diseases", "pesticide_safety"],
    },
    "commonrust": {
        "type": "Fungal rust disease",
        "what": "Corn common rust is a fungal disease that forms spore-producing pustules on leaves. Its impact depends on hybrid susceptibility, crop stage, and how much leaf area is affected.",
        "signs": ["Look for raised rust-colored pustules on both leaf surfaces; gently inspect without rubbing spores into healthy plants.", "Compare the number of affected leaves and whether upper canopy leaves are involved."],
        "spread": "Windborne spores can move between plants and fields; cool-to-mild, humid weather can favor infection.",
        "first_steps": ["Scout more than one row and several plants; record crop stage and the percentage of leaves affected.", "Check whether the pustules are raised and rust-colored; other leaf spots need different diagnosis.", "Share crop-stage and field photos with an agronomist before deciding on a spray."],
        "prevention": ["Select locally adapted resistant hybrids where available.", "Monitor early and maintain balanced crop nutrition; avoid unnecessary pesticide applications."],
        "watch": "Rapid increase before flowering or significant disease on upper leaves merits a field-level agronomy decision.",
        "source_keys": ["plant_diseases", "pesticide_safety"],
    },
    "northernleafblight": {
        "type": "Fungal leaf blight",
        "what": "Northern corn leaf blight is a fungal disease of corn. Long lesions can remove photosynthetic leaf area, with the greatest concern when susceptible crops are infected before or around flowering.",
        "signs": ["Compare for long, cigar-shaped gray-green to tan lesions that are not neatly limited by small leaf veins.", "Check whether lesions are appearing on upper leaves and expanding."],
        "spread": "The pathogen can survive in corn residue and spread by spores; humid weather and prolonged leaf wetness favor infection.",
        "first_steps": ["Scout several plants and rows, noting crop stage and whether lesions are on upper leaves.", "Photograph a full lesion beside a ruler or finger for scale and record recent wet weather.", "Ask an agronomist to verify the disease and estimate yield risk before considering a fungicide."],
        "prevention": ["Plant resistant/tolerant hybrids recommended for the area.", "Use rotation and residue management appropriate to the farm and maintain balanced fertility."],
        "watch": "Fast upward movement in the canopy, especially near flowering, should trigger prompt local agronomy advice.",
        "source_keys": ["plant_diseases", "pesticide_safety"],
    },
    "grapeblackrot": {
        "type": "Fungal disease",
        "what": "Grape black rot is a fungal disease that can affect leaves, shoots, and berries. Leaf spots alone do not show whether fruit is at risk; inspect clusters and young canes too.",
        "signs": ["Look for small tan-to-brown leaf spots that may develop dark margins or tiny black dots.", "Infected berries may shrivel into hard, dark mummies that remain in the canopy."],
        "spread": "The fungus can survive on mummified berries and infected vine material; rain and humidity help spores infect susceptible growth.",
        "first_steps": ["Inspect leaves, shoots, and grape clusters throughout the vine; photograph any shriveled berries.", "Remove accessible mummified berries and infected debris during dry weather.", "Avoid moving suspect plant material to other vines or plots."],
        "prevention": ["Open the canopy for air and light, and remove mummies before the next growing season.", "Use a locally recommended resistant variety when planting and maintain a scouting log."],
        "watch": "New lesions on fruit clusters, rapid spread after rain, or repeated annual infection requires vineyard adviser input.",
        "source_keys": ["plant_diseases", "pesticide_safety"],
    },
    "escablackmeasles": {
        "type": "Grapevine trunk disease (fungal complex)",
        "what": "Esca, also called black measles, is part of a grapevine trunk-disease complex. Leaf symptoms can be irregular and a photo of one leaf cannot confirm the trunk pathogen.",
        "signs": ["Compare for interveinal striping or scorched patches, sometimes with yellowing on white grapes or reddish bands on red grapes.", "Check whether symptoms are concentrated on one shoot or cordon and whether the vine has dieback."],
        "spread": "The fungi infect woody tissues, often through pruning wounds; established wood infections are not removed by ordinary foliar fungicide sprays.",
        "first_steps": ["Mark the vine and photograph leaves, shoots, and the whole plant; do not cut into the trunk based on this result.", "Ask a vineyard specialist to distinguish trunk disease from drought, nutrition, spray injury, or other causes.", "Keep pruning tools clean and avoid pruning during wet conditions."],
        "prevention": ["Use sound pruning and wound-management practices recommended for the local vineyard.", "Remove or renovate dead/diseased wood only with a vineyard adviser’s guidance."],
        "watch": "Sudden whole-shoot wilt, trunk/cordon dieback, or repeat symptoms on the same vine calls for prompt specialist review.",
        "source_keys": ["grape_esca", "pesticide_safety"],
    },
    "leafblightisariopsisleafspot": {
        "type": "Fungal leaf disease",
        "what": "This grape class refers to a leaf-blight/leaf-spot pattern. Several grape diseases and noninfectious stresses can look similar in a single photo, so compare symptoms on multiple leaves and shoots.",
        "signs": ["Check for expanding brown or dark spots, yellowing around damaged tissue, and whether symptoms begin on older leaves.", "Look for matching lesions on nearby shoots or fruit before concluding it is a vine disease."],
        "spread": "Many grape leaf-spot fungi persist on infected plant material and spread more readily in wet, poorly ventilated canopies.",
        "first_steps": ["Photograph both leaf surfaces and inspect several vines, shoots, and clusters.", "Remove only clearly dead material during dry weather; keep it away from healthy vines.", "Ask a local grape adviser to confirm the specific pathogen before treatment."],
        "prevention": ["Maintain an open canopy, avoid prolonged leaf wetness, and remove infected debris after harvest.", "Use clean planting stock and keep records of variety, weather, and symptom timing."],
        "watch": "If lesions spread onto fruit or defoliation progresses quickly, arrange an in-person diagnosis.",
        "source_keys": ["plant_diseases", "pesticide_safety"],
    },
    "huanglongbingcitrusgreening": {
        "type": "Serious bacterial citrus disease (vector-spread)",
        "what": "Huanglongbing (citrus greening) is a serious bacterial disease of citrus spread by psyllid insects and infected planting material. The image model cannot confirm HLB; nutrient problems and other stresses can also yellow leaves.",
        "signs": ["A key sign to compare is uneven, blotchy yellowing across the leaf midrib rather than a balanced pattern on both sides.", "Also check for misshapen, unevenly colored fruit, premature fruit drop, and psyllids or waxy psyllid nymphs on new flush."],
        "spread": "Citrus psyllids and movement of infected citrus plants or grafting material can spread the pathogen; local quarantine rules may apply.",
        "first_steps": ["Do not move cuttings, seedlings, or suspect plant material to another site.", "Photograph several leaves, new shoots, fruit, and the whole tree; note the location and recent planting source.", "Contact a local plant-health/agriculture authority or citrus extension service for official testing and instructions."],
        "prevention": ["Use inspected, certified citrus planting stock and monitor new flush for psyllids.", "Follow local quarantine and coordinated vector-control advice; do not remove the tree until advised by the responsible authority."],
        "watch": "Treat any suspected HLB as urgent for official confirmation because it is serious and regulated in some regions. There is no known cure for an infected tree.",
        "source_keys": ["citrus_hlb", "pesticide_safety"],
        "priority": "Urgent expert confirmation",
    },
    "peachbacterialspot": {
        "type": "Bacterial leaf and fruit disease",
        "what": "Peach bacterial spot is caused by bacteria and may affect leaves, twigs, and fruit. Symptoms can be confused with other leaf spots, spray injury, or nutrient stress.",
        "signs": ["Look for small dark or water-soaked spots that may develop yellow margins or drop out, leaving shot-hole-like marks.", "Check fruit and young twigs as well as leaves."],
        "spread": "Bacteria spread in splashing water and can enter through natural openings or wounds; wet foliage and susceptible varieties raise risk.",
        "first_steps": ["Photograph both sides of several leaves, twigs, and fruit; note recent rain, overhead irrigation, and any sprays.", "Avoid pruning or handling trees while foliage is wet.", "Ask a local fruit-tree adviser to confirm before applying a product."],
        "prevention": ["Use resistant varieties where available, reduce leaf wetness, and keep tools clean.", "Remove infected debris and follow local orchard sanitation and irrigation guidance."],
        "watch": "Repeated twig dieback, extensive fruit spotting, or rapid new symptoms should be reviewed by an orchard specialist.",
        "source_keys": ["plant_diseases", "pesticide_safety"],
    },
    "bacterialspot": {
        "type": "Bacterial leaf disease",
        "what": "Bacterial spot of pepper or tomato is caused by Xanthomonas bacteria. A single leaf image cannot reliably separate it from fungal spots, spray injury, or other stress.",
        "signs": ["Tomato may show small brown spots with yellow halos; pepper spots may look dark and water-soaked and may not have a halo.", "Some lesions can dry and fall out, leaving small holes; fruit can also develop raised spots."],
        "spread": "Bacteria can move in splashing rain/irrigation, on hands and tools, and with contaminated seed or transplants; working among wet plants can spread it.",
        "first_steps": ["Inspect nearby plants and fruit; take photos of both leaf sides and note whether symptoms followed rain or overhead watering.", "Avoid handling wet plants; sanitize tools between plants and remove severely affected leaves only if the plant can tolerate it.", "Use clean transplants and ask a local vegetable adviser to confirm the disease."],
        "prevention": ["Use clean seed/transplants, drip or base watering, good spacing, and crop rotation away from tomato/pepper relatives as locally advised.", "Remove crop debris and volunteer plants after harvest."],
        "watch": "A pesticide will not repair already infected leaves. Some locally approved protectants may reduce new infection in certain crops, but efficacy varies and copper resistance is documented; get local advice before use.",
        "source_keys": ["bacterial_spot", "pesticide_safety"],
    },
    "earlyblight": {
        "type": "Fungal leaf blight",
        "what": "Early blight of tomato or potato is a fungal disease that commonly begins on older lower leaves and can also affect stems and fruit.",
        "signs": ["Look for round brown leaf spots with darker concentric rings, often surrounded by yellowing.", "Symptoms often begin on older, lower leaves; fruit or stem lesions may occur."],
        "spread": "The fungus survives on infected debris and can spread by water splash; wet leaves, crowded plants, and volunteer host plants help it persist.",
        "first_steps": ["Inspect lower and upper leaves on several plants; photograph ringed spots and check for fruit or stem lesions.", "Remove a small number of affected lower leaves if plants remain well-leafed; do not strip more than needed.", "Use mulch and water at soil level; clean tools and hands after touching affected plants."],
        "prevention": ["Rotate away from tomato/potato relatives for the locally recommended interval and remove volunteer plants.", "Stake plants, improve airflow, and clear infected residue after harvest."],
        "watch": "If spots are advancing rapidly, reaching upper foliage, or affecting fruit, ask a local adviser whether a labelled fungicide is justified. Products protect healthy growth; they do not erase existing lesions.",
        "source_keys": ["early_blight", "pesticide_safety"],
    },
    "lateblight": {
        "type": "Fast-spreading water-mold disease",
        "what": "Late blight is caused by Phytophthora infestans, a water mold, not a true fungus. It can spread rapidly in cool, wet conditions and affect tomato or potato foliage, stems, fruit, and tubers.",
        "signs": ["Compare for large, irregular dark blotches with pale green/gray margins; humid conditions may show fine white growth on the underside.", "Check stems and potato/tomato fruit or tubers for dark, firm-to-soft lesions."],
        "spread": "Spores spread quickly in wet weather and can arrive on infected potato tubers, transplants, or from nearby crops.",
        "first_steps": ["Keep suspect plants separate from healthy transplants and avoid touching plants while wet.", "Take clear photos of leaf tops/undersides, stems, fruit, and nearby plants; note recent wet weather.", "Contact a local plant-disease adviser promptly for confirmation because late blight can spread quickly."],
        "prevention": ["Use certified seed potatoes and inspected transplants; remove volunteer potatoes and manage cull piles.", "Keep foliage dry, improve spacing/airflow, and remove infected crop debris according to local advice."],
        "watch": "Rapid spread or dark lesions on stems/fruit/tubers is urgent. If confirmed, only a locally registered late-blight product and timing advised for the crop and region should be considered; a generic fungicide may not work against this water mold.",
        "source_keys": ["late_blight", "pesticide_safety"],
        "priority": "Prompt expert confirmation",
    },
    "potatohealthy": {
        "healthy": True,
    },
    "powderymildew": {
        "type": "Fungal disease",
        "what": "Powdery mildew is a group of fungal diseases that form superficial growth on leaves and can reduce vigor or distort young growth. It is not the same disease as downy mildew.",
        "signs": ["Look for white, powder-like patches on the upper or lower leaf surface.", "Leaves may yellow, curl, or become distorted as infection increases."],
        "spread": "Spores spread through air; dense growth and susceptible young tissue may increase risk, although weather patterns differ from many wet-leaf diseases.",
        "first_steps": ["Check both sides of multiple leaves and compare with dusty residue or spray deposits.", "Remove a few badly affected leaves if practical, without stripping the plant.", "Increase airflow and water at the soil line; avoid stressing plants with irregular watering."],
        "prevention": ["Choose resistant varieties when possible and space plants for airflow.", "Remove diseased debris and monitor new growth regularly."],
        "watch": "If new growth is heavily distorted or fruiting is affected, ask a local horticulture adviser about a crop-labelled option.",
        "source_keys": ["mildew", "pesticide_safety"],
    },
    "leafscorch": {
        "type": "Fungal leaf disease",
        "what": "Strawberry leaf scorch is a fungal disease that causes many small leaf spots; severe infection can make leaves look burned and may reduce plant vigor and fruit quality.",
        "signs": ["Compare for small brown-to-purple spots with indistinct edges; severe leaves may redden, dry, curl, and look scorched.", "Common leaf spot can look similar but often has a more clearly defined spot border."],
        "spread": "The fungus survives in strawberry debris; rain splash, overhead irrigation, warm wet weather, and crowded foliage can help it spread.",
        "first_steps": ["Check several leaves and plants, noting whether spots are spreading; photograph upper and lower surfaces.", "Remove dead/scorched debris without stripping healthy leaves and keep it away from the strawberry bed.", "Switch to drip/base watering and irrigate in the morning so foliage dries quickly."],
        "prevention": ["Use clean plants, an open sunny bed, adequate spacing, and weed control.", "Remove old strawberry debris after the season; consider locally recommended annual renewal or resistant varieties where suitable."],
        "watch": "If new spots continue to appear in wet weather or flowers/fruit are affected, ask a local strawberry adviser to confirm the diagnosis. A crop-labelled fungicide may be considered only under local guidance; cultural controls remain important.",
        "source_keys": ["strawberry_scorch", "pesticide_safety"],
    },
    "leafmold": {
        "type": "Fungal leaf disease",
        "what": "Tomato leaf mold is a fungal disease that often develops in humid, poorly ventilated conditions, especially under cover. It usually begins on older foliage.",
        "signs": ["Look for pale yellow patches on the upper leaf surface with olive-green to brown velvety growth beneath the matching areas.", "Severe leaves may curl, dry, and drop; fruit is less commonly affected."],
        "spread": "Spores move through air and infected crop debris; high humidity and long periods of leaf wetness favor disease.",
        "first_steps": ["Inspect the underside of leaves corresponding to yellow patches and check other plants in the greenhouse/row.", "Improve ventilation, avoid wetting leaves, and remove badly affected lower leaves using clean tools.", "Bag or dispose of infected debris away from the crop."],
        "prevention": ["Ventilate protected crops, space and train plants, water at soil level, and clean the growing area after harvest.", "Use resistant varieties where available and monitor humidity and new growth."],
        "watch": "If the disease keeps returning despite drier air and sanitation, seek a local greenhouse adviser’s diagnosis and crop-labelled control options.",
        "source_keys": ["tomato", "pesticide_safety"],
    },
    "septorialeafspot": {
        "type": "Fungal leaf spot",
        "what": "Septoria leaf spot is a fungal disease of tomato foliage that often starts on older, lower leaves and can cause significant defoliation in wet weather.",
        "signs": ["Look for numerous small, round spots with pale gray/tan centers and darker edges; tiny dark specks may sit in the centers.", "Spots usually lack the large bull's-eye rings typical of early blight."],
        "spread": "The fungus survives in infected debris and can splash from soil or move in wet foliage; prolonged leaf wetness favors infection.",
        "first_steps": ["Inspect lower leaves on multiple plants and compare spots for pale centers and dark margins.", "Remove the lowest severely spotted leaves if practical, sanitize tools, and mulch soil to reduce splash.", "Water at the base and avoid handling wet plants."],
        "prevention": ["Rotate away from tomato relatives, remove crop debris and volunteers, and stake/space plants for airflow.", "Use clean seed/transplants and keep foliage dry."],
        "watch": "If lesions reach upper canopy or defoliation is accelerating, ask a local adviser about a crop-labelled fungicide; sprays cannot restore dead leaf tissue.",
        "source_keys": ["tomato", "pesticide_safety"],
    },
    "tomatospidermitestwospottedspidermite": {
        "type": "Mite pest (not a disease)",
        "what": "The model's label is consistent with two-spotted spider-mite injury on tomato. Spider mites are tiny sap-feeding pests, not insects or a fungal disease.",
        "signs": ["Check the undersides of leaves with a hand lens for tiny moving mites, eggs, or fine webbing.", "Feeding often causes many pale pinprick specks, then bronzing or drying; drought stress can look similar."],
        "spread": "Hot, dry conditions can allow mite numbers to rise quickly; mites and infested plant material can move between nearby plants.",
        "first_steps": ["Tap a discolored leaf over white paper and look for moving specks; inspect undersides on several plants.", "Reduce plant water stress and, if locally appropriate, rinse leaf undersides with water.", "Do not use a broad-spectrum insecticide as a first response; it can kill natural enemies and worsen mite outbreaks."],
        "prevention": ["Scout leaf undersides regularly during hot, dry periods and control dust where practical.", "Conserve predatory mites and other beneficial insects; remove badly infested debris."],
        "watch": "If mites are confirmed and increasing, ask local extension which labelled miticide/acaricide or contact product is suitable. Coverage of leaf undersides, crop safety, harvest interval, and beneficial-insect effects matter.",
        "source_keys": ["mites", "pesticide_safety"],
    },
    "targetspot": {
        "type": "Fungal leaf spot",
        "what": "Target spot is a fungal disease that can affect tomato leaves and sometimes other plant parts. It can resemble early blight or other leaf-spot diseases.",
        "signs": ["Compare for brown circular lesions with concentric rings; spots may develop yellowing around them.", "Check lower and upper leaves and fruit/stems because the pattern can overlap with other diseases."],
        "spread": "Infected residue and humid, wet foliage can contribute to spread; dense canopies dry slowly.",
        "first_steps": ["Photograph multiple lesions beside unaffected tissue and inspect neighboring plants.", "Keep foliage dry, improve airflow, and remove severely affected leaves with clean tools.", "Ask an adviser to distinguish target spot from early blight and bacterial spot before treatment."],
        "prevention": ["Use clean planting material, crop rotation, removal of volunteers/debris, and adequate spacing.", "Avoid overhead irrigation and keep a weekly symptom log."],
        "watch": "Rapid spread into upper foliage or fruit symptoms should be assessed before choosing a crop-labelled fungicide.",
        "source_keys": ["tomato", "pesticide_safety"],
    },
    "tomatoyellowleafcurlvirus": {
        "type": "Viral disease (often whitefly-transmitted)",
        "what": "Tomato yellow leaf curl is a viral disease associated with whitefly transmission. Similar curling or yellowing can result from heat, drought, herbicide injury, or nutrient stress, so confirm before removing plants.",
        "signs": ["Check for upward-curling, smaller yellow leaflets on new growth and shortened internodes or stunting.", "Look for whiteflies under leaves and compare symptoms across plants."],
        "spread": "Whiteflies can transmit the virus between tomato plants; infected transplants and movement of plants can also introduce risk.",
        "first_steps": ["Inspect new leaves and undersides for whiteflies; photograph whole plants and nearby tomatoes.", "Do not save cuttings or move suspect transplants to another plot.", "Ask an extension adviser or plant-health service to confirm before removing plants or applying insecticides."],
        "prevention": ["Use clean transplants and locally recommended resistant varieties; manage weeds/volunteer tomatoes that host whiteflies.", "Use vector management only as part of a local integrated plan; vector control does not cure an infected plant."],
        "watch": "There is no curative spray for an infected plant. If several plants show new-growth symptoms, get local diagnosis and vector-management advice promptly.",
        "source_keys": ["tomato", "pesticide_safety"],
    },
    "tomatomosaicvirus": {
        "type": "Viral disease",
        "what": "Tomato mosaic virus can cause mottled foliage and distorted growth. Nutrient stress, herbicide injury, and other viruses may look similar, so the image class needs confirmation.",
        "signs": ["Compare for irregular light and dark green mosaic patches, leaf distortion, or narrow/fern-like leaflets.", "Some plants may be stunted or produce uneven fruit."],
        "spread": "The virus can spread on contaminated hands, tools, seed, and plant material; handling plants can move it mechanically.",
        "first_steps": ["Avoid touching healthy tomato plants after handling a suspect plant; wash hands and clean tools.", "Do not save seed or cuttings from a suspect plant while awaiting advice.", "Ask a local extension adviser to confirm the cause before removing plants."],
        "prevention": ["Use certified clean seed/transplants and resistant varieties where locally available.", "Clean tools and work from apparently healthy plants toward suspect ones."],
        "watch": "No pesticide cures a virus inside a plant. If symptoms are appearing on several plants, seek confirmation and sanitation guidance; do not spend on fungicide or improvised antibiotics.",
        "source_keys": ["tomato", "pesticide_safety"],
    },
}


_HEALTHY = {
    "type": "No disease class detected",
    "what": "The model matched the photo to a healthy-leaf class for this crop. This means the image resembles healthy examples the model learned; it does not rule out early disease, pests, nutrient stress, or problems outside the leaf area shown.",
    "signs": ["Compare several leaves, including new growth and the underside, for spots, mottling, insects, webbing, curling, or unusual yellowing.", "Look at the whole plant and neighboring plants; a single clean leaf cannot establish that the crop is healthy."],
    "spread": "Not applicable to a healthy-class prediction. Continue monitoring because early symptoms may not be visible in the submitted photo.",
    "first_steps": ["No medication is indicated from this result alone.", "Keep watering and nutrition consistent with the crop and local soil conditions.", "Take a dated photo now and compare it with new growth over the next several days."],
    "prevention": ["Use clean planting material, good spacing, balanced irrigation, and routine scouting.", "Remove crop debris and disinfect tools when moving between plots or plants."],
    "watch": "If symptoms appear or plants decline despite this result, upload clear photos of affected leaves and consult a local crop adviser.",
    "source_keys": ["plant_diseases"],
}


def _key(value: str) -> str:
    return "".join(character for character in value.lower() if character.isalnum())


def _crop_key(value: str) -> str:
    key = _key(value)
    if key.startswith("cherry"):
        return "cherry"
    if key.startswith("cornmaize"):
        return "corn"
    if key.startswith("pepperbell"):
        return "pepper"
    return key


def _pathogen_group(disease: str) -> str:
    key = _key(disease)
    if key == "healthy":
        return "healthy"
    if "huanglongbing" in key or "citrusgreening" in key:
        return "hlb"
    if "virus" in key or "yellowleafcurl" in key or "mosaic" in key:
        return "virus"
    if "bacterial" in key:
        return "bacterial"
    if "spidermite" in key or "twospotted" in key:
        return "mite"
    if "esca" in key or "blackmeasles" in key:
        return "trunk"
    if "lateblight" in key:
        return "oomycete"
    return "fungal"


def _treatment_options(disease: str, profile: dict) -> list[str]:
    group = _pathogen_group(disease)
    if profile.get("healthy"):
        return ["No pesticide or medication is recommended by this result. Diagnose a visible problem separately before treating."]
    if group == "hlb":
        return ["There is no known cure for a citrus tree infected with HLB. Do not buy a spray claiming to cure it.", "Psyllid control and removal/quarantine decisions are local, often coordinated actions; contact the responsible agriculture or plant-health authority before treatment or moving plant material."]
    if group == "virus":
        return ["There is no curative pesticide for a virus inside a plant. Fungicides and antibiotics do not cure viral infection.", "Vector control may reduce new spread for some viruses but does not cure an infected plant; use only a locally recommended integrated plan after the diagnosis is confirmed."]
    if group == "bacterial":
        return ["Already infected leaf tissue will not recover. Some crop-specific, locally registered protectant bactericides may reduce new infection in certain settings, but results vary and resistance or leaf injury can occur.", "Ask a local agricultural adviser to confirm the cause and the currently registered product for this crop and disease. Do not improvise antibiotic use."]
    if group == "mite":
        return ["Start with scouting and water-stress correction; rinse leaf undersides if practical and safe for the crop.", "If mites are confirmed and increasing, ask about a crop-labelled miticide/acaricide or contact product. Treat the underside as directed and protect beneficial predators; broad-spectrum insecticides can make mite problems worse."]
    if group == "trunk":
        return ["A foliar fungicide will not cure established Esca infection in vine wood. Avoid purchasing a spray based on this leaf result.", "A vineyard specialist should assess pruning, vine surgery, or replacement options for the affected vine and local conditions."]
    if group == "oomycete":
        return ["Late blight is caused by a water mold, so products intended for ordinary fungi may not control it.", "If confirmed, a locally registered late-blight product may protect uninfected tissue when applied at the right time. Get urgent regional advice and follow the exact crop label, including harvest and re-entry limits."]
    return ["Nonchemical steps and confirmation come first; treatments do not restore leaves that are already dead or scorched.", "If disease is confirmed and still spreading, ask local extension which fungicide is currently registered for this exact crop and disease. Product choice, rate, timing, and harvest interval depend on the country and label.", "Use personal protective equipment and follow all label directions; avoid spraying in wind, near water, or when pollinators may be exposed. Do not mix products unless the label permits it."]


def advisory_for(disease: str, crop: str) -> dict:
    """Return a structured, cautious field assessment for a model class."""
    disease_key = _key(disease)
    profile = _PROFILES.get(_crop_key(crop) + disease_key) or _PROFILES.get(disease_key)
    if profile is None and disease_key == "healthy":
        profile = _HEALTHY
    if profile is None:
        # Model labels not covered above still receive a disease-specific
        # category and a safe IPM action plan rather than a blank result.
        group = _pathogen_group(disease)
        if group == "bacterial":
            profile = {
                "type": "Possible bacterial disease",
                "what": f"The classifier matched this {crop} image to {disease}. Bacterial, fungal, and noninfectious leaf problems can overlap in appearance, so this result needs local confirmation.",
                "signs": ["Compare spots on several leaves, both surfaces, and check whether the edges are water-soaked, yellow, or raised.", "Look for matching symptoms on stems, fruit, or nearby plants."],
                "spread": "Many bacterial leaf diseases spread through splashing water, contaminated tools, or infected planting material.",
                "first_steps": ["Avoid handling wet plants and sanitize tools between plants.", "Photograph the whole plant and close-ups and note recent rain, watering, and sprays.", "Ask a local crop adviser to confirm the disease before treatment."],
                "prevention": ["Use clean seed/transplants, reduce leaf wetness, and remove infected crop debris after harvest.", "Follow locally appropriate crop rotation and sanitation."],
                "watch": "Get advice if lesions spread quickly, affect stems/fruit, or appear across many plants.",
                "source_keys": ["plant_diseases", "pesticide_safety"],
            }
        elif group == "virus":
            profile = {
                "type": "Possible viral disease",
                "what": f"The classifier matched this {crop} image to {disease}. Leaf patterns alone cannot confirm a virus, and stresses can cause similar symptoms.",
                "signs": ["Look for mosaic coloring, curling, distortion, or stunting on new growth.", "Check for insect vectors and compare several plants."],
                "spread": "Plant viruses can spread through vectors, contaminated tools, seed, or infected planting material depending on the virus.",
                "first_steps": ["Do not move cuttings or seedlings from the suspect plant.", "Clean tools and wash hands before handling other plants.", "Seek local confirmation before removing plants or using insecticides."],
                "prevention": ["Use certified clean planting material and locally recommended resistant varieties.", "Control potential vectors only through an integrated local plan."],
                "watch": "No pesticide cures an infected plant; ask for an expert review if new symptoms continue appearing.",
                "source_keys": ["plant_diseases", "pesticide_safety"],
            }
        else:
            profile = {
                "type": "Possible fungal leaf disease",
                "what": f"The classifier matched this {crop} image to {disease}. This is a screening clue; similar spots can have different causes and need different treatment.",
                "signs": ["Compare the shape, color, border, and location of spots on several leaves.", "Inspect both leaf surfaces and look for signs on stems or fruit."],
                "spread": "Many leaf-spot fungi survive in debris and spread when infected foliage stays wet, but the exact life cycle depends on the disease.",
                "first_steps": ["Photograph several affected and healthy leaves and record when symptoms began.", "Water at soil level, improve airflow, and avoid working among wet plants.", "Remove clearly dead debris and clean tools between plants."],
                "prevention": ["Use clean planting material, appropriate rotation, spacing, and sanitation.", "Monitor weekly and confirm the cause before choosing a pesticide."],
                "watch": "Seek local advice if symptoms spread to new growth, fruit, or stems, or if plants decline quickly.",
                "source_keys": ["plant_diseases", "pesticide_safety"],
            }

    is_healthy = bool(profile.get("healthy"))
    if is_healthy:
        profile = _HEALTHY
    sources = []
    for source_key in profile.get("source_keys", ["plant_diseases"]):
        label, url = _SOURCES[source_key]
        sources.append({"label": label, "url": url})
    # A label-safety source is useful whenever the recommendation includes a
    # conditional chemical option.
    if not is_healthy and _pathogen_group(disease) not in {"virus", "hlb", "trunk"}:
        label, url = _SOURCES["pesticide_safety"]
        if not any(source["url"] == url for source in sources):
            sources.append({"label": label, "url": url})

    first_steps = profile.get("first_steps", [])
    return {
        "summary": f"The image model suggests {disease} on {crop}. Compare the typical signs below and confirm the cause before using a pesticide.",
        "actions": first_steps[:3],
        "crop_note": f"Crop predicted from the photo: {crop}. The model assigns the whole image to a learned crop/disease class; it does not mark the lesion or verify every symptom.",
        "type": profile.get("type", "Possible plant-health issue"),
        "what": profile.get("what", "This is a screening estimate, not a confirmed diagnosis."),
        "signs": profile.get("signs", []),
        "spread": profile.get("spread", "Spread patterns vary by disease and local conditions."),
        "first_steps": first_steps,
        "treatment": _treatment_options(disease, profile),
        "prevention": profile.get("prevention", []),
        "watch": profile.get("watch", "Seek local advice if symptoms spread or the plant declines."),
        "priority": profile.get("priority", "Monitor and confirm locally"),
        "sources": sources,
        "healthy": is_healthy,
    }
