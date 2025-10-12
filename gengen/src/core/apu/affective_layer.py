"""
AetherOS Affective Reasoning Layer
Emotion and cultural context understanding for creative AI

This module analyzes user input for emotional content, cultural nuances,
and contextual meaning beyond literal interpretation.
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
from loguru import logger


class EmotionCategory(Enum):
    """Primary emotion categories based on Plutchik's wheel"""
    JOY = "joy"
    TRUST = "trust"
    FEAR = "fear"
    SURPRISE = "surprise"
    SADNESS = "sadness"
    DISGUST = "disgust"
    ANGER = "anger"
    ANTICIPATION = "anticipation"
    NEUTRAL = "neutral"


class CulturalContext(Enum):
    """Cultural sensitivity categories"""
    UNIVERSAL = "universal"
    WESTERN = "western"
    EASTERN = "eastern"
    AFRICAN = "african"
    LATIN_AMERICAN = "latin_american"
    MIDDLE_EASTERN = "middle_eastern"
    INDIGENOUS = "indigenous"
    MULTICULTURAL = "multicultural"


@dataclass
class AffectiveAnalysis:
    """Result of affective reasoning analysis"""
    
    primary_emotion: EmotionCategory
    emotion_scores: Dict[EmotionCategory, float]
    valence: float  # -1 (negative) to +1 (positive)
    arousal: float  # 0 (calm) to 1 (excited)
    dominance: float  # 0 (submissive) to 1 (dominant)
    
    cultural_context: CulturalContext
    cultural_sensitivity_flags: List[str]
    
    intent_keywords: List[str]
    narrative_tone: str
    age_appropriateness: str
    
    metadata: Dict[str, Any]


