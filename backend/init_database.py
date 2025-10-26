# init_database.py
import sqlite3
import chromadb
import os

def init_databases():
    """Initialize SQLite database and ChromaDB vector store"""
    
    # Initialize SQLite for conversation history
    init_sqlite_db()
    
    # Initialize ChromaDB for product embeddings
    init_chromadb()

def init_sqlite_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('education_store.db')
    cur = conn.cursor()
    
    # Create conversation_history table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            user_message TEXT,
            assistant_response TEXT,
            timestamp TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ SQLite database initialized successfully!")
    print("📊 Database file: education_store.db")

def init_chromadb():
    """Initialize ChromaDB with product embeddings using default embedding function"""
    
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create collection with default embedding function (all-MiniLM-L6-v2)
    collection = client.get_or_create_collection(
        name="education_products",
        metadata={"description": "Education store products with embeddings"}
    )
    
    # 50 Detailed Educational Products
    products = [
        # STEM & Science (15 items)
        {
            "id": "1", 
            "product_name": "Advanced STEM Robotics Kit", 
            "description": "Professional robotics kit with AI capabilities for advanced learners. Includes multiple sensors, programmable motors, and machine learning features. Perfect for high school and college students interested in robotics engineering.",
            "price": 149.99, 
            "category": "STEM", 
            "stock": 35, 
            "age_range": "14-18 years", 
            "brand": "RoboTech Pro",
            "features": "AI programming, Multiple sensors, Machine learning, Advanced coding"
        },
        {
            "id": "2",
            "product_name": "Digital Microscope Pro", 
            "description": "High-precision digital microscope with 2000x magnification and 4K image capture. Professional-grade tool for biology and material science studies with computer connectivity for detailed analysis.",
            "price": 129.99, 
            "category": "Science", 
            "stock": 25, 
            "age_range": "12+ years", 
            "brand": "ScienceVision",
            "features": "2000x magnification, 4K imaging, Computer connectivity, Measurement software"
        },
        {
            "id": "3",
            "product_name": "Complete Chemistry Laboratory", 
            "description": "Comprehensive chemistry set with 100+ experiments covering organic and inorganic chemistry. Includes professional glassware, safe chemicals, and digital lab manual with VR experiments.",
            "price": 189.99, 
            "category": "Science", 
            "stock": 20, 
            "age_range": "14+ years", 
            "brand": "ChemMaster",
            "features": "100+ experiments, Professional glassware, VR experiments, Safety equipment"
        },
        {
            "id": "4",
            "product_name": "Physics Master Lab", 
            "description": "Advanced physics laboratory covering mechanics, thermodynamics, optics, and electromagnetism. Includes precision instruments and data logging equipment for university-level experiments.",
            "price": 199.99, 
            "category": "Physics", 
            "stock": 18, 
            "age_range": "16+ years", 
            "brand": "PhysicsPro",
            "features": "University level, Precision instruments, Data logging, Comprehensive experiments"
        },
        {
            "id": "5",
            "product_name": "AI Programming Platform", 
            "description": "Complete AI and machine learning platform teaching Python programming with real AI projects. Includes neural network development and computer vision applications for future tech leaders.",
            "price": 89.99, 
            "category": "Technology", 
            "stock": 45, 
            "age_range": "13+ years", 
            "brand": "AI Learners",
            "features": "Machine learning, Neural networks, Computer vision, Python programming"
        },
        {
            "id": "6",
            "product_name": "Engineering Master Set", 
            "description": "Professional engineering set with 1000+ components for mechanical, civil, and electrical engineering projects. Teaches structural design, gear systems, and circuit design through hands-on building.",
            "price": 159.99, 
            "category": "Engineering", 
            "stock": 30, 
            "age_range": "12-18 years", 
            "brand": "EngineerPro",
            "features": "1000+ components, Multiple engineering fields, Structural design, Circuit building"
        },
        {
            "id": "7",
            "product_name": "Astronomy Telescope Pro", 
            "description": "Professional astronomical telescope with computerized tracking and high-resolution optics. Perfect for studying planets, stars, and deep space objects with detailed observation guides.",
            "price": 299.99, 
            "category": "Astronomy", 
            "stock": 15, 
            "age_range": "12+ years", 
            "brand": "StarGazer Pro",
            "features": "Computerized tracking, High-resolution optics, Planet observation, Star mapping"
        },
        {
            "id": "8",
            "product_name": "Advanced Electronics Lab", 
            "description": "Comprehensive electronics laboratory with microcontrollers, sensors, and IoT components. Teaches circuit design, programming, and Internet of Things development through real projects.",
            "price": 119.99, 
            "category": "Electronics", 
            "stock": 40, 
            "age_range": "14+ years", 
            "brand": "ElectroLab Pro",
            "features": "Microcontrollers, IoT development, Sensor networks, Circuit design"
        },
        {
            "id": "9",
            "product_name": "Math Mastery System", 
            "description": "Advanced mathematics learning system covering algebra, geometry, calculus, and statistics. Includes interactive software, manipulatives, and real-world problem-solving activities.",
            "price": 79.99, 
            "category": "Mathematics", 
            "stock": 60, 
            "age_range": "12-18 years", 
            "brand": "MathMaster Pro",
            "features": "Advanced math topics, Interactive software, Real-world problems, Comprehensive curriculum"
        },
        {
            "id": "10",
            "product_name": "3D Geometry Studio", 
            "description": "Interactive 3D geometry system with augmented reality features. Students can manipulate geometric shapes in virtual space and explore mathematical concepts through immersive learning.",
            "price": 69.99, 
            "category": "Mathematics", 
            "stock": 50, 
            "age_range": "10-16 years", 
            "brand": "GeoVision",
            "features": "3D modeling, Augmented reality, Shape manipulation, Interactive learning"
        },
        {
            "id": "11",
            "product_name": "Virtual Biology Lab", 
            "description": "Complete virtual biology laboratory with simulated dissections and experiments. No real specimens needed - uses detailed 3D models and realistic simulations for comprehensive biology education.",
            "price": 99.99, 
            "category": "Biology", 
            "stock": 35, 
            "age_range": "12+ years", 
            "brand": "BioLab VR",
            "features": "Virtual dissections, 3D models, Realistic simulations, No specimens needed"
        },
        {
            "id": "12",
            "product_name": "Professional Weather Station", 
            "description": "Advanced weather monitoring station with wireless sensors and predictive analytics. Measures temperature, humidity, pressure, wind, and precipitation with professional-grade accuracy.",
            "price": 149.99, 
            "category": "Meteorology", 
            "stock": 20, 
            "age_range": "12+ years", 
            "brand": "WeatherMaster",
            "features": "Wireless sensors, Predictive analytics, Professional accuracy, Multiple measurements"
        },
        {
            "id": "13",
            "product_name": "Renewable Energy Lab", 
            "description": "Comprehensive renewable energy laboratory exploring solar, wind, hydro, and hydrogen fuel cells. Build working models and analyze energy production data for environmental science studies.",
            "price": 129.99, 
            "category": "Environmental Science", 
            "stock": 25, 
            "age_range": "12+ years", 
            "brand": "EcoPower Lab",
            "features": "Multiple energy sources, Working models, Data analysis, Environmental science"
        },
        {
            "id": "14",
            "product_name": "Human Anatomy Master", 
            "description": "Detailed human anatomy model with augmented reality overlay. Includes all body systems with interactive digital content for medical and biological education at advanced levels.",
            "price": 89.99, 
            "category": "Biology", 
            "stock": 30, 
            "age_range": "14+ years", 
            "brand": "AnatomyMaster Pro",
            "features": "Augmented reality, All body systems, Interactive content, Medical accuracy"
        },
        {
            "id": "15",
            "product_name": "Geology Discovery Kit", 
            "description": "Professional geology kit with 75+ mineral and fossil specimens. Includes identification tools, geological maps, and digital learning resources for comprehensive earth science education.",
            "price": 79.99, 
            "category": "Geology", 
            "stock": 40, 
            "age_range": "10-16 years", 
            "brand": "GeoDiscover Pro",
            "features": "75+ specimens, Identification tools, Geological maps, Digital resources"
        },

        # Art & Creativity (10 items)
        {
            "id": "16",
            "product_name": "Professional Art Studio", 
            "description": "Complete professional art studio with 300+ high-quality art supplies. Includes acrylics, oils, watercolors, brushes, canvases, and drawing materials for serious art students.",
            "price": 199.99, 
            "category": "Art", 
            "stock": 25, 
            "age_range": "12+ years", 
            "brand": "ArtStudio Pro",
            "features": "300+ supplies, Professional quality, Multiple mediums, Complete studio"
        },
        {
            "id": "17",
            "product_name": "Digital Art Tablet Pro", 
            "description": "Professional digital art tablet with pressure-sensitive stylus and creative software. Perfect for digital painting, graphic design, and animation with industry-standard tools.",
            "price": 179.99, 
            "category": "Art", 
            "stock": 30, 
            "age_range": "12+ years", 
            "brand": "DigitalArt Pro",
            "features": "Pressure sensitive, Creative software, Digital painting, Animation tools"
        },
        {
            "id": "18",
            "product_name": "Pottery Wheel Studio", 
            "description": "Professional electric pottery wheel with clay tools and kiln-safe materials. Learn wheel throwing, sculpting, and ceramic art techniques with comprehensive video lessons.",
            "price": 249.99, 
            "category": "Art", 
            "stock": 15, 
            "age_range": "14+ years", 
            "brand": "ClayMaster Pro",
            "features": "Electric wheel, Kiln-safe materials, Video lessons, Professional tools"
        },
        {
            "id": "19",
            "product_name": "Watercolor Master Set", 
            "description": "Professional watercolor set with artist-grade paints, brushes, and papers. Includes techniques for wet-on-wet, glazing, and detailed watercolor painting methods.",
            "price": 89.99, 
            "category": "Art", 
            "stock": 45, 
            "age_range": "10+ years", 
            "brand": "Watercolor Pro",
            "features": "Artist grade, Professional brushes, Multiple techniques, High-quality paper"
        },
        {
            "id": "20",
            "product_name": "Sculpture & 3D Art Kit", 
            "description": "Comprehensive sculpture kit with various materials including clay, wire, wood, and found objects. Teaches 3D art techniques, form, and spatial relationships through hands-on projects.",
            "price": 69.99, 
            "category": "Art", 
            "stock": 35, 
            "age_range": "10+ years", 
            "brand": "SculptureWorks",
            "features": "Multiple materials, 3D techniques, Form studies, Spatial relationships"
        },
        {
            "id": "21",
            "product_name": "Calligraphy & Lettering Set", 
            "description": "Professional calligraphy set with various nibs, inks, and guide sheets. Learn traditional and modern lettering styles with comprehensive technique tutorials.",
            "price": 49.99, 
            "category": "Art", 
            "stock": 60, 
            "age_range": "12+ years", 
            "brand": "LetterMaster",
            "features": "Various nibs, Multiple inks, Traditional styles, Modern lettering"
        },
        {
            "id": "22",
            "product_name": "Printmaking Studio", 
            "description": "Complete printmaking studio with linoleum blocks, carving tools, and printing supplies. Learn relief printing, monoprinting, and edition making techniques.",
            "price": 79.99, 
            "category": "Art", 
            "stock": 30, 
            "age_range": "12+ years", 
            "brand": "PrintStudio Pro",
            "features": "Relief printing, Carving tools, Multiple techniques, Edition making"
        },
        {
            "id": "23",
            "product_name": "Textile Arts Laboratory", 
            "description": "Comprehensive textile arts kit with fabric painting, batik, weaving, and embroidery materials. Explore various fabric art techniques and cultural textile traditions.",
            "price": 89.99, 
            "category": "Art", 
            "stock": 40, 
            "age_range": "10+ years", 
            "brand": "TextileArts Lab",
            "features": "Fabric painting, Weaving, Embroidery, Cultural traditions"
        },
        {
            "id": "24",
            "product_name": "Digital Photography Kit", 
            "description": "Complete digital photography learning kit with camera, lenses, and editing software. Teaches composition, lighting, and post-processing for aspiring photographers.",
            "price": 299.99, 
            "category": "Art", 
            "stock": 20, 
            "age_range": "12+ years", 
            "brand": "PhotoLearn Pro",
            "features": "Digital camera, Multiple lenses, Editing software, Composition techniques"
        },
        {
            "id": "25",
            "product_name": "Animation Studio Set", 
            "description": "Complete animation studio with stop-motion equipment, software, and character building materials. Learn traditional and digital animation techniques through hands-on projects.",
            "price": 159.99, 
            "category": "Art", 
            "stock": 25, 
            "age_range": "10+ years", 
            "brand": "AnimationStudio",
            "features": "Stop-motion, Animation software, Character building, Multiple techniques"
        },

        # Books & Literature (10 items)
        {
            "id": "26",
            "product_name": "Classic Literature Collection", 
            "description": "Comprehensive collection of 50 classic literature works with study guides and analysis. Includes novels, poetry, and drama from different historical periods and cultures.",
            "price": 149.99, 
            "category": "Books", 
            "stock": 35, 
            "age_range": "12+ years", 
            "brand": "ClassicReads Pro",
            "features": "50 classic works, Study guides, Literary analysis, Historical context"
        },
        {
            "id": "27",
            "product_name": "Science Encyclopedia Pro", 
            "description": "Complete science encyclopedia with 10 volumes covering all major scientific disciplines. Includes interactive digital content and virtual experiments for comprehensive learning.",
            "price": 199.99, 
            "category": "Books", 
            "stock": 25, 
            "age_range": "10+ years", 
            "brand": "ScienceEncyclopedia Pro",
            "features": "10 volumes, All disciplines, Interactive content, Virtual experiments"
        },
        {
            "id": "28",
            "product_name": "World History Library", 
            "description": "Comprehensive world history collection spanning ancient civilizations to modern times. Includes primary sources, maps, and digital timelines for historical understanding.",
            "price": 179.99, 
            "category": "Books", 
            "stock": 30, 
            "age_range": "12+ years", 
            "brand": "HistoryLibrary Pro",
            "features": "Comprehensive history, Primary sources, Historical maps, Digital timelines"
        },
        {
            "id": "29",
            "product_name": "Mathematics Reference Set", 
            "description": "Complete mathematics reference library covering arithmetic to advanced calculus. Includes worked examples, practice problems, and step-by-step solution guides.",
            "price": 129.99, 
            "category": "Books", 
            "stock": 40, 
            "age_range": "10+ years", 
            "brand": "MathReference Pro",
            "features": "Complete coverage, Worked examples, Practice problems, Solution guides"
        },
        {
            "id": "30",
            "product_name": "Language Learning Library", 
            "description": "Comprehensive language learning system with books, audio, and digital resources for 5 languages. Uses immersive methods and cultural context for effective language acquisition.",
            "price": 159.99, 
            "category": "Books", 
            "stock": 35, 
            "age_range": "8+ years", 
            "brand": "LanguageMaster Pro",
            "features": "5 languages, Audio resources, Cultural context, Immersive methods"
        },
        {
            "id": "31",
            "product_name": "Art History Collection", 
            "description": "Comprehensive art history collection covering major movements and artists. Includes high-quality reproductions, analysis, and cultural context for art appreciation.",
            "price": 139.99, 
            "category": "Books", 
            "stock": 30, 
            "age_range": "12+ years", 
            "brand": "ArtHistory Pro",
            "features": "Major movements, Artist profiles, High-quality reproductions, Cultural context"
        },
        {
            "id": "32",
            "product_name": "Philosophy for Thinkers", 
            "description": "Complete philosophy collection introducing major philosophical ideas and thinkers. Includes primary texts, commentary, and critical thinking exercises.",
            "price": 119.99, 
            "category": "Books", 
            "stock": 25, 
            "age_range": "14+ years", 
            "brand": "PhilosophyWorks",
            "features": "Major ideas, Primary texts, Critical thinking, Philosophical exercises"
        },
        {
            "id": "33",
            "product_name": "Creative Writing Studio", 
            "description": "Complete creative writing program with guides, prompts, and workshop materials. Covers fiction, poetry, non-fiction, and script writing with professional techniques.",
            "price": 89.99, 
            "category": "Books", 
            "stock": 45, 
            "age_range": "12+ years", 
            "brand": "WriteCreative Pro",
            "features": "Writing guides, Creative prompts, Workshop materials, Multiple genres"
        },
        {
            "id": "34",
            "product_name": "Economics & Business Library", 
            "description": "Comprehensive economics and business education collection. Covers microeconomics, macroeconomics, entrepreneurship, and personal finance with real-world applications.",
            "price": 149.99, 
            "category": "Books", 
            "stock": 30, 
            "age_range": "14+ years", 
            "brand": "EconBusiness Pro",
            "features": "Economic principles, Business concepts, Entrepreneurship, Real-world applications"
        },
        {
            "id": "35",
            "product_name": "Psychology Learning System", 
            "description": "Complete psychology education system covering major theories and research methods. Includes case studies, experiments, and psychological assessment tools.",
            "price": 129.99, 
            "category": "Books", 
            "stock": 35, 
            "age_range": "14+ years", 
            "brand": "PsychologyLearn Pro",
            "features": "Major theories, Research methods, Case studies, Assessment tools"
        },

        # Electronics & Technology (8 items)
        {
            "id": "36",
            "product_name": "Educational Tablet Pro", 
            "description": "Advanced educational tablet with curated learning apps and parental controls. Includes STEM applications, creative tools, and age-appropriate content for comprehensive learning.",
            "price": 199.99, 
            "category": "Electronics", 
            "stock": 40, 
            "age_range": "5-12 years", 
            "brand": "LearnTablet Pro",
            "features": "Curated apps, Parental controls, STEM applications, Creative tools"
        },
        {
            "id": "37",
            "product_name": "Coding Laptop Pro", 
            "description": "Professional coding laptop with pre-installed development environments and programming tools. Perfect for learning multiple programming languages and software development.",
            "price": 499.99, 
            "category": "Electronics", 
            "stock": 20, 
            "age_range": "12+ years", 
            "brand": "CodeLaptop Pro",
            "features": "Development environments, Multiple languages, Programming tools, Software development"
        },
        {
            "id": "38",
            "product_name": "Interactive Smart Globe", 
            "description": "Advanced interactive globe with augmented reality features and real-time data. Explore geography, cultures, and environmental changes with dynamic digital content.",
            "price": 149.99, 
            "category": "Electronics", 
            "stock": 30, 
            "age_range": "8+ years", 
            "brand": "SmartGlobe Pro",
            "features": "Augmented reality, Real-time data, Geography exploration, Cultural content"
        },
        {
            "id": "39",
            "product_name": "VR Learning Headset", 
            "description": "Virtual reality headset with educational content across all subjects. Experience immersive learning in science, history, art, and literature through virtual environments.",
            "price": 299.99, 
            "category": "Electronics", 
            "stock": 25, 
            "age_range": "10+ years", 
            "brand": "VREducation Pro",
            "features": "Virtual reality, Immersive learning, Multiple subjects, Educational content"
        },
        {
            "id": "40",
            "product_name": "Robotics Programming Kit", 
            "description": "Advanced robotics kit with multiple programming languages and AI capabilities. Build and program complex robots with sensors, actuators, and machine learning features.",
            "price": 179.99, 
            "category": "Electronics", 
            "stock": 35, 
            "age_range": "12+ years", 
            "brand": "RoboCode Pro",
            "features": "Multiple languages, AI capabilities, Complex robots, Machine learning"
        },
        {
            "id": "41",
            "product_name": "Electronic Music Studio", 
            "description": "Complete electronic music studio with synthesizers, drum machines, and production software. Learn music theory, composition, and audio production techniques.",
            "price": 249.99, 
            "category": "Electronics", 
            "stock": 20, 
            "age_range": "12+ years", 
            "brand": "MusicStudio Pro",
            "features": "Synthesizers, Drum machines, Production software, Music theory"
        },
        {
            "id": "42",
            "product_name": "3D Printer Education Kit", 
            "description": "Educational 3D printer with design software and curriculum. Learn 3D modeling, prototyping, and manufacturing principles through hands-on projects.",
            "price": 399.99, 
            "category": "Electronics", 
            "stock": 15, 
            "age_range": "12+ years", 
            "brand": "3DPrintLearn Pro",
            "features": "3D printing, Design software, Prototyping, Manufacturing principles"
        },
        {
            "id": "43",
            "product_name": "IoT Development Platform", 
            "description": "Internet of Things development platform with sensors, controllers, and cloud connectivity. Learn IoT programming, data analysis, and smart device development.",
            "price": 129.99, 
            "category": "Electronics", 
            "stock": 30, 
            "age_range": "14+ years", 
            "brand": "IoTDeveloper Pro",
            "features": "IoT development, Cloud connectivity, Data analysis, Smart devices"
        },

        # Early Learning & Classroom (7 items)
        {
            "id": "44",
            "product_name": "Montessori Learning System", 
            "description": "Complete Montessori learning system with materials for practical life, sensorial, mathematics, and language development. Based on authentic Montessori principles and methods.",
            "price": 299.99, 
            "category": "Early Learning", 
            "stock": 25, 
            "age_range": "3-6 years", 
            "brand": "Montessori Pro",
            "features": "Practical life, Sensorial materials, Mathematics, Language development"
        },
        {
            "id": "45",
            "product_name": "Phonics Mastery System", 
            "description": "Comprehensive phonics system with multisensory materials and digital resources. Teaches letter sounds, blending, and reading fluency through engaging activities.",
            "price": 89.99, 
            "category": "Early Learning", 
            "stock": 50, 
            "age_range": "4-8 years", 
            "brand": "PhonicsMaster Pro",
            "features": "Multisensory learning, Letter sounds, Reading fluency, Digital resources"
        },
        {
            "id": "46",
            "product_name": "Early Math Discovery Set", 
            "description": "Complete early mathematics system with manipulatives, games, and digital activities. Covers counting, operations, patterns, and early geometry concepts.",
            "price": 79.99, 
            "category": "Early Learning", 
            "stock": 45, 
            "age_range": "3-7 years", 
            "brand": "EarlyMath Pro",
            "features": "Math manipulatives, Learning games, Digital activities, Multiple concepts"
        },
        {
            "id": "47",
            "product_name": "Classroom Smart Board", 
            "description": "Interactive smart board for collaborative classroom learning. Includes educational software, touch capabilities, and multi-user functionality for engaging lessons.",
            "price": 899.99, 
            "category": "Classroom", 
            "stock": 10, 
            "age_range": "All ages", 
            "brand": "SmartBoard Pro",
            "features": "Interactive display, Educational software, Touch capabilities, Multi-user"
        },
        {
            "id": "48",
            "product_name": "Teacher Resource Library", 
            "description": "Comprehensive teacher resource library with lesson plans, activities, and assessment tools. Covers all subjects and grade levels with differentiated instruction materials.",
            "price": 199.99, 
            "category": "Classroom", 
            "stock": 30, 
            "age_range": "Teacher", 
            "brand": "TeacherResource Pro",
            "features": "Lesson plans, Activities, Assessment tools, Differentiated instruction"
        },
        {
            "id": "49",
            "product_name": "STEM Classroom Kit", 
            "description": "Complete STEM classroom kit with materials for 30 students. Includes robotics, coding, engineering, and science experiments with teacher guides and curriculum.",
            "price": 599.99, 
            "category": "Classroom", 
            "stock": 15, 
            "age_range": "8-14 years", 
            "brand": "STEMClassroom Pro",
            "features": "30 students, Multiple STEM areas, Teacher guides, Complete curriculum"
        },
        {
            "id": "50",
            "product_name": "Language Lab System", 
            "description": "Complete language laboratory system with headsets, recording, and interactive software. Perfect for foreign language instruction and speech therapy applications.",
            "price": 799.99, 
            "category": "Classroom", 
            "stock": 12, 
            "age_range": "All ages", 
            "brand": "LanguageLab Pro",
            "features": "Headsets, Recording capability, Interactive software, Speech therapy"
        }
    ]
    
        # Add all products to ChromaDB
    documents = []
    metadatas = []
    ids = []
    
    for product in products:
        # Create a comprehensive document for embedding
        doc_text = f"""
        Product: {product['product_name']}
        Category: {product['category']}
        Description: {product['description']}
        Features: {product['features']}
        Age Range: {product['age_range']}
        Brand: {product['brand']}
        Price: ${product['price']}
        Stock: {product['stock']} units
        """
        
        documents.append(doc_text)
        metadatas.append(product)
        ids.append(product['id'])
    
    # Add to ChromaDB collection
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ ChromaDB initialized with {len(documents)} products!")
        print("📊 Vector database: ./chroma_db")
        
        # Verify the count
        count = collection.count()
        print(f"📈 Total products in vector store: {count}")
    else:
        print("⚠️ No products added to ChromaDB")

if __name__ == "__main__":
    init_databases()