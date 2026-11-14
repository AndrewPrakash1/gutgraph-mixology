<!-- ========================================== -->
    // Embedded Data Objects
        // Clean Relative Asset Paths
    const ASSETS = {
      "can-front-3d.png": "assets/can-front-3d.png",
      "can-rear-3d.png": "assets/can-rear-3d.png",
      "can1-texture.png": "assets/can1-texture.png",
      "can2-texture.png": "assets/can2-texture.png",
      "brush-top-right.png": "assets/brush-top-right.png",
      "brush-bottom.png": "assets/brush-bottom.png",
      "brush-left.png": "assets/brush-left.png",
      "logo-seal.png": "assets/logo-seal.png",
      "sunkissed.png": "assets/products/sunkissed.png",
      "golden-hour.png": "assets/products/golden-hour.png",
      "pink-paradise.png": "assets/products/pink-paradise.png",
      "desi-cool.png": "assets/products/desi-cool.png",
      "ruby-rush.png": "assets/products/ruby-rush.png",
      "mint-condition.png": "assets/products/mint-condition.png"
    };

    const PRODUCTS = [
      {
        id: "sunkissed",
        name: "SUNKISSED",
        tagline: "Golden Mango Pulp & Wild Citrus",
        subtitle: "High-Polyphenol Tropical Elixir",
        volume: "330ml",
        abv: "0.0%",
        calories: 34,
        primaryColor: "#FF9D36",
        cardBg: "#3A1A05",
        image: ASSETS["sunkissed.png"],
        category: "TROPICAL",
        microbe: "Bifidobacterium lactis HN019",
        microbeDesc: "Supports short-chain fatty acid (SCFA) conversion from prebiotic inulin.",
        molecules: [
          { name: "Mangiferin", source: "Alphonso Mango", role: "Antioxidant & metabolic balance" },
          { name: "Limonene", source: "Kaffir Lime", role: "Crisp citrus volatile & digestive ease" },
          { name: "1,8-Cineole", source: "Cardamom", role: "Aromatic top-note synergy" }
        ],
        nutrition: { protein: "0.6g", carbs: "8.2g", fiber: "3.2g", sodium: "28mg" },
        ingredients: ["Alphonso Mango Puree (Cold-Pressed)", "Sparkling Spring Water", "Kaffir Lime Peel Infusion", "Organic Inulin Prebiotic Fiber", "Green Cardamom Pod Extract", "Himalayan Pink Salt"],
        allergens: "None declared.",
        context: "Post-lunch afternoon refreshment, campus dining companion."
      },
      {
        id: "golden-hour",
        name: "GOLDEN HOUR",
        tagline: "Bio-Optimized Haldi & Tellicherry Pepper",
        subtitle: "The Modernized Indian Golden Elixir",
        volume: "330ml",
        abv: "0.0%",
        calories: 28,
        primaryColor: "#E9BD48",
        cardBg: "#302206",
        image: ASSETS["golden-hour.png"],
        category: "AYURVEDIC",
        microbe: "Faecalibacterium prausnitzii (Simulated Support)",
        microbeDesc: "Polyphenol fraction encourages butyrate-producing commensal bacteria.",
        molecules: [
          { name: "Curcumin", source: "Lakadong Turmeric", role: "Gut lining barrier support" },
          { name: "Piperine", source: "Tellicherry Pepper", role: "Amplifies curcumin absorption by 2000%" },
          { name: "Gingerols", source: "Fresh Ginger", role: "Gastric motility stimulant" }
        ],
        nutrition: { protein: "1.2g", carbs: "5.4g", fiber: "2.8g", sodium: "34mg" },
        ingredients: ["Lakadong Turmeric (High 7.5% Curcumin)", "Steeped Oat & Coconut Milk Blend", "Fresh Crushed Ginger Rhizome", "Tellicherry Black Pepper", "Ceylon Cinnamon Bark", "Organic Raw Monkfruit"],
        allergens: "Contains Coconut. Dairy-free, vegan certified.",
        context: "Late-night mess recovery, anti-inflammatory wind-down."
      },
      {
        id: "pink-paradise",
        name: "PINK PARADISE",
        tagline: "Wild Guava & Organic Aloe Vera",
        subtitle: "Tropical Prebiotic Botanical Spritz",
        volume: "330ml",
        abv: "0.0%",
        calories: 30,
        primaryColor: "#F18BAA",
        cardBg: "#340F1E",
        image: ASSETS["pink-paradise.png"],
        category: "TROPICAL",
        microbe: "Lactobacillus rhamnosus GG",
        microbeDesc: "Synergistic pectin fiber feeds colonic microflora while aloe provides soothing gut transit.",
        molecules: [
          { name: "Lycopene", source: "Pink Guava", role: "Cellular oxidative shield" },
          { name: "Acemannan", source: "Aloe Vera Gel", role: "Mucosal lining soothing polysaccharide" },
          { name: "Anthocyanins", source: "Hibiscus", role: "Vibrant pigmentation and polyphenol diversity" }
        ],
        nutrition: { protein: "0.8g", carbs: "6.8g", fiber: "4.1g", sodium: "42mg" },
        ingredients: ["Pink Allahabad Guava Puree", "Electrolyte Spring Water", "Aloe Vera Inner Leaf Fillet Juice", "Hibiscus Sabdariffa Calyx Tea", "Rock Salt & Roasted Chaat Spices"],
        allergens: "None declared.",
        context: "Brunch beverage, post-workout rehydration."
      },
      {
        id: "desi-cool",
        name: "DESI COOL",
        tagline: "Cultured Masala Chaas & Roasted Jeera",
        subtitle: "The Probiotic Subcontinental Heritage Tonic",
        volume: "330ml",
        abv: "0.0%",
        calories: 22,
        primaryColor: "#80B98B",
        cardBg: "#122A1A",
        image: ASSETS["desi-cool.png"],
        category: "FERMENTED",
        microbe: "Active Live Cultures (2.5 Billion CFU)",
        microbeDesc: "Direct introduction of live lactic-acid fermenting bacteria to replenish gut ecosystem.",
        molecules: [
          { name: "Cuminaldehyde", source: "Roasted Cumin", role: "Pancreatic enzyme activation" },
          { name: "Carvone", source: "Fresh Spearmint", role: "Smooth muscle relaxant & cooling sensation" },
          { name: "Lactic Acid", source: "Cultured Ferment", role: "Natural preservative & gut pH maintenance" }
        ],
        nutrition: { protein: "2.4g", carbs: "3.2g", fiber: "1.2g", sodium: "88mg" },
        ingredients: ["Artisanal Cultured Buttermilk", "Dry-Roasted Cumin (Jeera) Seeds", "Hand-Torn Spearmint & Curry Leaves", "Ginger Root Pressed Juice", "Black Kala Namak Mineral Salt"],
        allergens: "Contains Milk / Dairy (Lactose).",
        context: "Post-lunch digestive reset, hostel canteen savior."
      },
      {
        id: "ruby-rush",
        name: "RUBY RUSH",
        tagline: "Wild Kokum & Cold-Pressed Pomegranate",
        subtitle: "High-Flavonoid Coastal Tannin Spritzer",
        volume: "330ml",
        abv: "0.0%",
        calories: 32,
        primaryColor: "#A92348",
        cardBg: "#2A0612",
        image: ASSETS["ruby-rush.png"],
        category: "AYURVEDIC",
        microbe: "Gordonibacter urolithinfaciens (Targeted Pathway)",
        microbeDesc: "Provides raw ellagitannin precursors that healthy gut microflora metabolize into Urolithin A.",
        molecules: [
          { name: "Garcinol", source: "Malabar Kokum", role: "Potent gastric mucosal protection" },
          { name: "Punicalagin", source: "Pomegranate Rind", role: "Converted to Urolithin A by gut microbes" },
          { name: "Anethole", source: "Toasted Fennel", role: "Carminative bloat reducer" }
        ],
        nutrition: { protein: "0.5g", carbs: "7.6g", fiber: "3.0g", sodium: "18mg" },
        ingredients: ["Wild Malabar Kokum Rind Extract", "Bhagwa Pomegranate Fresh Squeeze", "Sparkling Filtered Mountain Spring Water", "Crushed Coriander Seeds", "Toasted Fennel Infusion"],
        allergens: "None declared.",
        context: "Dinner apéritif, sophisticated evening alcohol alternative."
      },
      {
        id: "mint-condition",
        name: "MINT CONDITION",
        tagline: "Wild Spearmint, Lime & Micro-Dosed Ginger",
        subtitle: "Electrifying Crisp Alkaline Refresher",
        volume: "330ml",
        abv: "0.0%",
        calories: 19,
        primaryColor: "#70B96B",
        cardBg: "#0C2412",
        image: ASSETS["mint-condition.png"],
        category: "REFRESHING",
        microbe: "Akkermansia muciniphila (Indirect Stimulus)",
        microbeDesc: "Supports gut barrier mucus layer integrity with tart phytochemicals and fermentable pectin.",
        molecules: [
          { name: "Menthol & Menthone", source: "Wild Spearmint", role: "Trigeminal cooling receptor activation" },
          { name: "Citric Acid & Limonene", source: "Kagzi Lime", role: "Palate cleanser & salivary stimulant" },
          { name: "Pectin", source: "Green Apple", role: "Soluble prebiotic gel matrix" }
        ],
        nutrition: { protein: "0.2g", carbs: "4.1g", fiber: "2.5g", sodium: "22mg" },
        ingredients: ["Double-Distilled Spearmint Hydrosol", "Kagzi Lime Cold-Pressed Juice", "Subtle Cold-Pressed Ginger Root", "Sparkling Artesian Water", "Green Apple Skin Pectin"],
        allergens: "None declared.",
        context: "Instant mental clarity, post-canteen digestive reboot."
      }
    ];

    const RECIPES = [
      {
        id: "haldi-ginger-chaas",
        name: "Haldi Ginger Chaas",
        hindiName: "हल्दी अदरक छाछ",
        category: "Digestive Chaas",
        prepTime: "4 mins",
        difficulty: "Easy (3 min)",
        temperature: "Chilled",
        desc: "Cold-whisked probiotic dahi infused with freshly grated raw turmeric root, crushed ginger juice, and fragrant dry-roasted jeera.",
        target: "Instant noodles, greasy canteen roll, fried samosas or pakoras.",
        ingredients: [
          { item: "Fresh Dahi / Curd", qty: "1 Cup", notes: "Active lactic cultures" },
          { item: "Chilled Water", qty: "1/2 Cup", notes: "Spring or filtered" },
          { item: "Raw Turmeric Root", qty: "1/2 Inch", notes: "Finely grated" },
          { item: "Fresh Ginger", qty: "1/2 Inch", notes: "Crushed in mortar & pestle" },
          { item: "Roasted Cumin", qty: "1/2 tsp", notes: "Freshly ground" },
          { item: "Black Pepper", qty: "1 Pinch", notes: "Activates 2000% curcumin absorption" },
          { item: "Kala Namak", qty: "1/4 tsp", notes: "Mineral electrolyte" }
        ],
        steps: [
          "In a stainless steel jug or kulhad, add 1 cup of fresh chilled dahi.",
          "Crush the raw ginger, turmeric root, and fresh mint in a mortar and pestle to release volatile oils.",
          "Add the crushed herbs, black salt, black pepper, and roasted cumin powder to the dahi.",
          "Pour in 1/2 cup of chilled water and churn vigorously with a wooden mathani for 90 seconds until a creamy foam crowns the top.",
          "Serve in an earthen kulhad with a dusting of roasted cumin."
        ]
      },
      {
        id: "kokum-jeera-cooler",
        name: "Malabar Kokum Jeera Cooler",
        hindiName: "कोकम जीरा शर्बत",
        category: "Botanical Sharbath",
        prepTime: "3 mins",
        difficulty: "Easy (3 min)",
        temperature: "Chilled",
        desc: "Sun-dried wild kokum rinds steeped into a vibrant ruby-red liquor, spiked with roasted cumin and crushed pink peppercorns.",
        target: "Spicy biryani, heavy mutton or chicken curry, high-salt packaged meals.",
        ingredients: [
          { item: "Dried Kokum Petals", qty: "4-5 pcs", notes: "Soaked in warm water 15m" },
          { item: "Chilled Sparkling Water", qty: "200 ml", notes: "Effervescent" },
          { item: "Roasted Cumin Powder", qty: "1/2 tsp", notes: "Carminative stimulant" },
          { item: "Organic Jaggery", qty: "1 tsp", notes: "Natural minerals" },
          { item: "Himalayan Rock Salt", qty: "1/4 tsp", notes: "Electrolyte balance" }
        ],
        steps: [
          "Steep kokum petals in 1/2 cup warm water for 15 minutes, pressing occasionally to extract garcinol.",
          "Strain the deep ruby concentrate into a shaker with raw jaggery, roasted cumin, and rock salt.",
          "Stir until dissolved, then add plenty of crushed ice.",
          "Top with sparkling water and garnish with a sprig of fresh coriander."
        ]
      },
      {
        id: "triphala-golden-brew",
        name: "Ayurvedic Triphala Honey Infusion",
        hindiName: "त्रिफला अमृत काढ़ा",
        category: "Spiced Brew",
        prepTime: "8 mins",
        difficulty: "Simmer (10 min)",
        temperature: "Warm",
        desc: "Gently simmered decoction of ancient Ayurvedic triphala fruits (Amla, Haritaki, Bibhitaki) sweetened with raw mountain honey.",
        target: "Late-night carb loads, processed midnight snacks, sluggish digestion reset.",
        ingredients: [
          { item: "Triphala Churna", qty: "1/2 tsp", notes: "Whole dried fruit blend" },
          { item: "Filtered Water", qty: "1.5 Cups", notes: "Brought to boil" },
          { item: "Ceylon Cinnamon", qty: "1 Stick", notes: "Glycaemic stabilizer" },
          { item: "Cardamom Pods", qty: "2 Pods", notes: "Crushed open" },
          { item: "Raw Honey", qty: "1 tsp", notes: "Added after brew cools" }
        ],
        steps: [
          "In a saucepan, bring 1.5 cups of water to a boil with cinnamon and crushed cardamom.",
          "Stir in 1/2 tsp of Triphala powder and simmer gently for 5 minutes.",
          "Strain through a fine sieve into a ceramic mug.",
          "Allow to cool to warm drinking temperature, then stir in raw honey. Sip slowly."
        ]
      },
      {
        id: "spearmint-kombucha-spritz",
        name: "Live Spearmint & Kokum Spritzer",
        hindiName: "पुदीना कोकम स्प्रिट्ज़र",
        category: "Hydration Tonic",
        prepTime: "2 mins",
        difficulty: "Easy (3 min)",
        temperature: "Chilled",
        desc: "Effervescent fusion of steeped spearmint tea, fermented botanical kombucha, and raw lime zest.",
        target: "Paneer butter masala, cheese naan, pasta or pizza.",
        ingredients: [
          { item: "Fresh Spearmint", qty: "12 leaves", notes: "Bruised gently" },
          { item: "Live Green Tea Kombucha", qty: "150 ml", notes: "Active SCOBY cultures" },
          { item: "Fresh Lime Juice", qty: "1 tbsp", notes: "Freshly squeezed" },
          { item: "Lime Peel Zest", qty: "1 Pinch", notes: "Rich in limonene" },
          { item: "Ice Cubes", qty: "1 Cup", notes: "Artisanal clear ice" }
        ],
        steps: [
          "In a highball glass, muddle spearmint leaves with fresh lime juice and zest.",
          "Fill the glass with ice cubes.",
          "Pour live kombucha slowly down the side of the glass to retain sparkle.",
          "Stir gently once and serve immediately."
        ]
      }
    ];

    const MEALS = [
      {
        id: "noodles-coke",
        name: "Instant Noodles & Chilled Cola",
        category: "Late-Night Hostel Mess / Ultra-Processed",
        image: "https://images.unsplash.com/photo-1612927601601-6638404737ce?auto=format&fit=crop&w=800&q=80",
        shortDesc: "Refined wheat noodles fried in palm oil with MSG seasoning pack, accompanied by high-fructose carbonated beverage.",
        calories: 640,
        protein: "8.5g",
        carbs: "94g",
        fiber: "1.4g (Critical Deficit)",
        processedScore: 92,
        recommendedProduct: PRODUCTS[1], // GOLDEN HOUR
        freshAlt: "Fresh Haldi-Ginger Chaas with roasted jeera and black salt.",
        rationale: "Black pepper's piperine increases curcumin bioavailability by 2000%, actively downregulating postprandial inflammatory cascades from high-glycaemic meals.",
        scores: [
          { id: "fiber", name: "Fibre Forager", vote: "URGENT GAP", score: 12, bg: "bg-[#A92348]", text: "text-white", msg: "Critical fiber deficit (<2g). Microbial species like Bacteroides and Faecalibacterium are starved of non-digestible polysaccharides." },
          { id: "ferment", name: "Ferment Scout", vote: "DEFICIT", score: 0, bg: "bg-[#FF9D36]", text: "text-[#211A2A]", msg: "Zero live cultures or fermented food present. Gut ecosystem lacks active microbial replenishment." },
          { id: "sugar", name: "Sugar Sentry", vote: "URGENT GAP", score: 18, bg: "bg-[#A92348]", text: "text-white", msg: "42g of liquid simple sugars causes rapid glycaemic excursion and inflammatory signalling." },
          { id: "diversity", name: "Diversity Botanist", vote: "DEFICIT", score: 14, bg: "bg-[#FF9D36]", text: "text-[#211A2A]", msg: "Only 2 plant species detected. Microbiome diversity thrives on 30+ distinct botanical sources weekly." }
        ]
      },
      {
        id: "paneer-rice",
        name: "Paneer Rice Bowl with Spiced Gravy",
        category: "Campus Canteen Vegetarian Classic",
        image: "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80",
        shortDesc: "Golden seared cottage cheese cubes simmered in spiced onion-tomato butter gravy over fragrant steamed basmati rice.",
        calories: 580,
        protein: "22g",
        carbs: "62g",
        fiber: "4.8g (Moderate)",
        processedScore: 38,
        recommendedProduct: PRODUCTS[5], // MINT CONDITION
        freshAlt: "Chilled Mint-Jeera Buttermilk with hand-crushed curry leaves.",
        rationale: "Spearmint's carvone and lime's limonene cut cleanly through heavy casein fats, while stimulating peristaltic motility and bile secretion.",
        scores: [
          { id: "fiber", name: "Fibre Forager", vote: "ADEQUATE", score: 62, bg: "bg-[#E9BD48]", text: "text-[#211A2A]", msg: "Moderate fiber baseline from onions, tomatoes and whole spices, though roughage could be bolstered." },
          { id: "ferment", name: "Ferment Scout", vote: "DEFICIT", score: 25, bg: "bg-[#FF9D36]", text: "text-[#211A2A]", msg: "Rich cooked dairy meal lacks living lactic acid probiotic strains to optimize lactose assimilation." },
          { id: "sugar", name: "Sugar Sentry", vote: "THRIVING", score: 85, bg: "bg-[#70B96B]", text: "text-[#211A2A]", msg: "No refined sugars. Fat-protein matrix produces a smooth, prolonged glucose curve." },
          { id: "diversity", name: "Diversity Botanist", vote: "ADEQUATE", score: 68, bg: "bg-[#E9BD48]", text: "text-[#211A2A]", msg: "Good spice diversity (cinnamon, cloves, cumin, tomato, onion). Adding fresh herb volatiles would complete the spectrum." }
        ]
      },
      {
        id: "balanced-thali",
        name: "Homemade Balanced Dal-Roti Thali",
        category: "Whole Food Subcontinental Thali",
        image: "https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=800&q=80",
        shortDesc: "Yellow moong dal tadka with ghee, 2 whole-wheat rotis, spiced bhindi (okra), fresh cucumber salad, and homemade dahi (curd).",
        calories: 510,
        protein: "24g",
        carbs: "72g",
        fiber: "12.4g (Excellent)",
        processedScore: 12,
        recommendedProduct: PRODUCTS[4], // RUBY RUSH
        freshAlt: "Wild Kokum & Rose Petal Sharbath with crushed chia seeds.",
        rationale: "Pomegranate punicalagins convert into Urolithin A inside a high-diversity gut microbiome like this one, maximizing longevity metabolites.",
        scores: [
          { id: "fiber", name: "Fibre Forager", vote: "THRIVING", score: 95, bg: "bg-[#70B96B]", text: "text-[#211A2A]", msg: "Exceptional prebiotic fiber (12.4g) combining resistant starches, legume galactooligosaccharides, and okra mucilage." },
          { id: "ferment", name: "Ferment Scout", vote: "THRIVING", score: 92, bg: "bg-[#70B96B]", text: "text-[#211A2A]", msg: "Live homemade curd introduces robust commensal bacteria that colonize smoothly in the presence of lentil prebiotics." },
          { id: "sugar", name: "Sugar Sentry", vote: "THRIVING", score: 96, bg: "bg-[#70B96B]", text: "text-[#211A2A]", msg: "Zero added sugars. High fiber blunts post-meal insulin response completely." },
          { id: "diversity", name: "Diversity Botanist", vote: "THRIVING", score: 90, bg: "bg-[#70B96B]", text: "text-[#211A2A]", msg: "Over 8 plant and spice species present in one seating. Outstanding nutritional density." }
        ]
      }
    ];

    let currentMeal = MEALS[0];

    // ==========================================
    // HERO SCROLL ANIMATION
    // ==========================================
    const heroTrack = document.getElementById("hero-track");
    const frontCan = document.getElementById("hero-front-can");
    const rearCan = document.getElementById("hero-rear-can");
    const heroTypo = document.getElementById("hero-typo");
    const heroBottom = document.getElementById("hero-bottom");

    // ==========================================
    // REAL-TIME 3D THREE.JS WEBGL ENGINE
    // ==========================================
    let threeInitialized = false;
    let frontCanGroup = null;
    let rearCanGroup = null;
    let threeRenderer = null;
    let threeScene = null;
    let threeCamera = null;

    function initThreeHero() {
      if (typeof THREE === "undefined") return;
      const canvas = document.getElementById("hero-webgl-canvas");
      if (!canvas) return;

      try {
        threeScene = new THREE.Scene();
        threeCamera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.1, 100);
        threeCamera.position.set(0, 0, 7.6);

        threeRenderer = new THREE.WebGLRenderer({
          canvas: canvas,
          alpha: true,
          antialias: true,
          powerPreference: "high-performance"
        });
        threeRenderer.setSize(window.innerWidth, window.innerHeight);
        threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

        // Studio Lighting
        const ambient = new THREE.AmbientLight(0xffffff, 1.4);
        threeScene.add(ambient);

        const keyLight = new THREE.DirectionalLight(0xffffff, 2.4);
        keyLight.position.set(4, 6, 6);
        threeScene.add(keyLight);

        const fillLight = new THREE.DirectionalLight(0xe6f0ff, 1.2);
        fillLight.position.set(-5, 2, 4);
        threeScene.add(fillLight);

        const rimLight = new THREE.SpotLight(0xfff1d9, 2.8, 20, 0.6, 0.7);
        rimLight.position.set(0, 6, -5);
        threeScene.add(rimLight);

        const underBounce = new THREE.DirectionalLight(0xffd52a, 0.6);
        underBounce.position.set(0, -4, 2);
        threeScene.add(underBounce);

        // Procedural 3D Beverage Can Mesh Builder
        function build3DCan(textureDataUri) {
          const group = new THREE.Group();
          const loader = new THREE.TextureLoader();
          const texture = loader.load(textureDataUri);
          texture.wrapS = THREE.RepeatWrapping;
          texture.wrapT = THREE.ClampToEdgeWrapping;

          const labelMat = new THREE.MeshStandardMaterial({
            map: texture,
            roughness: 0.30,
            metalness: 0.22
          });

          const metalMat = new THREE.MeshStandardMaterial({
            color: 0xd8e0e8,
            roughness: 0.18,
            metalness: 0.92
          });

          // 1. Printed Cylinder Body
          const bodyGeom = new THREE.CylinderGeometry(1.0, 1.0, 2.7, 48, 1, true);
          const bodyMesh = new THREE.Mesh(bodyGeom, labelMat);
          bodyMesh.rotation.y = Math.PI / 2;
          group.add(bodyMesh);

          // 2. Top Neck Taper
          const neckGeom = new THREE.CylinderGeometry(0.88, 1.0, 0.27, 48);
          const neckMesh = new THREE.Mesh(neckGeom, metalMat);
          neckMesh.position.y = 1.35 + 0.27 / 2;
          group.add(neckMesh);

          // 3. Top Rim / Chime
          const rimGeom = new THREE.TorusGeometry(0.89, 0.04, 16, 48);
          rimGeom.rotateX(Math.PI / 2);
          const rimMesh = new THREE.Mesh(rimGeom, metalMat);
          rimMesh.position.y = 1.62;
          group.add(rimMesh);

          // 4. Recessed Lid
          const lidGeom = new THREE.CylinderGeometry(0.84, 0.84, 0.02, 48);
          const lidMesh = new THREE.Mesh(lidGeom, metalMat);
          lidMesh.position.y = 1.60;
          group.add(lidMesh);

          // 5. Pull Tab
          const tabGeom = new THREE.BoxGeometry(0.2, 0.02, 0.4);
          const tabMesh = new THREE.Mesh(tabGeom, metalMat);
          tabMesh.position.set(0, 1.63, 0.1);
          tabMesh.rotation.x = -0.05;
          group.add(tabMesh);

          // 6. Bottom Neck Taper
          const baseTaperGeom = new THREE.CylinderGeometry(1.0, 0.88, 0.27, 48);
          const baseTaperMesh = new THREE.Mesh(baseTaperGeom, metalMat);
          baseTaperMesh.position.y = -1.35 - 0.27 / 2;
          group.add(baseTaperMesh);

          // 7. Bottom Rim
          const baseRimGeom = new THREE.TorusGeometry(0.88, 0.035, 16, 48);
          baseRimGeom.rotateX(Math.PI / 2);
          const baseRimMesh = new THREE.Mesh(baseRimGeom, metalMat);
          baseRimMesh.position.y = -1.62;
          group.add(baseRimMesh);

          // 8. Bottom Concave Dome
          const domeGeom = new THREE.CylinderGeometry(0.82, 0.82, 0.02, 32);
          const domeMesh = new THREE.Mesh(domeGeom, metalMat);
          domeMesh.position.y = -1.60;
          group.add(domeMesh);

          return group;
        }

        // Build both products with authentic packaging textures
        frontCanGroup = build3DCan("assets/can1-texture.png");
        rearCanGroup = build3DCan("assets/can2-texture.png");

        threeScene.add(rearCanGroup);
        threeScene.add(frontCanGroup);

        // Hide 2D elements when 3D WebGL is initialized
        if (frontCan) frontCan.style.opacity = "0";
        if (rearCan) rearCan.style.opacity = "0";

        window.addEventListener("resize", () => {
          if (threeCamera && threeRenderer) {
            threeCamera.aspect = window.innerWidth / window.innerHeight;
            threeCamera.updateProjectionMatrix();
            threeRenderer.setSize(window.innerWidth, window.innerHeight);
          }
        });

        threeInitialized = true;
      } catch (err) {
        console.warn("WebGL initialization note, using high-res fallback:", err);
      }
    }

    let idleTime = 0;
    function updateHeroScroll() {
      const rect = heroTrack.getBoundingClientRect();
      const trackHeight = heroTrack.offsetHeight - window.innerHeight;
      const progress = Math.min(Math.max(-rect.top / trackHeight, 0), 1);

      idleTime += 0.03;
      const idleY = Math.sin(idleTime) * 0.06;
      const idleRearY = Math.sin(idleTime + 1.2) * 0.05;

      if (threeInitialized && frontCanGroup && rearCanGroup) {
        // FRONT CAN (Mint/Citrus - Foreground)
        const exitT = Math.max(0, (progress - 0.5) / 0.5);
        const exitEase = Math.pow(exitT, 1.8);

        frontCanGroup.position.set(
          -0.62 - exitEase * 3.4,
          0.08 + idleY + progress * 0.15 - exitEase * 0.4,
          0.75 + progress * 0.1 - exitEase * 0.3
        );
        frontCanGroup.rotation.set(
          0.14 - progress * 0.12,
          -0.08 + progress * 1.85,
          -0.27 + Math.cos(idleTime) * 0.015 + progress * 0.22 - exitEase * 0.25
        );
        frontCanGroup.scale.setScalar(1.08 + progress * 0.06 - exitEase * 0.12);

        // REAR CAN (Dark Purple Botanical - Background)
        rearCanGroup.position.set(
          0.82 + exitEase * 3.4,
          -0.18 + idleRearY - progress * 0.1 - exitEase * 0.4,
          -0.25 - exitEase * 0.4
        );
        rearCanGroup.rotation.set(
          0.12 + progress * 0.08,
          0.12 - progress * 1.75,
          0.36 + Math.cos(idleTime + 0.8) * 0.012 - progress * 0.2 + exitEase * 0.22
        );
        rearCanGroup.scale.setScalar(0.98 + progress * 0.05 - exitEase * 0.1);

        threeRenderer.render(threeScene, threeCamera);
      } else {
        // 2D FALLBACK (Exact Visual Reference Angles & Motion)
        const fRot = -15.2 + progress * 55;
        const fX = progress > 0.5 ? (progress - 0.5) * -110 : 0;
        const fY = progress * 20 + idleY * 80;
        const fScale = 1 + progress * 0.05 - (progress > 0.7 ? (progress - 0.7) * 0.2 : 0);

        const rRot = 20.7 - progress * 55;
        const rX = progress > 0.5 ? (progress - 0.5) * 110 : 0;
        const rY = progress * 15 + idleRearY * 80;
        const rScale = 1 + progress * 0.04 - (progress > 0.7 ? (progress - 0.7) * 0.2 : 0);

        if (frontCan) frontCan.style.transform = `translate3d(${fX}%, ${fY}px, 0) rotate(${fRot}deg) scale(${fScale})`;
        if (rearCan) rearCan.style.transform = `translate3d(${rX}%, ${rY}px, 0) rotate(${rRot}deg) scale(${rScale})`;
      }

      // Typography parallax
      if (heroTypo) {
        heroTypo.style.transform = `scale(${1 + progress * 0.06})`;
        heroTypo.style.opacity = Math.max(0.3, 1 - progress * 0.8);
      }

      // Bottom bar fade
      if (heroBottom) {
        heroBottom.style.opacity = Math.max(0, 1 - progress * 1.5);
        heroBottom.style.transform = `translateY(${progress * 30}px)`;
      }
    }

    // Try initializing Three.js on page load
    window.addEventListener("DOMContentLoaded", () => {
      initThreeHero();
      updateHeroScroll();
    });
    // Fallback trigger if DOMContentLoaded already fired
    setTimeout(() => {
      if (!threeInitialized) initThreeHero();
      updateHeroScroll();
    }, 200);

    window.addEventListener("scroll", updateHeroScroll, { passive: true });
    setInterval(updateHeroScroll, 33); // Continuous idle floating

    // ==========================================
    // CART DRAWER
    // ==========================================
    function toggleCart(open) {
      const drawer = document.getElementById("cart-drawer");
      const backdrop = document.getElementById("cart-backdrop");
      if (open) {
        backdrop.classList.remove("hidden");
        backdrop.classList.add("is-open");
        drawer.classList.add("open");
      } else {
        drawer.classList.remove("open");
        backdrop.classList.remove("is-open");
        backdrop.classList.add("hidden");
      }
    }

    // ==========================================
    // PIPELINE INTERACTION
    // ==========================================
    const PIPELINE_STAGES = [
      { step: "01", title: "YOUR MEAL", subtitle: "Natural Language Input", tagline: "Type what you ate or snap your tray", desc: "Input your dish in everyday words—whether it's hostel mess instant noodles with cola, campus canteen paneer rice, or a Sunday home-cooked thali.", badge: "INPUT STREAM", label: "User Typed:", content: '"Instant noodles + chilled Coke"', meta: "RecipeDB match: 98.4%" },
      { step: "02", title: "THE INGREDIENTS", subtitle: "Foodoscope RecipeDB Breakdown", tagline: "Deconstructed into bio-chemical constituents", desc: "Your meal is cross-referenced with Foodoscope's RecipeDB repository to isolate whole botanical ingredients, refined starches, cooking lipids, sodium levels, and free sugars.", badge: "DECONSTRUCTION", label: "Identified Components:", content: "Refined wheat maida • Palm oil • Monosodium glutamate • High-fructose corn syrup", meta: "Dietary fiber: 1.4g (Low)" },
      { step: "03", title: "THE GUT AGENTS", subtitle: "Transparent Microbe Rule Scoring", tagline: "4 simulated dietary pattern evaluators", desc: "Fibre Forager, Ferment Scout, Sugar Sentry, and Diversity Botanist cast explainable votes based on peer-reviewed diet–microbe studies.", badge: "SIMULATED AGENTS", label: "Agent Consensus:", content: "🚨 Critical Fiber Gap (-6.5g) • Zero Live Probiotics • High Free Sugar Load", meta: "Educational score: 26/100" },
      { step: "04", title: "FLAVOUR CHEMISTRY", subtitle: "FlavorDB Molecular Graph Matching", tagline: "Pairing by shared aromatic volatiles", desc: "Rather than forcing a random vitamin pill, FlavorDB queries the molecular flavor network for bio-active spices sharing volatile compounds with your meal.", badge: "MOLECULAR AFFINITY", label: "Volatile Pairing:", content: "Tellicherry Piperine + Lakadong Curcumin + Gingerols", meta: "Curcumin bio-uptake +2000%" },
      { step: "05", title: "YOUR NEXT SIP", subtitle: "The Functional Beverage Prescription", tagline: "A delicious, tailored companion drink", desc: "You receive an instant, hyper-specific beverage recommendation: either a ready-to-crack packaged GutGraph can or a 3-minute freshly churned canteen recipe.", badge: "RECOMMENDATION", label: "Formulated Pairing:", content: "GOLDEN HOUR CAN (Haldi & Black Pepper) or Fresh Haldi-Ginger Chaas", meta: "Ready to sip • 100% Explainable" }
    ];

    let currentPipelineStage = 0;
    function renderPipeline() {
      const btnContainer = document.getElementById("pipeline-buttons");
      btnContainer.innerHTML = PIPELINE_STAGES.map((s, idx) => `
        <button onclick="setPipelineStage(${idx})" class="p-4 rounded-2xl text-left border transition-all ${idx === currentPipelineStage ? 'bg-[#321078] border-[#FFD52A] shadow-lg' : 'bg-white/[0.03] border-white/10 hover:bg-white/[0.06]'}">
          <span class="font-mono text-xs font-black block mb-2 ${idx === currentPipelineStage ? 'text-[#FFD52A]' : 'text-white/40'}">${s.step}</span>
          <h3 class="font-gutgraph text-lg uppercase text-white">${s.title}</h3>
          <span class="text-[11px] text-white/60 truncate block">${s.subtitle}</span>
        </button>
      `).join("");

      const active = PIPELINE_STAGES[currentPipelineStage];
      document.getElementById("pipeline-showcase").innerHTML = `
        <div class="lg:col-span-7 space-y-5">
          <div class="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-[#FFD52A]/20 text-[#FFD52A]">
            <span>STAGE ${active.step}</span> • <span>${active.subtitle}</span>
          </div>
          <h3 class="font-gutgraph text-4xl sm:text-6xl uppercase tracking-tight text-white leading-tight">${active.tagline}</h3>
          <p class="text-base text-white/80 leading-relaxed font-normal">${active.desc}</p>
          <div class="pt-2">
            <button onclick="setPipelineStage((${currentPipelineStage} + 1) % 5)" class="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#FFD52A] hover:bg-[#ffe36e] text-[#211A2A] font-extrabold text-sm shadow-md transition-transform active:scale-95">
              <span>Explore Next Stage</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>
        </div>
        <div class="lg:col-span-5 p-6 rounded-2xl bg-[#0e002e] border border-white/10 font-mono text-xs space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-white/10">
            <span class="text-[10px] tracking-widest uppercase font-bold text-[#FFD52A]">${active.badge}</span>
            <span class="w-2 h-2 rounded-full bg-[#70B96B] animate-ping"></span>
          </div>
          <div>
            <span class="text-white/50 block text-[11px] mb-1">${active.label}</span>
            <p class="text-sm font-bold text-white bg-white/[0.04] p-3 rounded-xl border border-white/5">${active.content}</p>
          </div>
          <div class="pt-2 border-t border-white/5 flex items-center justify-between text-[11px] text-white/60">
            <span>Verified Pipeline Logic</span>
            <span class="text-white/80">${active.meta}</span>
          </div>
        </div>
      `;
    }

    function setPipelineStage(idx) {
      currentPipelineStage = idx;
      renderPipeline();
    }

    // ==========================================
    // SIP SHOP PRODUCTS
    // ==========================================
    let currentSipFilter = "ALL";
    const SIP_FILTERS = ["ALL", "TROPICAL", "AYURVEDIC", "FERMENTED", "REFRESHING"];

    function renderSipShop() {
      const filterContainer = document.getElementById("sip-filter-buttons");
      filterContainer.innerHTML = SIP_FILTERS.map(f => `
        <button onclick="setSipFilter('${f}')" class="px-4 py-2 rounded-full text-xs font-extrabold tracking-wider uppercase transition-all ${currentSipFilter === f ? 'bg-[#FFD52A] text-[#211A2A] shadow-md scale-105' : 'bg-white/10 text-white/70 hover:bg-white/20'}">
          ${f}
        </button>
      `).join("");

      const grid = document.getElementById("sip-products-grid");
      const filtered = PRODUCTS.filter(p => currentSipFilter === "ALL" || p.category === currentSipFilter);

      grid.innerHTML = filtered.map(p => `
        <div onclick="openProductModal('${p.id}')" class="group relative rounded-3xl p-8 border border-white/15 bg-gradient-to-b from-white/[0.08] to-white/[0.02] backdrop-blur-sm cursor-pointer overflow-hidden flex flex-col justify-between hover:border-white/40 transition-all duration-500 hover:-translate-y-2 hover:shadow-2xl">
          <div class="flex items-start justify-between z-10">
            <div>
              <span class="text-[11px] font-extrabold uppercase tracking-widest block" style="color: ${p.primaryColor}">${p.subtitle}</span>
              <h3 class="font-gutgraph text-3xl sm:text-4xl uppercase tracking-tight text-white mt-0.5">${p.name}</h3>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-bold bg-white/10 text-white">${p.calories} kcal</span>
          </div>

          <div class="relative w-full h-80 my-6 flex items-center justify-center">
            <div class="relative w-48 sm:w-52 h-full transition-transform duration-500 group-hover:scale-105 group-hover:rotate-2">
              <img src="${p.image}" alt="${p.name}" class="w-full h-full object-contain filter drop-shadow-[0_25px_35px_rgba(0,0,0,0.65)]" />
            </div>
          </div>

          <div class="space-y-4 pt-4 border-t border-white/10 z-10">
            <p class="text-xs text-white/80 line-clamp-2 leading-relaxed">${p.tagline}</p>
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono font-bold text-white/60">${p.volume} • ${p.abv}</span>
              <button class="flex items-center gap-1.5 text-xs font-extrabold uppercase tracking-wider px-4 py-2 rounded-full bg-[#FFD52A] text-[#211A2A] group-hover:bg-white transition-colors">
                <span>View Formula</span>
              </button>
            </div>
          </div>
        </div>
      `).join("");
    }

    function setSipFilter(f) {
      currentSipFilter = f;
      renderSipShop();
    }

    function openProductModal(id) {
      const p = PRODUCTS.find(x => x.id === id);
      if (!p) return;

      document.getElementById("product-modal-content").innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
          <div class="md:col-span-5 flex flex-col items-center justify-center p-6 rounded-2xl bg-white/[0.03] border border-white/10">
            <div class="relative w-48 sm:w-56 h-[340px] mb-4">
              <img src="${p.image}" alt="${p.name}" class="w-full h-full object-contain filter drop-shadow-[0_20px_35px_rgba(0,0,0,0.6)]" />
            </div>
            <div class="flex items-center gap-3 w-full justify-center text-xs font-semibold uppercase">
              <span class="px-3 py-1 rounded-full bg-white/10">${p.volume}</span>
              <span class="px-3 py-1 rounded-full bg-white/10">${p.abv}</span>
              <span class="px-3 py-1 rounded-full bg-[#FFD52A]/20 text-[#FFD52A]">${p.calories} kcal</span>
            </div>
          </div>

          <div class="md:col-span-7 space-y-6">
            <div>
              <span class="text-xs uppercase font-extrabold tracking-widest text-[#FFD52A]">${p.subtitle}</span>
              <h3 class="font-gutgraph text-4xl sm:text-5xl uppercase tracking-tight text-[#faeed6] mt-1">${p.name}</h3>
              <p class="text-base text-white/80 font-normal mt-2 leading-relaxed">${p.tagline}</p>
            </div>

            <div class="p-4 rounded-xl bg-white/[0.04] border border-white/10 space-y-1">
              <span class="text-xs font-bold uppercase tracking-wide text-[#9de0ce] block">Simulated Microbe Target:</span>
              <p class="text-sm font-semibold text-white">${p.microbe}</p>
              <p class="text-xs text-white/70 leading-relaxed">${p.microbeDesc}</p>
            </div>

            <div>
              <h4 class="text-xs uppercase font-bold tracking-wider text-white/60 mb-2.5">Key Bioactive Molecules</h4>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
                ${p.molecules.map(m => `
                  <div class="p-2.5 rounded-lg bg-white/[0.03] border border-white/5">
                    <span class="block text-xs font-bold text-[#FFD52A]">${m.name}</span>
                    <span class="block text-[11px] text-white/50">${m.source}</span>
                    <span class="block text-[10px] text-white/75 mt-1">${m.role}</span>
                  </div>
                `).join("")}
              </div>
            </div>

            <div>
              <h4 class="text-xs uppercase font-bold tracking-wider text-white/60 mb-2">Nutritional Breakdown</h4>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                <div class="p-2 rounded bg-white/[0.02] border border-white/5"><span class="text-white/50 block text-[10px]">Protein</span><span class="font-bold text-white">${p.nutrition.protein}</span></div>
                <div class="p-2 rounded bg-white/[0.02] border border-white/5"><span class="text-white/50 block text-[10px]">Total Carbs</span><span class="font-bold text-white">${p.nutrition.carbs}</span></div>
                <div class="p-2 rounded bg-white/[0.02] border border-white/5"><span class="text-white/50 block text-[10px]">Fiber</span><span class="font-bold text-[#70B96B]">${p.nutrition.fiber}</span></div>
                <div class="p-2 rounded bg-white/[0.02] border border-white/5"><span class="text-white/50 block text-[10px]">Sodium</span><span class="font-bold text-white">${p.nutrition.sodium}</span></div>
              </div>
            </div>

            <div>
              <h4 class="text-xs uppercase font-bold tracking-wider text-white/60 mb-2">Whole Ingredients</h4>
              <ul class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-xs text-white/80">
                ${p.ingredients.map(ing => `
                  <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-[#FFD52A]"></span><span>${ing}</span></li>
                `).join("")}
              </ul>
            </div>

            <div class="pt-2 border-t border-white/10 flex items-center justify-between text-xs text-white/60">
              <span>Allergens: ${p.allergens}</span>
              <span class="text-white/80">${p.context}</span>
            </div>
          </div>
        </div>
      `;

      document.getElementById("product-modal-backdrop").classList.remove("hidden");
      document.getElementById("product-modal-backdrop").classList.add("is-open", "flex");
    }

    function closeProductModal() {
      document.getElementById("product-modal-backdrop").classList.add("hidden");
      document.getElementById("product-modal-backdrop").classList.remove("is-open", "flex");
    }

    // ==========================================
    // MAKE YOUR OWN RECIPES
    // ==========================================
    let currentRecipeFilter = "ALL";
    const RECIPE_FILTERS = ["ALL", "Turmeric (Haldi)", "Ginger (Adrak)", "Kokum (Aamsul)", "Spearmint (Pudina)"];

    function renderRecipes() {
      const btnContainer = document.getElementById("recipe-filter-buttons");
      btnContainer.innerHTML = RECIPE_FILTERS.map(f => `
        <button onclick="setRecipeFilter('${f}')" class="px-3 py-1.5 rounded-full text-xs font-bold transition-colors ${currentRecipeFilter === f ? 'bg-[#FFD52A] text-[#211A2A]' : 'bg-white/10 text-white/70 hover:bg-white/20'}">
          ${f}
        </button>
      `).join("");

      const grid = document.getElementById("recipes-grid");
      const filtered = RECIPES.filter(r => {
        if (currentRecipeFilter === "ALL") return true;
        if (currentRecipeFilter.includes("Turmeric")) return r.id.includes("haldi");
        if (currentRecipeFilter.includes("Ginger")) return r.id.includes("ginger");
        if (currentRecipeFilter.includes("Kokum")) return r.id.includes("kokum");
        if (currentRecipeFilter.includes("Spearmint")) return r.id.includes("spearmint");
        return true;
      });

      grid.innerHTML = filtered.map(r => `
        <div onclick="openRecipeModal('${r.id}')" class="group relative rounded-3xl bg-gradient-to-br from-[#321078]/80 to-[#1b0642]/90 border border-white/10 p-7 sm:p-9 cursor-pointer hover:border-[#FFD52A]/50 transition-all flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-xs mb-3">
              <span class="font-extrabold uppercase tracking-widest text-[#FFD52A]">${r.category}</span>
              <div class="flex items-center gap-3 text-white/60">
                <span>⏱ ${r.prepTime}</span>
                <span>🔥 ${r.difficulty}</span>
              </div>
            </div>
            <h3 class="font-gutgraph text-3xl sm:text-4xl uppercase tracking-tight text-white group-hover:text-[#FFD52A] transition-colors">${r.name}</h3>
            <span class="block text-xs text-[#F5A6CB] mb-3">${r.hindiName}</span>
            <p class="text-sm text-white/80 leading-relaxed font-normal mb-6">${r.desc}</p>
          </div>

          <div class="pt-5 border-t border-white/10 space-y-4">
            <div class="p-3 rounded-2xl bg-white/[0.03] border border-white/5 flex items-start justify-between text-xs">
              <span class="text-white/60">Best Paired With:</span>
              <span class="text-white font-semibold text-right max-w-[200px] truncate">${r.target}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="px-3 py-1 rounded-full bg-[#70B96B]/20 text-[#70B96B] text-[11px] font-bold">${r.temperature}</span>
              <span class="text-xs font-bold uppercase tracking-wider text-[#FFD52A]">Recipe Steps →</span>
            </div>
          </div>
        </div>
      `).join("");
    }

    function setRecipeFilter(f) {
      currentRecipeFilter = f;
      renderRecipes();
    }

    function openRecipeModal(id) {
      const r = RECIPES.find(x => x.id === id);
      if (!r) return;

      document.getElementById("recipe-modal-content").innerHTML = `
        <div class="mb-6">
          <div class="flex items-center gap-3 text-xs uppercase font-extrabold tracking-widest text-[#FFD52A] mb-1">
            <span>${r.category}</span> • <span class="text-white/70">${r.hindiName}</span>
          </div>
          <h3 class="font-gutgraph text-4xl sm:text-5xl uppercase tracking-tight text-[#faeed6]">${r.name}</h3>
          <p class="text-sm text-white/80 mt-1">${r.desc}</p>
        </div>

        <div class="flex flex-wrap items-center gap-3 mb-6 text-xs font-semibold">
          <span class="px-3 py-1.5 rounded-full bg-white/10">⏱ ${r.prepTime}</span>
          <span class="px-3 py-1.5 rounded-full bg-white/10">🔥 ${r.difficulty}</span>
          <span class="px-3 py-1.5 rounded-full bg-[#70B96B]/20 text-[#70B96B]">${r.temperature}</span>
        </div>

        <div class="p-4 rounded-2xl bg-[#FFD52A]/10 border border-[#FFD52A]/20 mb-6 text-xs">
          <span class="font-bold text-[#FFD52A] block uppercase tracking-wider mb-1">Ideal Meal Antidote:</span>
          <p class="text-white/90">${r.target}</p>
        </div>

        <div class="mb-8">
          <h4 class="text-sm font-bold uppercase tracking-wider text-white/60 mb-3">Fresh Ingredients</h4>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            ${r.ingredients.map(ing => `
              <div class="p-2.5 rounded-xl bg-white/[0.03] border border-white/5 flex items-start justify-between gap-2">
                <div><span class="font-bold text-white block">${ing.item}</span><span class="text-[11px] text-white/50">${ing.notes}</span></div>
                <span class="font-mono text-[#FFD52A]">${ing.qty}</span>
              </div>
            `).join("")}
          </div>
        </div>

        <div>
          <h4 class="text-sm font-bold uppercase tracking-wider text-white/60 mb-3">Preparation Ritual</h4>
          <ol class="space-y-3 text-xs sm:text-sm text-white/85">
            ${r.steps.map((st, i) => `
              <li class="flex items-start gap-3 p-3 rounded-xl bg-white/[0.02] border border-white/5">
                <span class="w-6 h-6 rounded-full bg-[#321078] text-[#FFD52A] font-bold text-xs flex items-center justify-center flex-shrink-0">${i + 1}</span>
                <span class="leading-relaxed">${st}</span>
              </li>
            `).join("")}
          </ol>
        </div>
      `;

      document.getElementById("recipe-modal-backdrop").classList.remove("hidden");
      document.getElementById("recipe-modal-backdrop").classList.add("is-open", "flex");
    }

    function closeRecipeModal() {
      document.getElementById("recipe-modal-backdrop").classList.add("hidden");
      document.getElementById("recipe-modal-backdrop").classList.remove("is-open", "flex");
    }

    // ==========================================
    // MEAL LAB & ANALYSIS SYNC
    // ==========================================
    function renderMealLab() {
      const grid = document.getElementById("meal-scenarios-grid");
      grid.innerHTML = MEALS.map(m => `
        <div onclick="selectMeal('${m.id}')" class="group relative rounded-3xl p-6 border cursor-pointer transition-all flex flex-col justify-between overflow-hidden ${m.id === currentMeal.id ? 'bg-[#321078] border-[#FFD52A] shadow-xl scale-[1.02]' : 'bg-white/[0.03] border-white/10 hover:bg-white/[0.06]'}">
          <div>
            <div class="relative w-full h-40 rounded-2xl overflow-hidden mb-4">
              <img src="${m.image}" alt="${m.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
              ${m.id === currentMeal.id ? '<div class="absolute top-3 right-3 px-3 py-1 rounded-full bg-[#FFD52A] text-[#211A2A] text-xs font-bold shadow-md">✓ Active</div>' : ''}
            </div>
            <span class="text-[11px] font-bold uppercase tracking-wider text-[#FFD52A] block mb-1">${m.category}</span>
            <h3 class="font-gutgraph text-2xl uppercase tracking-tight text-white mb-2">${m.name}</h3>
            <p class="text-xs text-white/75 leading-relaxed line-clamp-2">${m.shortDesc}</p>
          </div>
          <div class="pt-4 border-t border-white/10 mt-4 flex items-center justify-between text-xs">
            <span class="text-white/50">${m.calories} kcal</span>
            <span class="font-bold text-[#FFD52A]">Simulate Pipeline →</span>
          </div>
        </div>
      `).join("");

      document.getElementById("active-meal-banner").innerHTML = `
        <div class="md:col-span-8 space-y-3">
          <span class="text-xs uppercase font-extrabold tracking-widest text-[#70B96B]">Active Meal Under Simulation:</span>
          <h3 class="font-gutgraph text-3xl sm:text-4xl uppercase text-white">${currentMeal.name}</h3>
          <p class="text-xs sm:text-sm text-white/80 leading-relaxed font-normal">${currentMeal.shortDesc}</p>
          <div class="flex flex-wrap gap-2 pt-2 text-xs">
            <span class="px-3 py-1 rounded-full bg-white/10 font-mono">Protein: ${currentMeal.protein}</span>
            <span class="px-3 py-1 rounded-full bg-white/10 font-mono">Carbs: ${currentMeal.carbs}</span>
            <span class="px-3 py-1 rounded-full bg-white/10 font-mono">Fiber: ${currentMeal.fiber}</span>
            <span class="px-3 py-1 rounded-full bg-[#FFD52A]/20 text-[#FFD52A] font-mono font-bold">Ultra-Processed Index: ${currentMeal.processedScore}/100</span>
          </div>
        </div>
        <div class="md:col-span-4 flex flex-col items-start md:items-end justify-center">
          <a href="#gut-agents" class="px-6 py-3.5 rounded-full bg-[#FFD52A] hover:bg-[#ffe36e] text-[#211A2A] font-extrabold text-xs uppercase tracking-wider transition-all shadow-md">
            View Agent Votes Below ↓
          </a>
        </div>
      `;

      renderGutAgents();
      renderRecommendation();
    }

    function selectMeal(id) {
      const m = MEALS.find(x => x.id === id);
      if (m) {
        currentMeal = m;
        renderMealLab();
      }
    }

    const API_BASE = (location.port === "8000" || location.hostname === "127.0.0.1" && location.port === "8000")
      ? ""
      : "http://localhost:8000";

    function voteStyle(score) {
      if (score >= 70) return { vote: "THRIVING", bg: "bg-[#70B96B]", text: "text-[#211A2A]" };
      if (score >= 40) return { vote: "ADEQUATE", bg: "bg-[#E9BD48]", text: "text-[#211A2A]" };
      if (score >= 20) return { vote: "DEFICIT", bg: "bg-[#FF9D36]", text: "text-[#211A2A]" };
      return { vote: "URGENT GAP", bg: "bg-[#A92348]", text: "text-white" };
    }

    function applyLiveAnalysis(data, typed) {
      const gaps = (data.gaps || []).map(g => g.toLowerCase());
      const has = (needle) => gaps.some(g => g.includes(needle));
      const fibre = voteStyle(has("fibre") || has("fiber") ? 12 : 78);
      const ferment = voteStyle(has("ferment") || has("probiotic") ? 8 : 82);
      const sugar = voteStyle(has("sugar") ? 16 : 86);
      const spice = voteStyle(has("spice") ? 22 : 74);
      const drink = data.drink || {};
      const product = PRODUCTS.find(p => (drink.name || "").toLowerCase().includes(p.name.split(" ")[0].toLowerCase()))
        || currentMeal.recommendedProduct
        || PRODUCTS[1];

      currentMeal = {
        id: (data.meal && data.meal.id) || "live",
        name: (data.meal && data.meal.name) || typed,
        category: "Live GutGraph engine",
        image: currentMeal.image,
        shortDesc: ((data.meal && data.meal.ingredients) || []).map(i => i.name || i).join(", ") || typed,
        calories: Math.round((10 - (data.gut_score || 0)) * 80 + 400),
        protein: "—",
        carbs: "—",
        fiber: has("fibre") || has("fiber") ? "Low (engine)" : "Adequate (engine)",
        processedScore: Math.max(0, Math.round((10 - (data.gut_score || 0)) * 10)),
        recommendedProduct: product,
        freshAlt: drink.prep || currentMeal.freshAlt,
        rationale: drink.explanation || `Gut score ${data.gut_score}/10. Gaps: ${(data.gaps || []).join(", ") || "none"}.`,
        scores: [
          { id: "fiber", name: "Fibre Forager", score: fibre.vote === "URGENT GAP" ? 12 : fibre.vote === "THRIVING" ? 78 : 48, ...fibre, msg: has("fibre") || has("fiber") ? "Engine flagged low fibre." : "Fibre looks adequate for this plate." },
          { id: "ferment", name: "Ferment Scout", score: ferment.vote === "URGENT GAP" || ferment.vote === "DEFICIT" ? 10 : 82, ...ferment, msg: has("ferment") || has("probiotic") ? "No fermented food or live cultures detected." : "A ferment or culture is on the plate." },
          { id: "sugar", name: "Sugar Sentry", score: sugar.vote === "URGENT GAP" ? 16 : 86, ...sugar, msg: has("sugar") ? "Too much sugar for this meal." : "Sugar load stays inside the rule." },
          { id: "diversity", name: "Diversity Botanist", score: spice.vote === "DEFICIT" || spice.vote === "URGENT GAP" ? 18 : 74, ...spice, msg: has("spice") ? "Spice families are too narrow." : "Spice diversity clears the bar." }
        ]
      };
      renderMealLab();
      const rec = document.getElementById("recommendation");
      if (rec) rec.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function fallbackMeal(val) {
      if (val.includes("noodle") || val.includes("coke") || val.includes("maggi") || val.includes("pizza") || val.includes("burger")) {
        selectMeal("noodles-coke");
      } else if (val.includes("paneer") || val.includes("rice") || val.includes("biryani") || val.includes("curry") || val.includes("rajma")) {
        selectMeal("paneer-rice");
      } else if (val.includes("idli") || val.includes("thali") || val.includes("dal")) {
        selectMeal("balanced-thali");
      } else {
        selectMeal("noodles-coke");
      }
    }

    async function handleMealSubmit(e) {
      e.preventDefault();
      const raw = document.getElementById("meal-input").value.trim();
      if (!raw) return;
      const val = raw.toLowerCase();

      const progressBox = document.getElementById("meal-analyzing-progress");
      const progressBar = document.getElementById("meal-progress-bar");
      const progressText = document.getElementById("meal-progress-text");

      progressBox.classList.remove("hidden");
      progressBox.classList.add("is-open");
      progressBar.style.width = "35%";
      progressText.innerText = "Asking the gut engine…";

      try {
        const res = await fetch(API_BASE + "/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ meal_text: raw })
        });
        if (!res.ok) throw new Error("analyze " + res.status);
        const data = await res.json();
        progressBar.style.width = "100%";
        progressText.innerText = "Gut score " + data.gut_score + "/10";
        setTimeout(() => {
          progressBox.classList.add("hidden");
          progressBox.classList.remove("is-open");
          applyLiveAnalysis(data, raw);
        }, 280);
      } catch (err) {
        progressBar.style.width = "100%";
        progressText.innerText = "Engine offline — using the on-page scenario";
        setTimeout(() => {
          progressBox.classList.add("hidden");
          progressBox.classList.remove("is-open");
          fallbackMeal(val);
        }, 400);
      }
    }

    // ==========================================
    // GUT AGENTS
    // ==========================================
    const AGENTS_INFO = [
      { id: "fiber", name: "Fibre Forager", icon: "🌾", label: "Prebiotic Density", taxa: ["Faecalibacterium prausnitzii", "Bacteroides thetaiotaomicron"], rule: "Calculates grams of non-starch polysaccharides and resistant starch per 500 kcal intake.", premise: "Educational model representing commensal colonic taxa that ferment non-digestible polysaccharides into short-chain fatty acids.", advice: "Pair meals lacking dietary fiber with inulin-rich cold-pressed fruit extracts or prebiotic seed infusions." },
      { id: "ferment", name: "Ferment Scout", icon: "🏺", label: "Live Culture Presence", taxa: ["Lactobacillus delbrueckii", "Streptococcus thermophilus"], rule: "Checks for presence of unpasteurized/live fermented botanical or dairy inputs.", premise: "Heuristic scoring whether live cultures, cultured dairy, or wild-fermented foods are present to enrich transit.", advice: "Add a glass of cultured masala chaas or a fermented kokum tonic immediately after dense meals." },
      { id: "sugar", name: "Sugar Sentry", icon: "🛡️", label: "Glycaemic Stability", taxa: ["Akkermansia muciniphila", "Bacteroides vulgatus"], rule: "Tracks the ratio of free liquid sugars to fiber/protein buffering. Severe penalty when free sugars > 20g.", premise: "Models mucosal stress created when high concentrations of simple sugars bypass upper absorption.", advice: "Switch away from high-fructose sodas to unsweetened botanical spritzers carrying tart organic acids." },
      { id: "diversity", name: "Diversity Botanist", icon: "🌿", label: "Botanical Taxa Count", taxa: ["Eubacterium hallii", "Gordonibacter urolithinfaciens"], rule: "Counts unique plant species across herbs, spices, vegetables, fruits, and legumes.", premise: "Inspired by the American Gut Project: human microbiomes exposed to 30+ plant species weekly demonstrate peak resilience.", advice: "Incorporate micro-dosed Indian whole spices (Tellicherry pepper, fennel, turmeric) into everyday hydration." }
    ];

    let selectedAgentId = "fiber";

    function renderGutAgents() {
      document.getElementById("agent-active-meal-desc").innerHTML = `
        Four simulated microbial heuristics audit your active meal: <span class="font-bold text-white underline decoration-[#FFD52A]">${currentMeal.name}</span>. Click each agent to inspect their transparent scoring logic.
      `;

      const grid = document.getElementById("agents-grid");
      grid.innerHTML = currentMeal.scores.map(s => {
        const isSel = s.id === selectedAgentId;
        const agInfo = AGENTS_INFO.find(a => a.id === s.id);
        return `
          <div onclick="selectAgent('${s.id}')" class="rounded-3xl p-6 sm:p-7 border cursor-pointer transition-all flex flex-col justify-between overflow-hidden ${isSel ? 'bg-[#321078] border-[#FFD52A] shadow-xl' : 'bg-white/[0.03] border-white/10 hover:bg-white/[0.06]'}">
            <div>
              <div class="flex items-center justify-between mb-4">
                <span class="text-3xl p-2 rounded-2xl bg-white/10">${agInfo.icon}</span>
                <span class="text-[10px] font-extrabold uppercase tracking-widest px-2.5 py-1 rounded-full ${s.bg} ${s.text}">${s.vote}</span>
              </div>
              <h3 class="font-gutgraph text-2xl uppercase tracking-tight text-white mb-1">${s.name}</h3>
              <span class="block text-xs text-[#FFD52A] font-semibold mb-3">${agInfo.label}</span>
              <p class="text-xs text-white/75 leading-relaxed line-clamp-3">${s.msg}</p>
            </div>
            <div class="pt-4 border-t border-white/10 mt-6">
              <div class="flex items-center justify-between text-xs font-mono">
                <span class="text-white/50">Score</span>
                <span class="font-extrabold text-[#FFD52A]">${s.score}/100</span>
              </div>
              <div class="w-full h-1.5 rounded-full bg-white/10 mt-1.5 overflow-hidden">
                <div class="h-full bg-gradient-to-r from-[#A92348] via-[#FFD52A] to-[#70B96B]" style="width: ${s.score}%"></div>
              </div>
            </div>
          </div>
        `;
      }).join("");

      const ag = AGENTS_INFO.find(a => a.id === selectedAgentId) || AGENTS_INFO[0];
      const voteData = currentMeal.scores.find(s => s.id === selectedAgentId);

      document.getElementById("agent-detail-panel").innerHTML = `
        <div class="md:col-span-5 space-y-4">
          <div class="flex items-center gap-3">
            <span class="text-4xl">${ag.icon}</span>
            <div>
              <h4 class="font-gutgraph text-3xl uppercase text-white">${ag.name}</h4>
              <span class="text-xs text-[#FFD52A] font-bold uppercase tracking-wider block">${ag.label}</span>
            </div>
          </div>
          <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/5 space-y-2">
            <span class="text-[11px] font-bold uppercase tracking-wider text-white/50 block">Simulated Bacterial Taxa Modeled:</span>
            <ul class="space-y-1 text-xs text-white/80 font-mono">
              ${ag.taxa.map(t => `<li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-[#70B96B]"></span><span class="italic">${t}</span></li>`).join("")}
            </ul>
          </div>
          <div class="p-4 rounded-2xl bg-[#FFD52A]/10 border border-[#FFD52A]/20 text-xs">
            <span class="font-bold text-[#FFD52A] block uppercase mb-1">Actionable Beverage Pairing Goal:</span>
            <p class="text-white/90">${ag.advice}</p>
          </div>
        </div>

        <div class="md:col-span-7 space-y-5">
          <div>
            <span class="text-xs uppercase font-extrabold tracking-widest text-white/50 block mb-1">Evaluation Rule Applied to Active Meal:</span>
            <p class="text-sm text-white/90 leading-relaxed font-normal p-4 rounded-2xl bg-white/[0.03] border border-white/5">${ag.rule}</p>
          </div>
          <div>
            <span class="text-xs uppercase font-extrabold tracking-widest text-white/50 block mb-1">Scientific Literature Premise:</span>
            <p class="text-xs sm:text-sm text-white/75 leading-relaxed font-normal">${ag.premise}</p>
          </div>
          <div>
            <span class="text-xs uppercase font-extrabold tracking-widest text-white/50 block mb-2">Scoring Threshold Benchmarks:</span>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
              <div class="p-2.5 rounded-xl bg-[#70B96B]/15 border border-[#70B96B]/30"><span class="font-bold text-[#70B96B] block">Thriving</span><span class="text-[11px] text-white/80">≥ 10g prebiotic fiber</span></div>
              <div class="p-2.5 rounded-xl bg-[#E9BD48]/15 border border-[#E9BD48]/30"><span class="font-bold text-[#E9BD48] block">Adequate</span><span class="text-[11px] text-white/80">5g - 9g fiber</span></div>
              <div class="p-2.5 rounded-xl bg-[#A92348]/15 border border-[#A92348]/30"><span class="font-bold text-[#A92348] block">Deficit</span><span class="text-[11px] text-white/80">&lt; 4g fiber deficit</span></div>
            </div>
          </div>
        </div>
      `;
    }

    function selectAgent(id) {
      selectedAgentId = id;
      renderGutAgents();
    }

    // ==========================================
    // FLAVOUR CHEMISTRY LAB
    // ==========================================
    const FLAVOUR_NODES = [
      { id: "turmeric", name: "Lakadong Turmeric", color: "#E9BD48", count: 130, notes: "Warm, earthy, slightly bitter, woody undertones.", volatiles: ["Curcumin", "Turmerone", "Zingiberene"] },
      { id: "mango", name: "Alphonso Mango", color: "#FF9D36", count: 238, notes: "Rich, floral, tropical sweetness, delicate resinous pine.", volatiles: ["Mangiferin", "Beta-Ocimene", "Limonene"] },
      { id: "black-pepper", name: "Tellicherry Black Pepper", color: "#211A2A", count: 94, notes: "Sharp, pungent, citrus warmth, woody bite.", volatiles: ["Piperine", "Beta-Caryophyllene", "Pinene"] },
      { id: "ginger", name: "Fresh Ginger", color: "#F0E8C9", count: 115, notes: "Zesty, peppery heat, lemony brightness, pungent.", volatiles: ["Gingerol", "Shogaol", "Zingiberene"] },
      { id: "kokum", name: "Malabar Kokum", color: "#A92348", count: 82, notes: "Deep tart acidity, subtle berry sweetness, astringent tannin.", volatiles: ["Garcinol", "Hydroxycitric Acid", "Anthocyanins"] },
      { id: "chaas", name: "Cultured Buttermilk", color: "#80B98B", count: 76, notes: "Creamy, tangy, cooling, savory fermented richness.", volatiles: ["Lactic Acid", "Diacetyl", "Acetaldehyde"] },
      { id: "spearmint", name: "Wild Spearmint", color: "#70B96B", count: 110, notes: "Sweet herbaceous, icy cooling, uplifting verdant crispness.", volatiles: ["Carvone", "Limonene", "Menthol"] },
      { id: "lime", name: "Kagzi Lime", color: "#E6EF86", count: 142, notes: "High electric acidity, fragrant peel oil, sharp brightness.", volatiles: ["Limonene", "Citral", "Citric Acid"] }
    ];

    const FLAVOUR_EDGES = [
      { source: "turmeric", target: "mango", shared: 103, jaccard: 0.388, mech: "Chemical bridging: Turmeric's woody sesquiterpenes harmonize with mango's natural resinous alpha-pinene.", example: "Sunkissed & Golden Hour Cans" },
      { source: "turmeric", target: "black-pepper", shared: 48, jaccard: 0.272, mech: "Piperine blocks hepatic glucuronidation, amplifying curcumin bio-uptake by 2000%.", example: "Golden Hour Can" },
      { source: "ginger", target: "chaas", shared: 38, jaccard: 0.248, mech: "Fiery gingerols trigger TRPV1 receptors, immediately cushioned by cultured lactic acid.", example: "Desi Cool Can & Fresh Chaas" },
      { source: "spearmint", target: "lime", shared: 62, jaccard: 0.326, mech: "Limonene activates salivary gustatory receptors while Carvone triggers TRPM8 cooling receptors.", example: "Mint Condition Can" },
      { source: "kokum", target: "chaas", shared: 32, jaccard: 0.254, mech: "Malabar kokum garcinol dissolves readily in cultured emulsion, creating the Solkadhi digestive shield.", example: "Ruby Rush & Solkadhi" }
    ];

    let activeFlavourNode = "turmeric";

    function renderFlavourLab() {
      const cloud = document.getElementById("flavour-nodes-cloud");
      cloud.innerHTML = FLAVOUR_NODES.map(n => `
        <button onclick="setFlavourNode('${n.id}')" class="px-4 py-2.5 rounded-full text-xs font-extrabold tracking-wider transition-all border flex items-center gap-2 ${n.id === activeFlavourNode ? 'bg-[#FFD52A] text-[#211A2A] border-[#FFD52A] shadow-lg scale-105' : 'bg-white/[0.04] text-white/70 border-white/10 hover:bg-white/[0.08]'}">
          <span class="w-2.5 h-2.5 rounded-full" style="background-color: ${n.color}"></span>
          <span>${n.name}</span>
          <span class="text-[10px] font-mono opacity-70">(${n.count})</span>
        </button>
      `).join("");

      const node = FLAVOUR_NODES.find(n => n.id === activeFlavourNode) || FLAVOUR_NODES[0];
      document.getElementById("flavour-active-node-card").innerHTML = `
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-widest text-[#F5A6CB]">Selected Botanical Profile</span>
            <h4 class="font-gutgraph text-3xl uppercase text-white">${node.name}</h4>
          </div>
          <div class="text-right">
            <span class="text-xs text-white/50 block">Volatile Library</span>
            <span class="text-lg font-mono font-bold text-[#FFD52A]">${node.count} Molecules</span>
          </div>
        </div>
        <p class="text-xs text-white/80 leading-relaxed font-normal">${node.notes}</p>
        <div>
          <span class="text-[11px] font-bold uppercase tracking-wider text-white/50 block mb-2">Dominant Volatiles in FlavorDB:</span>
          <div class="flex flex-wrap gap-1.5">
            ${node.volatiles.map(v => `<span class="text-xs font-mono font-semibold px-2.5 py-1 rounded-md bg-white/10 text-white">⚛ ${v}</span>`).join("")}
          </div>
        </div>
      `;

      const edges = FLAVOUR_EDGES.filter(e => e.source === activeFlavourNode || e.target === activeFlavourNode);
      const edgeList = document.getElementById("flavour-edges-list");
      if (edges.length === 0) {
        edgeList.innerHTML = `<div class="p-8 rounded-2xl bg-white/[0.02] border border-white/10 text-center text-xs text-white/50">Click another node to explore its active chemical bridges.</div>`;
      } else {
        edgeList.innerHTML = edges.map(e => {
          const otherId = e.source === activeFlavourNode ? e.target : e.source;
          const other = FLAVOUR_NODES.find(n => n.id === otherId);
          return `
            <div class="p-5 rounded-2xl bg-gradient-to-br from-[#240c5e] to-[#1a0648] border border-white/15 space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2 text-sm font-bold text-white">
                  <span>${node.name}</span> ⇄ <span style="color: ${other.color}">${other.name}</span>
                </div>
                <span class="px-2.5 py-1 rounded-full text-xs font-mono font-bold bg-[#FFD52A]/15 text-[#FFD52A]">${e.shared} Shared</span>
              </div>
              <div class="text-xs space-y-1">
                <div class="flex items-center justify-between text-white/50 font-mono text-[11px]">
                  <span>Jaccard Index</span>
                  <span class="text-white font-bold">${e.jaccard}</span>
                </div>
                <div class="w-full h-1 rounded-full bg-white/10 overflow-hidden">
                  <div class="h-full bg-[#F5A6CB]" style="width: ${e.jaccard * 200}%"></div>
                </div>
              </div>
              <p class="text-xs text-white/75 leading-relaxed font-normal">${e.mech}</p>
              <div class="pt-2 border-t border-white/5 text-[11px] text-[#70B96B] font-semibold">
                ⚡ Used in: ${e.example}
              </div>
            </div>
          `;
        }).join("");
      }
    }

    function setFlavourNode(id) {
      activeFlavourNode = id;
      renderFlavourLab();
    }

    // ==========================================
    // RECOMMENDATION REVEAL
    // ==========================================
    function renderRecommendation() {
      const p = currentMeal.recommendedProduct;
      document.getElementById("recommendation-subtitle").innerText = `Based on your simulated meal (${currentMeal.name}), here is your scientifically paired GutGraph companion drink.`;

      document.getElementById("recommendation-card").innerHTML = `
        <div class="lg:col-span-5 flex flex-col items-center justify-center relative">
          <div class="relative w-56 sm:w-64 h-[420px] z-10 hover:scale-105 transition-transform duration-500">
            <img src="${p.image}" alt="${p.name}" class="w-full h-full object-contain filter drop-shadow-[0_30px_45px_rgba(0,0,0,0.7)]" />
          </div>
          <div class="flex items-center gap-3 mt-6 text-xs font-mono font-bold uppercase z-10">
            <span class="px-3.5 py-1.5 rounded-full bg-white/10 text-white">${p.volume}</span>
            <span class="px-3.5 py-1.5 rounded-full bg-white/10 text-white">${p.abv}</span>
            <span class="px-3.5 py-1.5 rounded-full bg-[#FFD52A] text-[#211A2A]">${p.calories} KCAL</span>
          </div>
        </div>

        <div class="lg:col-span-7 space-y-6">
          <div>
            <span class="text-xs uppercase font-extrabold tracking-widest block" style="color: ${p.primaryColor}">Formulated Companion Beverage</span>
            <h3 class="font-gutgraph text-5xl sm:text-6xl md:text-7xl uppercase tracking-tight text-white mt-1">${p.name}</h3>
            <p class="text-base text-white/80 font-normal mt-1 leading-relaxed">${p.tagline}</p>
          </div>

          <div class="p-5 rounded-2xl bg-white/[0.04] border border-white/10 space-y-2">
            <span class="text-xs font-bold uppercase tracking-wider text-[#FFD52A] block">Why This Beverage Was Recommended:</span>
            <p class="text-sm text-white/90 leading-relaxed font-normal">${currentMeal.rationale}</p>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
            <div class="p-3 rounded-xl bg-white/[0.03] border border-white/5"><span class="text-white/50 block text-[10px]">Prebiotic Fiber</span><span class="font-bold text-[#70B96B]">${p.nutrition.fiber}</span></div>
            <div class="p-3 rounded-xl bg-white/[0.03] border border-white/5"><span class="text-white/50 block text-[10px]">Simulated Target</span><span class="font-bold text-white truncate block">${p.microbe.split(" ")[0]}</span></div>
            <div class="p-3 rounded-xl bg-white/[0.03] border border-white/5"><span class="text-white/50 block text-[10px]">Sugar (Fruit)</span><span class="font-bold text-white">${p.calories < 25 ? 'Low' : 'Natural'}</span></div>
            <div class="p-3 rounded-xl bg-white/[0.03] border border-white/5"><span class="text-white/50 block text-[10px]">Allergen Check</span><span class="font-bold text-[#FFD52A]">${p.allergens.includes('None') ? 'Allergen-Free' : 'See Details'}</span></div>
          </div>

          <div class="p-4 rounded-xl bg-[#70B96B]/10 border border-[#70B96B]/20 text-xs flex items-center justify-between gap-4">
            <div>
              <span class="font-bold text-[#70B96B] block uppercase tracking-wider mb-0.5">Fresh Canteen Recipe Alternative:</span>
              <p class="text-white/90">${currentMeal.freshAlt}</p>
            </div>
            <a href="#make-your-own" class="flex-shrink-0 px-3.5 py-2 rounded-full bg-[#70B96B] text-[#160045] font-extrabold text-[11px] uppercase tracking-wider hover:bg-[#8fd88a]">View Recipe</a>
          </div>

          <div class="pt-2 flex flex-wrap items-center gap-4">
            <button onclick="toggleCart(true)" class="px-8 py-3.5 rounded-full bg-[#FFD52A] hover:bg-[#ffe36e] text-[#211A2A] font-extrabold text-sm uppercase tracking-wider transition-all shadow-lg flex items-center gap-2">
              <span>Add ${p.name} to Cart</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
            <a href="#sip-shop" class="px-6 py-3.5 rounded-full bg-white/10 hover:bg-white/20 text-white font-extrabold text-sm uppercase tracking-wider">Browse All 6 Cans</a>
          </div>
        </div>
      `;
    }

    // ==========================================
    // INITIALIZATION
    // ==========================================
    renderPipeline();
    renderSipShop();
    renderRecipes();
    renderMealLab();
    renderFlavourLab();