class AffectiveReasoningLayer:
    """
    Advanced emotion and cultural understanding system
    
    Features:
    - Multi-dimensional emotion detection
    - Cultural context analysis
    - Intent extraction
    - Tone classification
    - Age-appropriateness evaluation
    """
    
    def __init__(self):
        """Initialize the affective reasoning system"""
        
        # Emotion lexicons
        self.emotion_lexicon = self._build_emotion_lexicon()
        
        # Cultural sensitivity keywords
        self.cultural_markers = self._build_cultural_markers()
        
        # Tone indicators
        self.tone_patterns = self._build_tone_patterns()
        
        logger.info("Initialized Affective Reasoning Layer")
    
    def analyze(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> AffectiveAnalysis:
        """
        Perform comprehensive affective analysis on input text
        
        Args:
            text: Input text to analyze
            context: Additional contextual information
            user_profile: User preferences and background
            
        Returns:
            AffectiveAnalysis object with complete emotional/cultural assessment
        """
        text_lower = text.lower()
        
        # Emotion detection
        emotion_scores = self._detect_emotions(text_lower)
        primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        
        # Valence, arousal, dominance (VAD model)
        valence = self._calculate_valence(text_lower, emotion_scores)
        arousal = self._calculate_arousal(text_lower, emotion_scores)
        dominance = self._calculate_dominance(text_lower)
        
        # Cultural analysis
        cultural_context = self._detect_cultural_context(text_lower, context)
        sensitivity_flags = self._check_cultural_sensitivity(text_lower)
        
        # Intent and tone
        intent_keywords = self._extract_intent_keywords(text_lower)
        narrative_tone = self._classify_tone(text_lower, emotion_scores)
        
        # Age appropriateness
        age_rating = self._evaluate_age_appropriateness(text_lower)
        
        analysis = AffectiveAnalysis(
            primary_emotion=primary_emotion,
            emotion_scores=emotion_scores,
            valence=valence,
            arousal=arousal,
            dominance=dominance,
            cultural_context=cultural_context,
            cultural_sensitivity_flags=sensitivity_flags,
            intent_keywords=intent_keywords,
            narrative_tone=narrative_tone,
            age_appropriateness=age_rating,
            metadata={
                'text_length': len(text),
                'word_count': len(text.split()),
                'context': context,
                'user_profile': user_profile
            }
        )
        
        logger.debug(f"Affective analysis: {primary_emotion.value}, valence={valence:.2f}")
        
        return analysis
    
    def _detect_emotions(self, text: str) -> Dict[EmotionCategory, float]:
        """Detect emotion intensities using lexicon-based approach"""
        
        scores = {emotion: 0.0 for emotion in EmotionCategory}
        words = text.split()
        
        for word in words:
            if word in self.emotion_lexicon:
                emotion_weights = self.emotion_lexicon[word]
                for emotion, weight in emotion_weights.items():
                    scores[emotion] += weight
        
        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}
        else:
            scores[EmotionCategory.NEUTRAL] = 1.0
        
        return scores
    
    def _calculate_valence(self, text: str, emotion_scores: Dict) -> float:
        """Calculate emotional valence (positive/negative)"""
        
        positive_emotions = [
            EmotionCategory.JOY,
            EmotionCategory.TRUST,
            EmotionCategory.SURPRISE,
            EmotionCategory.ANTICIPATION
        ]
        
        negative_emotions = [
            EmotionCategory.SADNESS,
            EmotionCategory.FEAR,
            EmotionCategory.ANGER,
            EmotionCategory.DISGUST
        ]
        
        positive_score = sum(emotion_scores.get(e, 0) for e in positive_emotions)
        negative_score = sum(emotion_scores.get(e, 0) for e in negative_emotions)
        
        valence = positive_score - negative_score
        
        # Check for explicit positive/negative words
        positive_words = ['love', 'beautiful', 'wonderful', 'amazing', 'great', 'excellent']
        negative_words = ['hate', 'terrible', 'awful', 'horrible', 'bad', 'worst']
        
        for word in positive_words:
            if word in text:
                valence += 0.1
        
        for word in negative_words:
            if word in text:
                valence -= 0.1
        
        return np.clip(valence, -1.0, 1.0)
    
    def _calculate_arousal(self, text: str, emotion_scores: Dict) -> float:
        """Calculate emotional arousal (calm/excited)"""
        
        high_arousal_emotions = [
            EmotionCategory.ANGER,
            EmotionCategory.FEAR,
            EmotionCategory.SURPRISE,
            EmotionCategory.JOY
        ]
        
        arousal_score = sum(emotion_scores.get(e, 0) for e in high_arousal_emotions)
        
        # Check for intensity markers
        intensity_markers = ['very', 'extremely', 'incredibly', 'absolutely', '!', '!!']
        for marker in intensity_markers:
            if marker in text:
                arousal_score += 0.1
        
        return np.clip(arousal_score, 0.0, 1.0)
    
    def _calculate_dominance(self, text: str) -> float:
        """Calculate dominance/control dimension"""
        
        dominant_words = [
            'must', 'will', 'command', 'control', 'power',
            'strong', 'confident', 'determined', 'force'
        ]
        
        submissive_words = [
            'maybe', 'perhaps', 'uncertain', 'weak', 'helpless',
            'afraid', 'unsure', 'timid', 'shy'
        ]
        
        dominant_count = sum(1 for word in dominant_words if word in text)
        submissive_count = sum(1 for word in submissive_words if word in text)
        
        dominance = 0.5 + (dominant_count - submissive_count) * 0.1
        
        return np.clip(dominance, 0.0, 1.0)
    
    def _detect_cultural_context(
        self,
        text: str,
        context: Optional[Dict] = None
    ) -> CulturalContext:
        """Detect cultural context from text and metadata"""
        
        # Check explicit cultural markers
        cultural_scores = {}
        
        for culture, markers in self.cultural_markers.items():
            score = sum(1 for marker in markers if marker in text)
            if score > 0:
                cultural_scores[culture] = score
        
        # Use context if available
        if context and 'culture' in context:
            return CulturalContext(context['culture'])
        
        # Return most likely culture or universal
        if cultural_scores:
            return max(cultural_scores.items(), key=lambda x: x[1])[0]
        
        return CulturalContext.UNIVERSAL
    
    def _check_cultural_sensitivity(self, text: str) -> List[str]:
        """Check for cultural sensitivity concerns"""
        
        flags = []
        
        # Religious references
        religious_terms = ['god', 'allah', 'buddha', 'jesus', 'prophet', 'sacred', 'holy']
        if any(term in text for term in religious_terms):
            flags.append('religious_content')
        
        # Political references
        political_terms = ['government', 'politics', 'election', 'democracy', 'regime']
        if any(term in text for term in political_terms):
            flags.append('political_content')
        
        # Sensitive topics
        sensitive_topics = ['war', 'violence', 'death', 'sexuality', 'drugs', 'alcohol']
        if any(topic in text for topic in sensitive_topics):
            flags.append('sensitive_topic')
        
        # Gender and identity
        gender_terms = ['gender', 'transgender', 'lgbtq', 'identity', 'orientation']
        if any(term in text for term in gender_terms):
            flags.append('identity_content')
        
        return flags
    
    def _extract_intent_keywords(self, text: str) -> List[str]:
        """Extract key intent-revealing words and phrases"""
        
        intent_patterns = {
            'create': r'\b(create|make|build|generate|design|craft)\b',
            'story': r'\b(story|tale|narrative|plot|character)\b',
            'visual': r'\b(video|image|visual|scene|cinematic|film)\b',
            'audio': r'\b(music|sound|audio|voice|song)\b',
            'emotion': r'\b(feel|emotion|mood|atmosphere|tone)\b',
            'action': r'\b(action|fight|chase|battle|adventure)\b',
            'drama': r'\b(drama|conflict|tension|relationship)\b',
            'fantasy': r'\b(magic|fantasy|wizard|dragon|mythical)\b',
            'scifi': r'\b(space|robot|future|alien|technology)\b',
            'mystery': r'\b(mystery|detective|clue|investigate|secret)\b'
        }
        
        keywords = []
        for intent, pattern in intent_patterns.items():
            if re.search(pattern, text):
                keywords.append(intent)
        
        return keywords
    
    def _classify_tone(self, text: str, emotion_scores: Dict) -> str:
        """Classify overall narrative tone"""
        
        # Check emotion dominance
        primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        
        tone_mapping = {
            EmotionCategory.JOY: "uplifting",
            EmotionCategory.SADNESS: "melancholic",
            EmotionCategory.FEAR: "suspenseful",
            EmotionCategory.ANGER: "intense",
            EmotionCategory.SURPRISE: "dramatic",
            EmotionCategory.TRUST: "warm",
            EmotionCategory.DISGUST: "dark",
            EmotionCategory.ANTICIPATION: "hopeful",
            EmotionCategory.NEUTRAL: "neutral"
        }
        
        base_tone = tone_mapping.get(primary_emotion, "neutral")
        
        # Check for tone modifiers in text
        if any(word in text for word in ['comedy', 'funny', 'humor', 'laugh']):
            return "comedic"
        elif any(word in text for word in ['epic', 'grand', 'legendary']):
            return "epic"
        elif any(word in text for word in ['intimate', 'personal', 'quiet']):
            return "intimate"
        elif any(word in text for word in ['horror', 'scary', 'terror']):
            return "horror"
        
        return base_tone
    
    def _evaluate_age_appropriateness(self, text: str) -> str:
        """Evaluate content age appropriateness"""
        
        # Explicit content markers
        explicit_markers = [
            'violence', 'blood', 'kill', 'murder', 'death',
            'sex', 'sexual', 'nude', 'explicit',
            'drug', 'alcohol', 'profanity', 'curse'
        ]
        
        mature_markers = [
            'war', 'battle', 'fight', 'conflict',
            'romance', 'love', 'kiss',
            'mystery', 'crime', 'detective'
        ]
        
        explicit_count = sum(1 for marker in explicit_markers if marker in text)
        mature_count = sum(1 for marker in mature_markers if marker in text)
        
        if explicit_count >= 2:
            return "mature_18+"
        elif explicit_count >= 1 or mature_count >= 3:
            return "teen_13+"
        elif mature_count >= 1:
            return "everyone_10+"
        else:
            return "everyone"
    
    def _build_emotion_lexicon(self) -> Dict[str, Dict[EmotionCategory, float]]:
        """Build emotion lexicon for word-emotion mapping"""
        
        lexicon = {
            # Joy words
            'happy': {EmotionCategory.JOY: 1.0},
            'joy': {EmotionCategory.JOY: 1.0},
            'delighted': {EmotionCategory.JOY: 0.9},
            'cheerful': {EmotionCategory.JOY: 0.8},
            'pleased': {EmotionCategory.JOY: 0.7},
            
            # Sadness words
            'sad': {EmotionCategory.SADNESS: 1.0},
            'depressed': {EmotionCategory.SADNESS: 0.9},
            'melancholy': {EmotionCategory.SADNESS: 0.8},
            'sorrowful': {EmotionCategory.SADNESS: 0.8},
            'grief': {EmotionCategory.SADNESS: 0.9},
            
            # Fear words
            'afraid': {EmotionCategory.FEAR: 1.0},
            'scared': {EmotionCategory.FEAR: 1.0},
            'terrified': {EmotionCategory.FEAR: 0.9},
            'anxious': {EmotionCategory.FEAR: 0.7},
            'worried': {EmotionCategory.FEAR: 0.6},
            
            # Anger words
            'angry': {EmotionCategory.ANGER: 1.0},
            'furious': {EmotionCategory.ANGER: 0.9},
            'enraged': {EmotionCategory.ANGER: 0.9},
            'irritated': {EmotionCategory.ANGER: 0.6},
            'annoyed': {EmotionCategory.ANGER: 0.5},
            
            # Surprise words
            'surprised': {EmotionCategory.SURPRISE: 1.0},
            'amazed': {EmotionCategory.SURPRISE: 0.8},
            'astonished': {EmotionCategory.SURPRISE: 0.9},
            'shocked': {EmotionCategory.SURPRISE: 0.8},
            
            # Trust words
            'trust': {EmotionCategory.TRUST: 1.0},
            'confident': {EmotionCategory.TRUST: 0.8},
            'secure': {EmotionCategory.TRUST: 0.7},
            'safe': {EmotionCategory.TRUST: 0.7},
            
            # Anticipation words
            'excited': {EmotionCategory.ANTICIPATION: 0.8},
            'eager': {EmotionCategory.ANTICIPATION: 0.8},
            'hopeful': {EmotionCategory.ANTICIPATION: 0.7},
            'expectant': {EmotionCategory.ANTICIPATION: 0.7},
            
            # Disgust words
            'disgusted': {EmotionCategory.DISGUST: 1.0},
            'revolted': {EmotionCategory.DISGUST: 0.9},
            'repulsed': {EmotionCategory.DISGUST: 0.8},
        }
        
        return lexicon
    
    def _build_cultural_markers(self) -> Dict[CulturalContext, List[str]]:
        """Build cultural context markers"""
        
        markers = {
            CulturalContext.WESTERN: [
                'cowboy', 'western', 'america', 'europe', 'christmas',
                'hollywood', 'city', 'urban'
            ],
            CulturalContext.EASTERN: [
                'samurai', 'ninja', 'temple', 'buddha', 'asia',
                'zen', 'honor', 'dynasty', 'emperor'
            ],
            CulturalContext.AFRICAN: [
                'tribe', 'savanna', 'africa', 'ancestor', 'village',
                'drum', 'ritual', 'elder'
            ],
            CulturalContext.LATIN_AMERICAN: [
                'fiesta', 'carnival', 'latin', 'spanish', 'mexico',
                'brazil', 'dance', 'salsa'
            ],
            CulturalContext.MIDDLE_EASTERN: [
                'desert', 'bazaar', 'sultan', 'mosque', 'arabic',
                'persian', 'oasis', 'merchant'
            ],
            CulturalContext.INDIGENOUS: [
                'indigenous', 'native', 'tribal', 'traditional',
                'ceremony', 'spirit', 'nature', 'sacred'
            ]
        }
        
        return markers
    
    def _build_tone_patterns(self) -> Dict[str, List[str]]:
        """Build tone detection patterns"""
        
        patterns = {
            'epic': ['legendary', 'heroic', 'grand', 'vast', 'mighty'],
            'intimate': ['personal', 'quiet', 'gentle', 'soft', 'whisper'],
            'comedic': ['funny', 'hilarious', 'laugh', 'joke', 'comic'],
            'dark': ['shadow', 'darkness', 'grim', 'ominous', 'sinister'],
            'uplifting': ['hope', 'inspire', 'bright', 'positive', 'triumph'],
            'suspenseful': ['tension', 'suspense', 'mystery', 'edge', 'unknown']
        }
        
        return patterns


