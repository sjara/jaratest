import numpy as np

allenPlateNames = ['http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576991187&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576991103&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576991063&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576991023&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990983&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990943&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990901&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990861&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990821&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990781&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990741&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990701&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990661&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990621&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990581&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990541&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990501&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990461&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990421&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990381&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576991267&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576991227&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990353&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990313&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990273&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989589&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989549&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989509&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989469&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989429&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989389&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989349&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989309&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989269&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989229&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989189&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989149&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989109&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989069&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989029&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988989&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988949&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988909&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988869&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576991143&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988833&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988793&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987993&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987953&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987913&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987873&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987833&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987793&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987753&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987713&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987673&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987633&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987593&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987553&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987513&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987473&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987433&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987387&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987346&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987303&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987259&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990261&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990221&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990181&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990141&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990101&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990061&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576990020&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989980&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989940&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989900&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989860&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989820&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989779&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987211&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987171&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987131&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987091&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987051&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576987011&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986971&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986931&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986891&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986851&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986811&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986771&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986731&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986691&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986651&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986611&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986571&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986531&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986491&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986451&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986411&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986371&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988729&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988689&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988649&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988609&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988569&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988529&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988489&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988449&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988409&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988369&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988329&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988289&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988249&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988209&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988169&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988129&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988089&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988049&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576988009&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989723&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989682&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576989642&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986339&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986299&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986259&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986219&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986179&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986139&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986099&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986059&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4',

'http://atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate=576986019&structure=957&x=7748&y=4989.86669921875&zoom=-4&resolution=16.00&z=4']

#I added these in reverse order, so I need to reverse the list
allenPlateNames = allenPlateNames[::-1]

def convertAllenZ(allenZ):
    '''
    Convert a coronal Z-stack value into the corresponding plate in the web atlas
    Args:
        allenZ (int): The stack number in the allen CCF 25um volume
    Returns:
        webPlateURL (string): the URL of the closest-corresponding plate in the web viewer
    '''
    startPlate = 576986019
    plateSpacing = 40
    webPlateInd = int(np.round((allenZ - 2) / 4.))
    webPlateURL = allenPlateNames[webPlateInd]
    return webPlateURL
