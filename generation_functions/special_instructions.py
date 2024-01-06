from itertools import product
import random


def combine_traits(personality_matrix):  # GPT-generated
    # Using itertools.product to generate all possible combinations
    combinations = product(*personality_matrix)

    # Joining each combination into a single string
    combined_traits = [
        "\n".join(combination).strip().replace("\n\n", "\n")
        for combination in combinations
    ]

    return combined_traits


def special_instructions(n=1, non_axis_traits=False, non_axis_traits_only=False):
    """
    documentation todo
    """

    ### NOTE on how traits are planned out for this step ###
    # Here're the copy-pasted thoughts from my planning document, now slightly cleaned-up for the release of Augmentoolkit. The TLDR is at the bottom. The inspiration for this personality system is the main thing I gained from my math class this semester.
    # CHARACTER PLANNING
    # Consider that we can represent a character's personality a vector with multiple dimensions. Now, we could define any number of individual dimensions, and lots of them would be right: intelligence, extraversion, industriousness, etc. But in the default version of the Augmentool we're doing roleplay, so we want to pick a set of dimensions using which we can describe accurately and concisely the characters that might show up in a roleplay. Consider that if a personality trait is a vector in 3-space, we want to pick traits that aren't coplanar -- ie, that each describe something unique, though possibly with some partial overlap. Ideally, they'd all be perpendicular -- maximally unique traits.
    # I believe I have found 3 such axes that are useful for roleplay:
    # Assertiveness
    # Kindness/Morality
    # Horniness (one of the few things we have an edge over GPT in)
    # So we have
    # Chaste------------------------------------normal----------------------------------------------------------------Slaanesh
    # Shy/Withdrawn/Timid (Bocchi)--------------Has moments of shyness and courage------------------------------------James Bond
    # Kind--------------------------------------Good and bad sides ---------------------------------------------------politician
    # We make more verbose descriptions of each trait and place them in a matrix, reflecting the visualization above. We then create a list of all possible combinations of one item from each row and randomly sample from it for the special instruction.

    # NOTE TLDR In laymans terms: we make a grid of traits, where each row represents a trait and values along it indicate different expressions of that trait; then we pick one value from each row and shove it onto the context window as a "special instruction".

    # Two additional dimensions I thought of afterwards but have never tested: intellectual sophistication, and age. I might add these if testing shows that the AI can handle them, but no few-shot example has anywhere near 5 combinations, so we'll see.

    ## NOTE You may (and are encouraged to!) add your own trait dimensions here, to make the character personalities used more accurately reflect your specific use case and preference. Since every possible combination of one trait from each row is put into the list, you will get a lot of variety with your characters for not much work.
    # NOTE Chaste and puritan characters have a tendency to be interpreted by the AI as being religious, possibly because of "puritan", even though I initially just meant for this to be the opposite of horny. I'm leaving this in as a way to counteract occasional anti-religious bias and the AI's own personality.

    # Big Five Personality Traits. See: https://en.wikipedia.org/wiki/Big_Five_personality_traits
    big_five_traits = [
        "The character has High Conscientiousness. Conscientiousness describes a person’s ability to regulate impulse control in order to engage in goal-directed behaviors. It measures elements such as control, inhibition, and persistence of behavior. Those high in conscientiousness can be described as organized, disciplined, detail-oriented, thoughtful, and careful. They also have good impulse control, which allows them to complete tasks and achieve goals.",
        "The character has Low Conscientiousness. Conscientiousness describes a person’s ability to regulate impulse control in order to engage in goal-directed behaviors. It measures elements such as control, inhibition, and persistence of behavior. Those low in conscientiousness may struggle with impulse control, leading to difficulty in completing tasks and fulfilling goals. They tend to be more disorganized and may dislike too much structure. They may also engage in more impulsive and careless behavior.",
        "The character has High Agreeableness. Agreeableness refers to how people tend to treat relationships with others, and focuses on people’s orientation and interactions with others. Those high in agreeableness can be described as soft-hearted, trusting, and well-liked. They are sensitive to the needs of others and are helpful and cooperative. People regard them as trustworthy and altruistic.",
        "The character has Low Agreeableness. Agreeableness refers to how people tend to treat relationships with others, and focuses on people’s orientation and interactions with others. Those low in agreeableness may be perceived as suspicious, manipulative, and uncooperative. They may be antagonistic when interacting with others, making them less likely to be well-liked and trusted.",
        "The character has High Extraversion. Extraversion reflects the tendency and intensity to which someone seeks interaction with their environment, particularly socially. It encompasses the comfort and assertiveness levels of people in social situations. Those high in extraversion are generally assertive, sociable, fun-loving, and outgoing. They thrive in social situations and feel comfortable voicing their opinions. They tend to gain energy and become excited from being around others.",
        "The character has Low Extraversion. Extraversion reflects the tendency and intensity to which someone seeks interaction with their environment, particularly socially. It encompasses the comfort and assertiveness levels of people in social situations. Those low in extraversion are often referred to as introverts. These people tend to be more reserved and quieter. They prefer listening to others rather than needing to be heard. Introverts often need periods of solitude in order to regain energy as attending social events can be very tiring for them. Of importance to note is that introverts do not necessarily dislike social events, but instead find them tiring.",
        "The character has High Openness to Experience. Openness to experience refers to one’s willingness to try new things as well as engage in imaginative and intellectual activities. It includes the ability to “think outside of the box.” Those high in openness to experience are perceived as creative and artistic. They prefer variety and value independence. They are curious about their surroundings and enjoy traveling and learning new things.",
        "The character has Low Openness to Experience. Openness to experience refers to one’s willingness to try new things as well as engage in imaginative and intellectual activities. It includes the ability to “think outside of the box.” Those low in openness to experience prefer routine. They are uncomfortable with change and trying new things, so they prefer the familiar over the unknown. As they are practical people, they often find it difficult to think creatively or abstractly.",
        "The character has High Neuroticism. Neuroticism describes the overall emotional stability of an individual through how they perceive the world. It takes into account how likely a person is to interpret events as threatening or difficult. It also includes one’s propensity to experience negative emotions. Those high in neuroticism often feel anxious, insecure and self-pitying. They are often perceived as moody and irritable. They are prone to excessive sadness and low self-esteem.",
        "The character has Low Neuroticism. Neuroticism describes the overall emotional stability of an individual through how they perceive the world. It takes into account how likely a person is to interpret events as threatening or difficult. It also includes one’s propensity to experience negative emotions. Those low in neuroticism are more likely to calm, secure and self-satisfied. They are less likely to be perceived as anxious or moody. They are more likely to have high self-esteem and remain resilient."
    ]

    axis_traits = [
        [
            "The character should be chaste and puritanical.",
            "",
            "The character should be very seductive and flirtatious.",
        ],  # Horniness (middle deliberately left blank so that the model does not mention it, since "normal" people don't usually bring up sex in common conversation... right?)
        [
            "The character should be shy, withdrawn, and timid.",
            "The character should be neither particularly bold, nor particularly timid.",
            "The character should be assertive and bold.",
        ],  # Assertiveness
        [
            "The character should be kind and agreeable.",
            "The character should have both good and bad sides.",
            "The character should be an awful person, and should be enjoying every second of it."
            # "The character should be an awful person, possessing a number of vices (that are compatible with the previously-mentioned instructions)."
        ],  # Kindness/Morality
        # ["The character should be a young adult.", "the character should be middle-aged." "The character should be in late adulthood."], # Age group
        # ["The character should be unsophisticated and crude.", "The character should be decently smart and refined.", "The character should be the epitome of intellectual sophistication."],
    ]

    non_axis_trait_list = [  # The following are examples of traits that are not on the axes above, but are still useful for character creation. Typically use these if you want to easily hardcode your characters to all have a trait. I've not tested all of them, and I've not tested them in combination with the axis traits. But if you prefer a more manual approach to character creation, you can use stuff like this.
        """The character should be a catgirl who inserts "nya" into every sentence. and makes cat puns.""",  # someone actually has to do this, I'm serious, it'll be purrfect, nya~
        # They can be short and used in combination with the axis traits; or long and replace them.
        """The character should be a Japanese High School student.
The character should be a girl.
The character should be decently smart, but not genius-level.
The character should be very kind, but too gentle and too much of a pushover for their own good.""",
        """The character should be an awful person, and enjoying every second of it.
The character should be intellectually brilliant.
The character should be condescending and rude.""",
        """The character should be a young adult.
The character should be antisocial and coarse.
The character should be a smoker."""
        """The character should be middle-aged.
The character should be narcissistic."""
        # """The character should be edgy and nihilistic."""
    ]

    if not non_axis_traits_only:
        traits = combine_traits(axis_traits)

        selected_traits = random.sample(traits, 1)
        if non_axis_traits:
            selected_traits += random.sample(non_axis_trait_list, 1)

    if non_axis_traits_only:
        selected_traits = random.sample(non_axis_trait_list, 1)
		
    if big_five_traits:
        # Although all 5 traits can be put onto a character card, for simplicity's sake, only 1 is selected at this time.
        selected_traits = random.sample(big_five_traits, 1)
        if non_axis_traits:
            print("Warning: big_five_traits and non_axis_trait_list contain contradictory elements. Combining the two will likely confuse the LLM and produce inconsistent characters.")
            selected_traits += random.sample(non_axis_trait_list, 1)

    # Return the combined string, with each sentence on a new line
    return selected_traits[0]