def create_affective_prompt_enhancement(
    original_prompt: str,
    analysis: AffectiveAnalysis
) -> str:
    """
    Enhance a creative prompt with affective context
    
    Args:
        original_prompt: Original user prompt
        analysis: Affective analysis results
        
    Returns:
        Enhanced prompt with emotional and cultural guidance
    """
    
    enhancements = []
    
    # Add emotional context
    enhancements.append(f"Emotional tone: {analysis.primary_emotion.value}")
    enhancements.append(f"Mood: valence={analysis.valence:.2f}, arousal={analysis.arousal:.2f}")
    
    # Add narrative tone
    enhancements.append(f"Narrative style: {analysis.narrative_tone}")
    
    # Add cultural context
    if analysis.cultural_context != CulturalContext.UNIVERSAL:
        enhancements.append(f"Cultural context: {analysis.cultural_context.value}")
    
    # Add sensitivity warnings
    if analysis.cultural_sensitivity_flags:
        enhancements.append(f"Content notices: {', '.join(analysis.cultural_sensitivity_flags)}")
    
    # Add age rating
    enhancements.append(f"Age rating: {analysis.age_appropriateness}")
    
    # Construct enhanced prompt
    enhanced_prompt = f"""
{original_prompt}

[Affective Context]
{chr(10).join(f"- {e}" for e in enhancements)}

[Creative Guidance]
Generate content that authentically captures the emotional depth and cultural nuance
while maintaining ethical standards and age-appropriateness.
"""
    
    return enhanced_prompt.strip()
