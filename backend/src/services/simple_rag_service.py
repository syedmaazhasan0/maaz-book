"""
Simple RAG service that works without external dependencies for demo purposes
"""
from typing import List
from src.models.query_models import QueryRequest, QueryResponse


# Sample book content embedded in code for demo
BOOK_CONTENT = {
    "book_structure": """The Physical AI and Humanoid Robotics book contains the following chapters:

Chapter 1: Introduction to Physical AI - Covers the fundamentals of physical AI, embodiment, and real-world operation
Chapter 2: Humanoid Robotics Fundamentals - Discusses robot design, components, actuators, sensors, and mechanical structure
Chapter 3: Perception Systems - Explores visual perception, sensors, object detection, and depth estimation
Chapter 4: Motion Planning and Control - Details path planning, trajectory optimization, and control systems
Chapter 5: Bipedal Locomotion - Covers walking, balance, gait patterns, and the Zero Moment Point
Chapter 6: Manipulation and Grasping - Discusses grasp planning, force control, and bimanual manipulation
Chapter 7: Learning and Adaptation - Covers reinforcement learning, imitation learning, and sim-to-real transfer
Chapter 8: Human-Robot Interaction - Explores natural language processing, gesture recognition, and safe interaction
Chapter 9: Hardware Platforms - Reviews major humanoid robots including Atlas, ASIMO, Pepper, Digit, and Optimus
Chapter 10: Applications and Future Directions - Discusses use cases in healthcare, manufacturing, and exploration
Chapter 11: Challenges and Research Frontiers - Addresses robustness, energy efficiency, and ethical considerations""",

    "physical_ai": """Chapter 1: Introduction to Physical AI

Physical AI refers to artificial intelligence systems that interact with and navigate the physical world. Unlike traditional AI that operates purely in digital environments, physical AI systems must deal with real-world constraints, sensor noise, and physical dynamics. This field combines robotics, computer vision, machine learning, and control theory to create intelligent systems that can perceive, reason about, and act in the physical world.

The key characteristics of physical AI include embodiment (having a physical form), situatedness (operating in real-world environments), and real-time operation (making decisions within tight time constraints).""",

    "humanoid_robots": """Chapter 2: Humanoid Robotics Fundamentals

Humanoid robots are robots designed to resemble and behave like humans. They typically have a torso, head, two arms, and two legs, mimicking human body structure. The motivation for humanoid design includes navigating human-designed environments, using human tools, and providing intuitive human-robot interaction.

Key components include actuators (motors and servos), sensors (cameras, IMUs, force sensors), computing systems, power systems (batteries), and mechanical structure (frames, joints, and linkages).""",

    "perception": """Chapter 3: Perception Systems

Perception is critical for humanoid robots to understand their environment. Visual perception uses cameras to detect objects, people, and obstacles. Common techniques include object detection and recognition using deep learning models like YOLO and Faster R-CNN, depth estimation using stereo cameras or depth sensors, semantic segmentation to understand scene composition, and human pose estimation to recognize and track people.

Beyond vision, robots use tactile sensors, IMUs for balance, Lidar for 3D mapping, and microphones for audio perception.""",

    "locomotion": """Chapter 5: Bipedal Locomotion

Walking on two legs is one of the most challenging aspects of humanoid robotics. Unlike wheeled robots, bipedal robots must constantly maintain balance while transitioning weight between feet. Key concepts include the Zero Moment Point (ZMP), which is a stability criterion for bipedal walking. Gait patterns are cyclic patterns of leg movement, including walking, running, and stair climbing.

Balance control involves predicting and compensating for disturbances using feedback from IMUs and force sensors. Push recovery strategies help robots recover from external forces.""",

    "manipulation": """Chapter 6: Manipulation and Grasping

Humanoid robots need dexterous manipulation capabilities to interact with objects and use tools. Key challenges include grasp planning (determining where and how to grasp objects), force control (applying appropriate forces without damaging objects), bimanual manipulation (coordinating both arms), and tool use (using human tools like hammers and screwdrivers).

Force control requires force feedback and compliant control to grasp objects securely without damage.""",

    "learning": """Chapter 7: Learning and Adaptation

Modern humanoid robots increasingly rely on machine learning to improve their capabilities. Reinforcement Learning allows robots to learn behaviors through trial and error - deep RL has achieved impressive results in locomotion and manipulation. Imitation Learning enables robots to learn by observing human demonstrations, which can accelerate learning compared to pure RL. Transfer Learning helps transfer knowledge learned in simulation or one task to real robots or other tasks.

Sim-to-real transfer involves training in simulation and deploying on real robots, addressing the high cost and safety concerns of real-world training.""",

    "interaction": """Chapter 8: Human-Robot Interaction

For humanoid robots to work alongside humans, effective interaction is essential. This includes natural language processing for understanding and generating human language, gesture recognition for interpreting human gestures and body language, recognizing social cues and emotions, ensuring safe interaction through compliant actuators and collision detection, and collaborating on shared goals.

Social robots like Pepper are specifically designed for customer service and companionship applications.""",

    "platforms": """Chapter 9: Hardware Platforms

Several notable humanoid robot platforms exist:

Atlas by Boston Dynamics - An advanced research platform known for dynamic locomotion and parkour capabilities, featuring hydraulic actuation and advanced perception systems.

ASIMO by Honda - One of the first commercially demonstrated humanoid robots, showcasing smooth walking, stair climbing, and basic interaction capabilities.

Pepper by SoftBank Robotics - A social humanoid robot designed for customer service and companionship, featuring emotion recognition and natural interaction.

Digit by Agility Robotics - A commercial humanoid designed for logistics and warehouse applications, featuring efficient bipedal locomotion and package manipulation.

Tesla Optimus - A recently announced general-purpose humanoid robot aimed at performing dangerous or repetitive tasks.""",

    "applications": """Chapter 10: Applications and Future Directions

Humanoid robots have numerous potential applications:

Healthcare - Assisting elderly or disabled individuals with daily activities, rehabilitation, and companionship
Manufacturing - Flexible automation that can work alongside humans and use existing tools and infrastructure
Service Industry - Customer service, hospitality, and retail applications where human-like appearance aids interaction
Exploration - Operating in hazardous environments like disaster zones or space where human-like mobility is advantageous
Entertainment - Performers, educators, and companions in entertainment and educational settings

Future directions include more robust hardware, better energy efficiency, more sophisticated AI, improved natural interaction, lower costs, better sim-to-real transfer, and integration of foundation models.""",

    "challenges": """Chapter 11: Challenges and Research Frontiers

Despite significant progress, many challenges remain:

Robustness - Current systems are fragile and struggle with unexpected situations. Improving robustness is critical for real-world deployment.

Energy Efficiency - Humanoid robots consume significant power, limiting operation time. Better actuators and control strategies are needed.

Computational Requirements - Running sophisticated AI models requires substantial computing power, creating challenges for onboard processing.

Generalization - Robots trained in specific environments often fail when conditions change. Better generalization is essential.

Safety - Ensuring robots operate safely around humans remains critical, requiring better perception, prediction, and control.

Ethical Considerations - As robots become more capable, questions arise about autonomy, accountability, and societal impact."""
}


