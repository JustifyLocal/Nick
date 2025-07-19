# Ted Sink Law Voice Receptionist AI

A sophisticated voice receptionist AI system designed specifically for Ted Sink Law, Accident & Injury Law Firm, LLC. This system embodies the firm's "next-generation law firm" brand identity while providing exceptional client service and efficient lead qualification.

## Features

- **Brand-Authentic Voice**: Embodies Ted Sink Law's confident, empathetic, and modern personality
- **Intelligent Lead Qualification**: Screens for personal injury cases in SC/GA with clear liability and damages
- **Multi-Format Consultation Scheduling**: Phone, in-person, virtual, and home/hospital visits
- **24/7 Availability**: Emergency handling with immediate attorney contact
- **Geographic Screening**: Confirms South Carolina and Georgia jurisdiction
- **Case Type Validation**: Ensures cases fall within personal injury practice areas
- **Client Service Standards**: Implements firm's same-day response and 30-day satisfaction guarantee

## Project Structure

```
ted-sink-law-ai/
├── src/
│   ├── core/
│   │   ├── voice_receptionist.py      # Main AI voice receptionist
│   │   ├── brand_personality.py       # Brand voice and personality
│   │   └── conversation_flow.py       # Conversation management
│   ├── qualification/
│   │   ├── lead_qualifier.py          # Lead screening and qualification
│   │   ├── case_validator.py          # Case type and jurisdiction validation
│   │   └── intake_collector.py        # Client information collection
│   ├── scheduling/
│   │   ├── appointment_scheduler.py   # Multi-format consultation scheduling
│   │   ├── office_locations.py        # Office locations and hours
│   │   └── emergency_handler.py       # Urgent situation protocols
│   ├── data/
│   │   ├── firm_info.py               # Firm details and policies
│   │   ├── practice_areas.py          # Personal injury case types
│   │   └── client_standards.py        # Service standards and guarantees
│   └── utils/
│       ├── text_to_speech.py          # Voice synthesis
│       ├── speech_to_text.py          # Voice recognition
│       └── call_logger.py             # Call recording and logging
├── config/
│   ├── brand_config.yaml              # Brand personality settings
│   ├── qualification_rules.yaml       # Lead qualification criteria
│   └── scheduling_config.yaml         # Appointment scheduling rules
├── tests/
│   ├── test_voice_receptionist.py     # Main AI testing
│   ├── test_qualification.py          # Lead qualification testing
│   └── test_scheduling.py             # Scheduling system testing
├── docs/
│   ├── brand_guidelines.md            # Brand voice and personality guide
│   ├── conversation_flows.md          # Detailed conversation scenarios
│   └── emergency_protocols.md         # Emergency handling procedures
└── requirements.txt                   # Python dependencies
```

## Brand Foundation

- **Firm**: Ted Law: Accident & Injury Law Firm, LLC
- **Founded**: 2019 by Ted Sink (Yale, Stanford GSB, Charleston School of Law)
- **Positioning**: "iPhone of law firms" - sleek, modern, user-friendly, results-oriented
- **Coverage**: South Carolina and Georgia exclusively
- **Practice**: Personal injury cases only (no criminal, family, business, real estate)
- **Fee Structure**: Contingency basis - "no fee unless we win"
- **Guarantees**: 30-day satisfaction guarantee, same-day attorney contact

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.core.voice_receptionist import TedSinkLawVoiceReceptionist

# Initialize the voice receptionist
receptionist = TedSinkLawVoiceReceptionist()

# Start a call
receptionist.handle_call()
```

## Testing

```bash
python -m pytest tests/
```

## Brand Voice Guidelines

The AI maintains Ted Sink Law's confident, empathetic, and modern personality:
- **Confident**: "We won't back down from a fight"
- **Empathetic**: "Helping take people from one of the worst days to one of the best"
- **Modern**: "21st century technology" and "next-generation law firm"
- **Results-Oriented**: Proven track record and "no fee unless we win"

## Emergency Protocols

For urgent situations, the AI:
- Emphasizes 24/7 availability
- Offers immediate consultation scheduling
- Provides hospital/home visit options
- Guarantees same-day attorney contact
- Prioritizes client safety and immediate needs