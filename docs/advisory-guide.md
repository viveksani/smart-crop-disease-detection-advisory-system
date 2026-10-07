# Disease Advisory Guide

## What appears in a result

The MobileNetV2 classifier returns one of the supported crop/condition labels. The application maps that label to a curated, rules-based profile in `app/advisory.py`. The result page presents:

- the predicted crop and possible condition;
- typical signs a grower can compare against the plant;
- a short description of cause and possible spread;
- immediate scouting and sanitation steps;
- treatment categories and prevention actions;
- cues for contacting an extension officer, plant-health authority, or crop specialist;
- selected university-extension and regulatory references.

This advice is tied to the predicted class, not to image segmentation or a second visual analysis. The system does not claim that its listed symptoms were actually detected in the photo. A wrong crop/disease class can make the associated guidance inappropriate, so users should confirm the plant and condition before acting.

## Treatment language and safety limits

The application describes treatment options as conditional IPM guidance. It does not supply pesticide brands, rates, tank mixes, or a guarantee of effectiveness. Product registrations, permitted crops, application rates, protective equipment, re-entry periods, pollinator restrictions, and harvest intervals vary by jurisdiction and product label. In India, users can check the Directorate of Plant Protection, Quarantine and Storage / CIB&RC registered-product information and the specific container label. Elsewhere, users should check their national or local regulator.

The advisory distinguishes several treatment situations:

- **Fungal leaf spots and mildews:** sanitation, dry foliage, airflow, scouting, and crop-specific, locally registered fungicide guidance if infection is confirmed and still spreading. A spray cannot restore dead or scorched leaf tissue.
- **Late blight:** prompts quick expert confirmation because it may spread rapidly; it explains that the causal organism is a water mold, so a generic fungicide suggestion may be inappropriate.
- **Bacterial spot:** emphasizes clean transplants, tool hygiene, and reduced splash. A locally registered protectant can be considered only with expert guidance; efficacy and resistance vary.
- **Viruses and citrus greening:** explains that there is no curative spray for an infected plant, and points users toward vector management, official confirmation, and local quarantine instructions where relevant.
- **Spider mites:** directs the user to inspect leaf undersides and avoid broad-spectrum insecticides as a first response; any chemical option must be a crop-labeled miticide/acaricide.
- **Esca of grape:** explains that foliar sprays do not cure established trunk infection and recommends vine-level assessment.
- **Healthy class:** recommends monitoring rather than medication and explains that a healthy class does not rule out early symptoms or problems outside the submitted image.

## Sources used for the in-app guidance

- [UC IPM: strawberry leaf scorch](https://ipm.ucanr.edu/home-and-landscape/leaf-scorch-of-strawberries/) — typical strawberry symptoms, spread conditions, and cultural management.
- [University of Minnesota Extension: bacterial spot of tomato and pepper](https://extension.umn.edu/agriculture/specialty-crops/vegetable-farming/disease-management/bacterial-spot-of-tomato-and-pepper) — symptom comparison, splash/tool spread, sanitation, and resistance caveats.
- [University of Minnesota Extension: early blight in tomato and potato](https://extension.umn.edu/agriculture/specialty-crops/vegetable-farming/disease-management/early-blight-in-tomato-and-potato) — signs and cultural controls.
- [University of Minnesota Extension: late blight](https://extension.umn.edu/agriculture/specialty-crops/vegetable-farming/disease-management/late-blight) — water-mold classification, rapid-spread risk, crop sanitation, and local-label cautions.
- [UC IPM: citrus greening / Asian citrus psyllid](https://ipm.ucanr.edu/agriculture/citrus/asian-citrus-psyllid/) — vector relationship, lack of a cure, and coordinated management.
- [UC IPM: grape Esca (black measles)](https://ipm.ucanr.edu/agriculture/grape/esca-black-measles/) — trunk-disease symptoms and why foliar fungicides do not eradicate established wood infection.
- [University of Minnesota Extension: spider mites](https://extension.umn.edu/garden-and-home/yard-and-garden/yard-and-garden-insects/spider-mites) — underside scouting, stippling/webbing, and protecting natural enemies.
- [India PPQS / CIB&RC registered products](https://ppqs.gov.in/divisions/cib-rc/registered-products) — reference point for Indian product-registration information; the product's own approved label remains essential.

The references provide general learning material and are not a substitute for local, current crop guidance. Several extension pages are specific to their own regions. The field performance of this project's model and advisory has not been validated with local farmer photos or field trials.