class SimpleRAGService:
    def __init__(self):
        self.book_content = BOOK_CONTENT

    def _is_conversational_query(self, question: str) -> bool:
        """
        Check if the query is conversational (greeting, thanks, etc.) rather than a real question
        """
        question_lower = question.lower().strip()

        # Common conversational phrases
        conversational_patterns = [
            "hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening",
            "thanks", "thank you", "thx", "ty", "appreciate",
            "bye", "goodbye", "see you", "later",
            "ok", "okay", "cool", "nice", "great", "awesome",
            "yes", "no", "yeah", "nope", "yep",
        ]

        # Check if the entire question is just a conversational phrase
        for pattern in conversational_patterns:
            if question_lower == pattern or question_lower == pattern + "!":
                return True

        # Check if it's very short (less than 4 chars) without keywords
        if len(question_lower) < 4:
            return True

        return False

    def _find_relevant_content(self, question: str) -> List[str]:
        """
        Simple keyword-based matching to find relevant content
        """
        question_lower = question.lower()
        relevant_chunks = []

        # Keywords mapping to content sections
        keywords_map = {
            # Book structure queries
            "chapter": ["book_structure"],
            "chapters": ["book_structure"],
            "table of content": ["book_structure"],
            "contents": ["book_structure"],
            "structure": ["book_structure"],
            "outline": ["book_structure"],
            "chapter 1": ["physical_ai"],
            "chapter 2": ["humanoid_robots"],
            "chapter 3": ["perception"],
            "chapter 5": ["locomotion"],
            "chapter 6": ["manipulation"],
            "chapter 7": ["learning"],
            "chapter 8": ["interaction"],
            "chapter 9": ["platforms"],
            "chapter 10": ["applications"],
            "chapter 11": ["challenges"],

            # Topic-based queries
            "physical ai": ["physical_ai"],
            "humanoid": ["humanoid_robots", "platforms"],
            "robot": ["humanoid_robots", "platforms"],
            "fundamental": ["humanoid_robots"],
            "component": ["humanoid_robots"],
            "actuator": ["humanoid_robots"],
            "perception": ["perception"],
            "vision": ["perception"],
            "camera": ["perception"],
            "see": ["perception"],
            "sensor": ["perception", "humanoid_robots"],
            "detect": ["perception"],
            "walk": ["locomotion"],
            "walking": ["locomotion"],
            "locomotion": ["locomotion"],
            "balance": ["locomotion"],
            "leg": ["locomotion"],
            "feet": ["locomotion"],
            "bipedal": ["locomotion"],
            "gait": ["locomotion"],
            "grasp": ["manipulation"],
            "grasping": ["manipulation"],
            "manipulation": ["manipulation"],
            "hand": ["manipulation"],
            "grip": ["manipulation"],
            "tool": ["manipulation"],
            "learn": ["learning"],
            "learning": ["learning"],
            "training": ["learning"],
            "reinforcement": ["learning"],
            "imitation": ["learning"],
            "adapt": ["learning"],
            "interact": ["interaction"],
            "interaction": ["interaction"],
            "language": ["interaction"],
            "communication": ["interaction"],
            "social": ["interaction"],
            "gesture": ["interaction"],
            "atlas": ["platforms"],
            "asimo": ["platforms"],
            "pepper": ["platforms"],
            "digit": ["platforms"],
            "optimus": ["platforms"],
            "tesla": ["platforms"],
            "boston dynamics": ["platforms"],
            "platform": ["platforms"],
            "application": ["applications"],
            "use case": ["applications"],
            "healthcare": ["applications"],
            "manufacturing": ["applications"],
            "service": ["applications"],
            "future": ["applications"],
            "challenge": ["challenges"],
            "challenges": ["challenges"],
            "problem": ["challenges"],
            "difficult": ["challenges"],
            "limitation": ["challenges"],
            "robust": ["challenges"],
            "energy": ["challenges"],
            "safety": ["challenges"]
        }

        # Find matching content
        matched_sections = set()
        for keyword, sections in keywords_map.items():
            if keyword in question_lower:
                matched_sections.update(sections)

        # If no specific matches, return empty list (will be handled as no content found)
        if not matched_sections:
            return []

        # Get the content
        for section in matched_sections:
            if section in self.book_content:
                relevant_chunks.append(self.book_content[section])

        return relevant_chunks[:3]  # Return top 3 matches

    def _get_conversational_response(self, question: str) -> str:
        """
        Generate a friendly conversational response
        """
        question_lower = question.lower().strip()

        # Greetings
        if any(word in question_lower for word in ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]):
            return "Hello! I'm your Physical AI and Humanoid Robotics assistant. I can answer questions about physical AI, humanoid robots, perception systems, locomotion, manipulation, learning algorithms, robot platforms, applications, and challenges in the field. What would you like to know?"

        # Thanks
        if any(word in question_lower for word in ["thanks", "thank you", "thx", "appreciate"]):
            return "You're welcome! Feel free to ask me more questions about Physical AI and Humanoid Robotics anytime."

        # Goodbye
        if any(word in question_lower for word in ["bye", "goodbye", "see you", "later"]):
            return "Goodbye! Come back anytime you have questions about Physical AI and Humanoid Robotics!"

        # Positive feedback
        if any(word in question_lower for word in ["ok", "okay", "cool", "nice", "great", "awesome"]):
            return "Great! Is there anything else about Physical AI or Humanoid Robotics you'd like to know?"

        # Default conversational response
        return "I'm here to help you with questions about Physical AI and Humanoid Robotics. You can ask me about robot platforms, perception systems, locomotion, manipulation, learning algorithms, applications, and more!"

    def _generate_answer(self, question: str, context_chunks: List[str]) -> str:
        """
        Generate answer based on question and context
        """
        if not context_chunks:
            return "I'm sorry, I couldn't find specific information about that in the Physical AI and Humanoid Robotics book. Could you please rephrase your question or ask about topics like robot platforms, perception, locomotion, manipulation, learning, or applications?"

        context = "\n\n".join(context_chunks)

        # Create a more natural answer
        answer = f"Based on the Physical AI and Humanoid Robotics book:\n\n{context}"

        return answer

    def query_full_book(self, request: QueryRequest) -> QueryResponse:
        """
        Handle a query against the full book content
        """
        # Check if it's a conversational query (greeting, thanks, etc.)
        if self._is_conversational_query(request.question):
            answer = self._get_conversational_response(request.question)
            return QueryResponse(
                answer=answer,
                sources=["chatbot"],
                mode_used="conversational"
            )

        # Find relevant content for real questions
        relevant_chunks = self._find_relevant_content(request.question)

        # Generate answer
        answer = self._generate_answer(request.question, relevant_chunks)

        return QueryResponse(
            answer=answer,
            sources=["physical-ai-book"],
            mode_used="full_book"
        )

    def query_selected_text(self, request: QueryRequest) -> QueryResponse:
        """
        Handle a query against only the selected text
        """
        if not request.selected_text:
            raise ValueError("Selected text is required for selected_text mode")

        # For selected text, just use that text as context
        answer = f"Based on the selected text:\n\n{request.selected_text}\n\n"
        answer += f"Regarding your question '{request.question}': "
        answer += "The selected text provides context about this topic. "
        answer += "You can ask more specific questions about the content above."

        return QueryResponse(
            answer=answer,
            sources=["selected_text"],
            mode_used="selected_text"
        )

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """
        Process a query request, choosing between full-book and selected-text modes
        """
        if request.selected_text:
            return self.query_selected_text(request)
        else:
            return self.query_full_book(request)
