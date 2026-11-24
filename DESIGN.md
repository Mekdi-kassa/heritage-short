# DESIGN.md: Audience, Intent, and User Testing Journal

## 1. Project Overview & Thematic Premise
- **Title**: *የደሴው ሬዲዮ ጠጋኝ (The Radio Craftsman of Dessie)*
- **Logline**: In the misty highlands of Dessie, a young boy learns that broken radios and broken days can be mended with patience, copper wire, and an attentive ear—a lesson in craftsmanship that bridges generations.
- **Medium**: 75-second heritage short film in dual aspect ratios (16:9 cinematic landscape and 9:16 mobile vertical).
- **Language**: Amharic (አማርኛ) narration with synchronized English open subtitles.
- **Original Score**: Ethiopian Tizita minor pentatonic score (masenqo, krar, low cello drone, washint flute).

---

## 2. Audience Definition & Personas (Empathize & Define)

Before generating a single frame or audio token, we defined three core audience personas to anchor every creative and technical decision.

### Persona 1: Bethlehem "Betty" (Age 24, Ethiopian Diaspora in Washington D.C.)
- **Context**: Second-generation Ethiopian-American software engineer. Speaks conversational Amharic with her parents but prefers English subtitles for complex vocabulary.
- **Need**: Craves authentic connection to her family's roots beyond tourist cliches; appreciates technology that honors indigenous tradition.
- **Platform**: Consumes media vertically (9:16) on Instagram Reels and TikTok.
- **Emotional Intent**: Needs to feel cultural pride, nostalgic warmth, and a realization that her modern coding work is spiritually continuous with her grandparents' practical ingenuity.

### Persona 2: Ato Assefa (Age 68, Retired Civil Servant in Dessie/Addis Ababa)
- **Context**: Lived through the 1970s and 80s in Wollo. Remembers gathering around valve tube radios for evening news bulletins and Tilahun Gessesse broadcasts.
- **Need**: Highly sensitive to historical anachronisms, acoustic harshness, or disrespect toward elderly customs.
- **Platform**: Consumes media horizontally (16:9) via family tablet, YouTube, or forwarded Telegram videos.
- **Emotional Intent**: Needs to feel seen, respected, and moved to tears by the dignity of elder blessings and memory preservation.

### Persona 3: Dawit (Age 28, Emerging AI Engineer & Creative Developer in Addis Ababa)
- **Context**: Cohort colleague at 10 Academy building computer vision and generative media pipelines.
- **Need**: Evaluates technical craftsmanship, audio ducking cleanliness, temporal consistency, and prompt precision.
- **Platform**: Desktop YouTube and GitHub repository inspection.
- **Emotional Intent**: Needs to be inspired by how low-cost and open-weight models (Gemini Flash, Wan 2.2, ACE-Step, FFmpeg) can be orchestrated into a cohesive emotional studio.

---

## 3. Emotional Intent (The North Star)
When the final frame fades to the AI attribution card at 75 seconds, the viewer should feel:
> *"Craftsmanship never dies; it only changes materials. Whether twisting copper coils in Dessie in 1978 or wiring neural pipelines in 2026, the heart of engineering is learning to listen."*

---

## 4. User Test 1: The Radio Cut Prototype (Audio Animatic)

### Test Setup
- **Artifact Tested**: `outputs/final/radio_cut.mp4` (sequential Amharic TTS narration tracks over a temporary Tizita masenqo/krar score candidate on a black screen, total duration 75 seconds).
- **Participants**: 3 individuals matching target personas (Bethlehem, Ato Girma, Dawit).
- **Methodology**: Think-aloud feedback session conducted via voice call and Slack screen share.

### Feedback Collected & Recorded Notes

| Participant | Persona Match | Key Observation / Verbatim Quote | Actionable Insight |
| :--- | :--- | :--- | :--- |
| **Bethlehem** | Diaspora Youth | *"The opening line set the mood immediately, but during shot 3 and 4, the Amharic word for 'invitation/secret' was spoken so fast that without pictures I lost the thread for 3 seconds."* | Amharic TTS cadence in Shot 4 was too rapid (~4.8 syl/s). Slowed tempo down to 3.8 syl/s and inserted a 400ms pause after 'ዝምታውን'. |
| **Ato Girma** | Highland Elder | *"The masenqo sound is authentic Tizita, but the transition when the radio breaks felt too sudden. In 1978, when a valve blew, you heard a dying hum before the silence."* | Added spotting note in Shot 3: thin the score to a solitary low cello harmonic to musically convey the power vacuum. |
| **Dawit** | Tech Peer | *"The music volume in the draft was masking the second half of each sentence. You need steeper sidechain ducking or the narration won't survive small phone speakers."* | Increased FFmpeg `sidechaincompress` ratio from 4:1 to 7:1, lowered ducking threshold to 0.025, and increased release time to 1400ms. |

### Concrete Storyboard Changes Resulting from Test 1
1. **Shot 03 & 04 Pacing**: Extended duration of Shot 03 from 6.5s to 7.5s, allowing a quiet breath after the radio broadcast drops out.
2. **Narration Script Polish**: Replaced overly formal Amharic phrasing in Shot 06 with more idiomatic craftsmanship terminology: "በጨዋ እጅ የነካ ሰው" (He who touches with respectful/gentle hands).
3. **Music Cue Modification**: Re-arranged Candidate 1 to isolate the solo masenqo during Shot 01-03, keeping the frequency spectrum clean for voice entry.

---

## 5. User Test 2: The Near-Final Cut (Dual Aspect Ratios)

### Test Setup
- **Artifact Tested**: `outputs/final/heritage_short_16x9.mp4` and `heritage_short_9x16.mp4` with moving shots, ducked master score, normalized -14 LUFS loudness, burned English subtitles, and AI end card.
- **Participants**: 3 viewers (Tigist - film editor, Yonas - diaspora cousin, Dr. Solomon - cultural educator).

### Feedback Collected & Recorded Notes

| Participant | Role | Observation / Verbatim Quote | Actionable Adjustment |
| :--- | :--- | :--- | :--- |
| **Tigist** | Video Editor | *"The visual style in Shot 05 (copper wires) is gorgeous, but in the vertical 9:16 export, the edge of the soldering iron tip touched the TikTok bottom overlay safe zone."* | Shifted vertical crop window upwards (`crop=607:1080:(1920-607)/2:0`) and adjusted subtitle bottom margin from 40px to 85px to stay strictly within mobile platform safe areas. |
| **Yonas** | Diaspora | *"The subtitles are so easy to read now! Seeing both 'Dessie' on the radio glass and in the English translation made me want to call my dad."* | Validated emotional goal. Maintained 2-line subtitle constraint (max 42 characters per line). |
| **Dr. Solomon** | Historian | *"The AI attribution end card is very tasteful. It gives credit to human storytelling while being completely honest about the synthesis."* | Preserved 3.0-second end card hold and clear text mentioning Gemini, Wan 2.2, ACE-Step, and FFmpeg. |

---

## 6. Shot-by-Shot Stated Rationale (Why Every Shot Exists)

Every shot in `storyboard.json` was designed with an explicit narrative function, psychological purpose, and technical constraint:

- **Shot 01 (7.5s, Extreme Wide Establishing)**:
  * *Reason*: Establishes place, historical geography, and highland atmosphere (morning mist over Dessie hills) before introducing personal drama. Anchors the story in authentic Wollo topography.
- **Shot 02 (7.0s, Medium Interior)**:
  * *Reason*: Introduces the central physical artifact—the family 1970s Philips valve radio—framing it as the cultural and emotional fireplace of the household.
- **Shot 03 (7.5s, Medium Close-Up)**:
  * *Reason*: Inciting incident. When the evening broadcast vanishes, Grandfather Assefa's sigh underscores the fragility of connection and sets the emotional stakes.
- **Shot 04 (7.5s, Close-Up Character)**:
  * *Reason*: Perspective shift from elder resignation to youthful agency. Young Girma peeking behind the wooden cabinet establishes curiosity over despair.
- **Shot 05 (7.0s, Macro Electronic Chassis)**:
  * *Reason*: The diagnostic beat. Shows the engineer's eye isolating the single severed wire amidst glowing glass tubes; demonstrates that big failures often stem from small disconnects.
- **Shot 06 (8.0s, Medium Close-Up Workbench)**:
  * *Reason*: The physical climax of craftsmanship. Young hands carefully soldering copper wire, celebrating indigenous skill and patient practice without formal diplomas.
- **Shot 07 (7.5s, Close-Up Tuning Dial)**:
  * *Reason*: Catharsis and payoff. Static gives way to Tilahun Gessesse's song, validating Girma's courage and bringing life back into the silent room.
- **Shot 08 (8.0s, Medium Two-Shot)**:
  * *Reason*: The emotional core and moral blessing. Grandfather embraces the boy and shares the proverb linking technical mending to human empathy.
- **Shot 09 (7.5s, Temporal Match-Cut Pan)**:
  * *Reason*: The thematic bridge. Connects 1978 analog radio soldering directly to 2026 AI coding pipelines, showing that writing software is the contemporary continuation of family craftsmanship.
- **Shot 10 (7.5s, Centered End Card)**:
  * *Reason*: AI disclosure and artistic dedication. Fulfills the ethics and transparency contract while providing visual elegance and closure.
