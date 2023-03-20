# PA7, CS124, Stanford
# v.1.0.4
#
# Original Python code by Ignacio Cases (@cases)
######################################################################
import util

import numpy as np
import re


# noinspection PyMethodMayBeStatic
class Chatbot:
    """Simple class to implement the chatbot for PA 7."""

    def __init__(self, creative=False):
        # The chatbot's default name is `moviebot`.
        # TODO: Give your chatbot a new name.
        self.name = 'Spongebob'

        self.creative = creative

        # This matrix has the following shape: num_movies x num_users
        # The values stored in each row i and column j is the rating for
        # movie i by user j
        self.titles, ratings = util.load_ratings('data/ratings.txt')
        self.sentiment = util.load_sentiment_dictionary('data/sentiment.txt')

        ########################################################################
        # TODO: Binarize the movie ratings matrix.                             #
        ########################################################################

        self.ratings = self.binarize(ratings)
        self.num_sent_movies = 0
        self.user_ratings = np.zeros(len(ratings))
        self.movies = None
        self.curr_sent = None
        self.curr_titles = None
        self.num_movies_to_recommend = 10
        self.recmode = False
        self.curr_num_recommended = 0
        self.recommended_movies = None
        ########################################################################
        #                             END OF YOUR CODE                         #
        ########################################################################

    ############################################################################
    # 1. WARM UP REPL                                                          #
    ############################################################################

    def greeting(self):
        """Return a message that the chatbot uses to greet the user."""
        ########################################################################
        # TODO: Write a short greeting message                                 #
        ########################################################################

        greeting_message = "Hi, how are ya? I'm Spongebob, glad to meet ya! \n" \
                           "Mr Krabs gave me some time off from the Krusty Krab today. \nI'm a bit bummed " \
                           "but now I can recommend you some movies. \nI'm reaaaaaaaaaaaaaady!! Give me some" \
                           ' movies! \nTo help me out, put the movie name and date in quotes, e.g. "Titanic (1997)".' \
                            "\nLet's go!"

        ########################################################################
        #                             END OF YOUR CODE                         #
        ########################################################################
        return greeting_message

    def goodbye(self):
        """
        Return a message that the chatbot uses to bid farewell to the user.
        """
        ########################################################################
        # TODO: Write a short farewell message                                 #
        ########################################################################

        goodbye_message = "Ah, barnacles, we're done? Well, no problemo. See you next time!"

        ########################################################################
        #                          END OF YOUR CODE                            #
        ########################################################################
        return goodbye_message

    ############################################################################
    # 2. Modules 2 and 3: extraction and transformation                        #
    ############################################################################

    def process(self, line):
        """Process a line of input from the REPL and generate a response.

        This is the method that is called by the REPL loop directly with user
        input.

        You should delegate most of the work of processing the user's input to
        the helper functions you write later in this class.

        Takes the input string from the REPL and call delegated functions that
          1) extract the relevant information, and
          2) transform the information into a response to the user.

        Example:
          resp = chatbot.process('I loved "The Notebook" so much!!')
          print(resp) // prints 'So you loved "The Notebook", huh?'

        :param line: a user-supplied line of text
        :returns: a string containing the chatbot's response to the user input
        """

        if self.recmode:
            if line.lower()[0] == "y" or line.lower()[0] == "yes":
                if self.curr_num_recommended < self.num_movies_to_recommend:
                    response = "Got it, boss. You want another recommendation from the sponge. Patrick and I loved this one. You should check out '" + \
                               self.titles[self.recommended_movies[self.curr_num_recommended]][0] + "'.\n"
                    self.curr_num_recommended += 1
                    response += "Another rec? I got thousands. If so, please type 'yes' or 'y'. If you're done, type 'no' or 'n'. I'm ready."
                    return response
                else:
                    self.recmode = False
                    return "That's all of what I've got so far. We don't get many movies in Bikini Bottom. Tell me more about some more!"
            elif line.lower()[0] == "n" or line.lower()[0] == "no":
                self.recmode = False
                return "That was fun! Tell me more about movies you've seen and liked/disliked and I'll give some more!"
            else:
                return "Sorry, I'm not really catching your drift here." \
                       " If you'd like another rec from the sponge, please type 'yes' or 'y'. If not, type 'no' or 'n'."



        else:
            titles = self.extract_titles(line)
            sentiments = None
            response = []
            ################################################################################
            check = 0
            title_len = len(titles)
            #print(titles)
            if title_len == check:
                questions = ['Why is', 'How is', 'Where is', 'When is', 'What are',
                             'Why are', 'How are', 'Where are', 'When are', 'Would I', 'Should I', 'Could I',
                             'Could you,', 'Which is', 'Which are', 'Who are',
                             'Did you', 'what\'s your']
                questions.append('Can you')
                questions.append('Will you')
                questions.append('What is')
                questions.append('Can I')
                questions.append('Should you')
                questions.append('Who is')
                questions.append('Have you')
                questions.append('Would you')
                emotions = ['energized', 'sad', 'angry', 'surprised', 'disgusted', 'scared', 'furious',
                            'joyful', 'smile', 'flabbergasted']
                emotions.append('happy')
                emotions.append('confused')
                emotions.append('tired')
                greetings = ['Hi', 'Hello', 'Sup', 'Ciao', 'Whats up', 'Howdy']
                greetings.append('Ahoy')
                greetings.append('Greetings')
                pos_emotions = ['happy', 'joyful', 'smile']
                pos_emotions.append('energized')
                f = False
                t = True
                question_bool = f
                emotion_bool = f
                greetings_bool = f
                emotion = ""
                q_len = len(questions)
                e_len = len(emotions)
                g_len = len(greetings)
                for i in range(q_len):
                    temp = line.lower()
                    if questions[i].lower() in temp:
                        question_bool = t
                for i in range(e_len):
                    temp = line.lower()
                    if emotions[i] in temp:
                        emotion_bool = t
                        emotion = emotions[i]
                for i in range(g_len):
                    temp = line.lower()
                    if greetings[i].lower() in temp:
                        greetings_bool = t

                if self.creative:
                    if question_bool and line[-1] == '?':
                        line = "Ah tartar sauce, I dont get it. Could you enter it in statement form?"
                        return line
                    elif emotion_bool:
                        if emotion not in pos_emotions:
                            line = "Barnacles. Sorry about making you " + emotion + ". Shrimp paste."
                            return line
                        else:
                            line = "Hip hip hurray! Glad I could make you " + emotion + "!"
                            return line
                    elif greetings_bool:
                        line = "Ahoy there matey! I'm ready!"
                        return line
                    else:
                        line = "Whaddya mean by that one? Is it still movie time? Baaahahahahaha"
                        return line
                else:
                    line = "Did ya forgot to add the quotation marks around the movie? Or are we still talking? HeHe"
                    return line
                #########################################################################
            if len(titles) > 1 and self.creative:
                sentiments = self.extract_sentiment_for_movies(line)
            else:

                sentiment = self.extract_sentiment(line)
                sentiments = []
                for title in titles:
                    tup = (title, sentiment)
                    sentiments.append(tup)

            real_movie_titles_idxs = []
            for i, (title, sentiment) in enumerate(sentiments):
                movies = self.find_movies_by_title(title)
                #print([self.titles[movie] for movie in movies])

                if len(movies) > 1:
                    return "Agh! Shrimp paste, there's too many possible movies. Could you narrow it down a bit more for me here?"

                elif len(movies) == 0:
                    str = "Hmmmm Sorry. I've never heard of " + title
                    return (str + ". Can you tell me more about a different movie you liked or disliked that I would know?")
                elif len(movies) == 1:
                    real_movie_titles_idxs.append((movies[0], sentiment))

            for idx, sent in real_movie_titles_idxs:
                check = 0
                check1 = 1
                check2 = 2
                if sent == check:
                    newstr = "I'm sorry friend. I'm not sure whether you liked " + self.titles[idx][0]
                    newstr += ". Can you tell me more about the movie(s)? Gimme some good words, you love it."
                    response.append(newstr)

                elif check1 == sent:
                    newstr = "Oh, I get it now. I see that you like " + self.titles[idx][0]
                    newstr += "! I thought that one was kind of mid personally."
                    if self.user_ratings[idx] == check:
                        self.num_sent_movies += check1
                    self.user_ratings[idx] = check2
                    response.append(newstr)

                elif check2 == sent and self.creative:
                    newstr = "Oh, I see that you love " + self.titles[idx][0]
                    newstr += "! That's Squidward's favorite!"
                    if check == self.user_ratings[idx]:
                        self.num_sent_movies += check1
                    self.user_ratings[idx] = check2
                    response.append(newstr)

                elif sent == -1:
                    newstr = "I see that you didn't like " + self.titles[idx][0]
                    newstr += "! Yeah, that one is about as good as Squiddy's clarinet solo."
                    if check == self.user_ratings[idx]:
                        self.num_sent_movies += 1
                    self.user_ratings[idx] = -1
                    response.append(newstr)

                elif sent == -2 and self.creative:
                    newstr = "I see that you hate " + self.titles[idx][0]
                    newstr += "! Everyone in Bikini Bottom does too!"
                    if check == self.user_ratings[idx]:
                        self.num_sent_movies += 1
                    self.user_ratings[idx] = -2
                    response.append(newstr)


            if self.num_sent_movies >= 5:
                self.recmode = True
                self.recommended_movies = self.recommend(self.user_ratings, self.ratings, self.num_movies_to_recommend, self.creative)
                self.curr_num_recommended = 0
                response.append("That's enough movies for me. Would you like a movie recommendation now? We can go see it now!")
                response.append("If so, please type 'yes' or 'y'. If you're done, type 'no' or 'n'.")

            else:
                response.append("What about another movie? Tell me more! This is great!")

            return "\n".join(response)

        return ""

    @staticmethod
    def preprocess(text):
        """Do any general-purpose pre-processing before extracting information
        from a line of text.

        Given an input line of text, this method should do any general
        pre-processing and return the pre-processed string. The outputs of this
        method will be used as inputs (instead of the original raw text) for the
        extract_titles, extract_sentiment, and extract_sentiment_for_movies
        methods.

        Note that this method is intentially made static, as you shouldn't need
        to use any attributes of Chatbot in this method.

        :param text: a user-supplied line of text
        :returns: the same text, pre-processed
        """
        ########################################################################
        # TODO: Preprocess the text into a desired format.                     #
        # NOTE: This method is completely OPTIONAL. If it is not helpful to    #
        # your implementation to do any generic preprocessing, feel free to    #
        # leave this method unmodified.                                        #
        ########################################################################

        ########################################################################
        #                             END OF YOUR CODE                         #
        ########################################################################

        return text

    def extract_titles(self, preprocessed_input):
        """Extract potential movie titles from a line of pre-processed text.

        Given an input text which has been pre-processed with preprocess(),
        this method should return a list of movie titles that are potentially
        in the text.

        - If there are no movie titles in the text, return an empty list.
        - If there is exactly one movie title in the text, return a list
        containing just that one movie title.
        - If there are multiple movie titles in the text, return a list
        of all movie titles you've extracted from the text.

        Example:
          potential_titles = chatbot.extract_titles(chatbot.preprocess(
                                            'I liked "The Notebook" a lot.'))
          print(potential_titles) // prints ["The Notebook"]

        :param preprocessed_input: a user-supplied line of text that has been
        pre-processed with preprocess()
        :returns: list of movie titles that are potentially in the text
        """
        re_find_titles = re.findall("\".*?\"", preprocessed_input)
        titles = []
        for title in re_find_titles:
            titles.append(title[1:len(title) - 1])
        general_titles = set()

        if len(titles) == 0:
            for i, (title, keywords) in enumerate(self.titles):

                general, _, year, _, alt = self.extract_year_title_alternative_title(title)


                findtitle = re.findall(rf"\W({re.escape(title.lower())})\W", " " + preprocessed_input.lower() + " ")
                if findtitle:
                    titles.append(title)
                    general_titles.add(general)

                findgeneral = re.findall(rf"\W({re.escape(general.lower())})\W", " " + preprocessed_input.lower() + " ")

                if general not in general_titles:
                    if findgeneral:
                        titles.append(general)
                        general_titles.add(general)

                if alt is not None:
                    findalt = re.findall(rf"\W({re.escape(alt.lower())})\W", " " + preprocessed_input.lower() + " ")
                    if findalt:
                        if general not in general_titles:
                            titles.append(general)
                            general_titles.add(general)

        return titles

    #helpers
    def check_title_contains_sublist(self, title, check_title):
        title = re.sub("[^A-Za-z0-9 ]", "", title)
        check_title = re.sub("[^A-Za-z0-9 ]", "", check_title)
        title_arr = title.split()
        check_title_arr = check_title.split()
        lengther1 = len(check_title_arr)
        lengther2 = len(title_arr)
        for i in range(lengther1 - lengther2 + 1):
            check = check_title_arr[i:i + lengther2]
            if check == title_arr:
                return True
        return False

    def extract_year_title_alternative_title(self, title):
        
        possible_years = re.findall("\([\d]{4}(?:-|-[\d]{4})?\)", title)
        general = title
        if possible_years:
            year = possible_years[len(possible_years) - 1]
            last_index = title.rindex(year)
            general = title[0:last_index].strip(" ")
        else:
            year = None

        begins_with_article = False
        alt = None

        if len(general.split()) is not 1:
            split = general.split()
            first = split[0].lower()
            if first == "a" or first == "an" or first == "the":
                newlist = split.copy()
                a = newlist.pop(0)
                alt_temp = " ".join(newlist)
                alt = alt_temp + ", " + split[0]

        if len(general.split(',')) is not 1 and alt is None:
            split_title = general.rsplit(',', maxsplit=1)
            start = split_title[0]
            end = split_title[1].strip()
            if end.lower() == "a" or end.lower() == "an" or end.lower() == "the":
                alt = end + " " + start
        yearbool = False
        altbool = False
        if year is not None:
            yearbool = True
        if alt is not None:
            altbool = True
        return general, yearbool, year, altbool, alt

    def find_movies_by_title(self, title):
        """ Given a movie title, return a list of indices of matching movies.

        - If no movies are found that match the given title, return an empty
        list.
        - If multiple movies are found that match the given title, return a list
        containing all of the indices of these matching movies.
        - If exactly one movie is found that matches the given title, return a
        list
        that contains the index of that matching movie.

        Example:
          ids = chatbot.find_movies_by_title('Titanic')
          print(ids) // prints [1359, 2716]

        :param title: a string containing a movie title
        :returns: a list of indices of matching movies
        """

        indices_matching_movies = []
        extract_title, has_year, year, has_alt_title, alt = self.extract_year_title_alternative_title(
            title)
        for i, title in enumerate(self.titles):
            ctitle = title[0]
            years = re.findall("\([\d]{4}(?:-|-[\d]{4})?\)", ctitle)

            if years:
                cyear = years[-1]
                cli = ctitle.rindex(cyear)
                ctitle = ctitle[0:cli].strip(" ")

            if years and year is not None:
                if year != cyear:
                    continue
            elower = extract_title.lower()
            clower = ctitle.lower()
            if clower == elower:
                indices_matching_movies.append(i)
                continue

            if alt is not None and clower == alt.lower():
                indices_matching_movies.append(i)
                continue

            if self.creative and self.check_title_contains_sublist(extract_title, ctitle):
                    indices_matching_movies.append(i)

        return indices_matching_movies
    
    def extract_sentiment(self, preprocessed_input):
        """Extract a sentiment rating from a line of pre-processed text.

        You should return -1 if the sentiment of the text is negative, 0 if the
        sentiment of the text is neutral (no sentiment detected), or +1 if the
        sentiment of the text is positive.

        As an optional creative extension, return -2 if the sentiment of the
        text is super negative and +2 if the sentiment of the text is super
        positive.

        Example:
          sentiment = chatbot.extract_sentiment(chatbot.preprocess(
                                                    'I liked "The Titanic"'))
          print(sentiment) // prints 1

        :param preprocessed_input: a user-supplied line of text that has been
        pre-processed with preprocess()
        :returns: a numerical value for the sentiment of the text
        """
        strong_sent_indicators = ["love", "hate", "excellent", "fantastic", "incredible", "life-changing", "amazing",
                                  "despise", "horrible", "hated", "loved", "perfectly", "extremely", "exceedingly",
                                  "acutely", "awfully", "exceedingly", "exceptionally", "excessively",
                                  "extraordinarily",
                                  "highly", "hugely", "immensely", "terrible", "inordinately", "intensely", "overly",
                                  "quite",
                                  "remarkably", "severely", "strikingly", "terribly", "terrifically", "too", "totally",
                                  "uncommonly", "unduly", "unusually", "utterly", "very", "really"]
        negation_indicators = ["not", "didn't", "couldn't", "aren't", "wasn't", "don't", "can't", "isn't", "won't",
                               "wouldn't",
                               "hasn't", "didnt", "couldnt", "arent", "wasnt", "dont", "cant", "isnt", "wont",
                               "wouldnt", "hasnt",
                               "no", "neither", "nor", "never"]
        punc = [".", ",", "!", "?", "...", ";"]
        strong_sent_indicators = set(strong_sent_indicators)
        negation_indicators = set(negation_indicators)
        punc = set(punc)

        sentence = re.sub("\".*?\"", "", preprocessed_input.lower())
        sentence = sentence.split()

        strong = False
        negation_locs = set()

        pos = 0
        neg = 0
        for i in range(len(sentence)):
            word = sentence[i]
            word = re.sub('[^A-Za-z0-9 ]+', '', word)
            if strong == False and word in strong_sent_indicators:
                strong = True
            if word in negation_indicators:
                negation_locs.add(i)
            word_sent = None
            if word in self.sentiment:
                word_sent = self.sentiment[word]
            elif word[-2:] == "ed" and word[0:-2] in self.sentiment:
                word_sent = self.sentiment[word[0:-2]]
            elif word[-2:] == "ed" and word[0:-1] in self.sentiment:
                word_sent = self.sentiment[word[0:-1]]
            elif word[-3:] == "ing" and word[0:-3] in self.sentiment:
                word_sent = self.sentiment[word[0:-3]]
            elif word[-3:] == "ing" and word[0:-3] + "e" in self.sentiment:
                word_sent = self.sentiment[word[0:-3] + "e"]

            if word_sent is not None:
                # word_sent = self.sentiment[sentence[i]]
                if word_sent == "pos":
                    if i >= 1:
                        if i - 1 in negation_locs or i-2 in negation_locs:
                            neg += 1
                        else:
                            pos += 1
                    else:
                        pos += 1
                elif word_sent == "neg":
                    if i >= 1:
                        if i - 1 in negation_locs or i-2 in negation_locs:
                            pos += 1
                        else:
                            neg += 1
                    else:
                        neg += 1

        if pos is 0 and neg is 0:
            return 0
        total_sentiment = (pos + .000001) / (neg + .000001)

        final_value = 0

        if total_sentiment > 1:
            if strong and self.creative:
                final_value = 2
            else:
                final_value = 1
        else:
            if strong and self.creative:
                final_value = -2
            else:
                final_value = -1
        return final_value

    def extract_sentiment_for_movies(self, preprocessed_input):
        """Creative Feature: Extracts the sentiments from a line of
        pre-processed text that may contain multiple movies. Note that the
        sentiments toward the movies may be different.

        You should use the same sentiment values as extract_sentiment, described

        above.
        Hint: feel free to call previously defined functions to implement this.

        Example:
          sentiments = chatbot.extract_sentiment_for_text(
                           chatbot.preprocess(
                           'I liked both "Titanic (1997)" and "Ex Machina".'))
          print(sentiments) // prints [("Titanic (1997)", 1), ("Ex Machina", 1)]

        :param preprocessed_input: a user-supplied line of text that has been
        pre-processed with preprocess()
        :returns: a list of tuples, where the first item in the tuple is a movie
        title, and the second is the sentiment in the text toward that movie
        """
        titles_section = []
        titles = re.findall("\".*?\"", preprocessed_input)
        tokenized_input = re.sub("\".*?\"", " <TITLETOKEN> ", preprocessed_input)
        text_sections = re.split("[,;]|but", tokenized_input)
        length_text = len(text_sections)
        sent_arr = []
        prev_sent_arr = []
        for i in range(length_text):
            section = text_sections[i]
            section_tokenized = section.split()
            for section_token in section_tokenized:
                check = 0
                if section_token == "<TITLETOKEN>":
                    check += 1
                if check > 0:
                    titles_section.append(i)
                else:
                    check = 0
                check = 0
        for i in range(length_text):
            removed_tokens_section = re.sub(" <TITLETOKEN> ", " ", text_sections[i])
            sent = self.extract_sentiment(removed_tokens_section)
            prev_sent_arr.append(sent)
            removed_tokens_section = re.sub("[^A-Za-z0-9 ]", "", removed_tokens_section).strip()
            xcheck = 0
            for __ in range(titles_section.count(i)):
                xcheck = 0
                length_arr = len(sent_arr)
                if removed_tokens_section == "not" and length_arr > 0:
                    xcheck = 1
                elif (removed_tokens_section == "" or removed_tokens_section == "and") and length_arr > 0:
                    xcheck = 2
                else:
                    xcheck = check

                if xcheck == 1:
                    sent_arr.append(sent_arr[-1] * -1)
                elif xcheck == 2:
                    sent_arr.append(sent_arr[-1])
                else:
                    sent_arr.append(sent)
        retval = []
        for i, title in enumerate(titles):
            retval.append((title[1:-1], sent_arr[i]))
        return retval

    def find_movies_closest_to_title(self, title, max_distance=3):
        """Creative Feature: Given a potentially misspelled movie title,
        return a list of the movies in the dataset whose titles have the least
        edit distance from the provided title, and with edit distance at most
        max_distance.

        - If no movies have titles within max_distance of the provided title,
        return an empty list.
        - Otherwise, if there's a movie closer in edit distance to the given
        title than all other movies, return a 1-element list containing its
        index.
        - If there is a tie for closest movie, return a list with the indices
        of all movies tying for minimum edit distance to the given movie.

        Example:
          # should return [1656]
          chatbot.find_movies_closest_to_title("Sleeping Beaty")

        :param title: a potentially misspelled title
        :param max_distance: the maximum edit distance to search for
        :returns: a list of movie indices with titles closest to the given title
        and within edit distance max_distance
        """

        indices_matching_movies = []
        extract_title, year_ex, year, has_alt_title, alternative_title = self.extract_year_title_alternative_title(
            title)
        best_edit_distance = float('inf')
        lengther_dic = len(self.titles)
        check = 0
        for i in range(lengther_dic):
            title_yes = self.titles[i][check]
            year_checker = re.findall("\([\d]{4}(?:-|-[\d]{4})?\)", title_yes)
            lengther_year = len(year_checker)
            if lengther_year < check:
                check_year_ex = check
            if lengther_year == check:
                check_year_ex = check
            else:
                check_year_ex = 1

            if check_year_ex > check:
                year_yes = year_checker[-1]
                index_checker = title_yes.rindex(year_yes)
                title_yes = title_yes[check:index_checker].strip(" ")

            if check_year_ex == 1:
                if year_ex == 1:
                    if year is not title_yes:
                        continue

            low_title = extract_title.lower()
            low2_title = title_yes.lower()
            distance = edit_distance(low_title, low2_title)

            if has_alt_title:
                find_alt = 1
            else:
                find_alt = check
            if find_alt == check and alternative_title is not None:
                low_alt = alternative_title.lower()
                distance = min(distance, edit_distance(low_alt, low2_title))

            if distance == best_edit_distance:
                if distance == max_distance:
                    indices_matching_movies.append(i)
                    continue
                elif distance < max_distance:
                    indices_matching_movies.append(i)
                    continue

            elif distance < best_edit_distance:
                if distance < max_distance:
                    indices_matching_movies = [i]
                    best_edit_distance = distance
                    continue
                elif distance == max_distance:
                    indices_matching_movies = [i]
                    best_edit_distance = distance
                    continue

            if self.creative:
                if self.check_title_contains_sublist(extract_title, title_yes):
                    if best_edit_distance > check:
                        indices_matching_movies = []
                    indices_matching_movies.append(i)
                    best_edit_distance = best_edit_distance - best_edit_distance
                    best_edit_distance = check

        return indices_matching_movies

    def disambiguate(self, clarification, candidates):
        """Creative Feature: Given a list of movies that the user could be
        talking about (represented as indices), and a string given by the user
        as clarification (eg. in response to your bot saying "Which movie did
        you mean: Titanic (1953) or Titanic (1997)?"), use the clarification to
        narrow down the list and return a smaller list of candidates (hopefully
        just 1!)

        - If the clarification uniquely identifies one of the movies, this
        should return a 1-element list with the index of that movie.
        - If it's unclear which movie the user means by the clarification, it
        should return a list with the indices it could be referring to (to
        continue the disambiguation dialogue).

        Example:
          chatbot.disambiguate("1997", [1359, 2716]) should return [1359]

        :param clarification: user input intended to disambiguate between the
        given movies
        :param candidates: a list of movie indices
        :returns: a list of indices corresponding to the movies identified by
        the clarification
        """
        pass

    ############################################################################
    # 3. Movie Recommendation helper functions                                 #
    ############################################################################

    @staticmethod
    def binarize(ratings, threshold=2.5):
        """Return a binarized version of the given matrix.

        To binarize a matrix, replace all entries above the threshold with 1.
        and replace all entries at or below the threshold with a -1.

        Entries whose values are 0 represent null values and should remain at 0.

        Note that this method is intentionally made static, as you shouldn't use
        any attributes of Chatbot like self.ratings in this method.

        :param ratings: a (num_movies x num_users) matrix of user ratings, from
         0.5 to 5.0
        :param threshold: Numerical rating above which ratings are considered
        positive

        :returns: a binarized version of the movie-rating matrix
        """
        ########################################################################
        # TODO: Binarize the supplied ratings matrix.                          #
        #                                                                      #
        # WARNING: Do not use self.ratings directly in this function.          #
        ########################################################################

        # The starter code returns a new matrix shaped like ratings but full of
        # zeros.
        binarized_ratings = np.zeros_like(ratings)
        for i in range(1):
            binarized_ratings[ratings > threshold] = 1
            binarized_ratings[ratings <= threshold] = -1
            binarized_ratings[ratings == 0] = 0

        ########################################################################
        #                        END OF YOUR CODE                              #
        ########################################################################
        return binarized_ratings

    def similarity(self, u, v):
        """Calculate the cosine similarity between two vectors.

        You may assume that the two arguments have the same shape.

        :param u: one vector, as a 1D numpy array
        :param v: another vector, as a 1D numpy array

        :returns: the cosine similarity between the two vectors
        """
        ########################################################################
        # TODO: Compute cosine similarity between the two vectors.             #
        ########################################################################
        

        if np.linalg.norm(u) == 0:
            similarity = 0
        elif np.linalg.norm(v) == 0:
            similarity = 0
        else:
            similarity = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
        ########################################################################
        #                          END OF YOUR CODE                            #
        ########################################################################
        return similarity

    def recommend(self, user_ratings, ratings_matrix, k=10, creative=False):
        """Generate a list of indices of movies to recommend using collaborative
         filtering.

        You should return a collection of `k` indices of movies recommendations.

        As a precondition, user_ratings and ratings_matrix are both binarized.

        Remember to exclude movies the user has already rated!

        Please do not use self.ratings directly in this method.

        :param user_ratings: a binarized 1D numpy array of the user's movie
            ratings
        :param ratings_matrix: a binarized 2D numpy matrix of all ratings, where
          `ratings_matrix[i, j]` is the rating for movie i by user j
        :param k: the number of recommendations to generate
        :param creative: whether the chatbot is in creative mode

        :returns: a list of k movie indices corresponding to movies in
        ratings_matrix, in descending order of recommendation.
        """

        ########################################################################
        # TODO: Implement a recommendation function that takes a vector        #
        # user_ratings and matrix ratings_matrix and outputs a list of movies  #
        # recommended by the chatbot.                                          #
        #                                                                      #
        # WARNING: Do not use the self.ratings matrix directly in this         #
        # function.                                                            #
        #                                                                      #
        # For starter mode, you should use item-item collaborative filtering   #
        # with cosine similarity, no mean-centering, and no normalization of   #
        # scores.                                                              #
        ########################################################################

        # Populate this list with k movie indices to recommend to the user.
        recommendations = []
        lengther = len(user_ratings)
        rs = user_ratings.reshape(lengther, 1)
        concatenate_ratings = np.hstack((ratings_matrix, rs))
        user_unrated_indices = np.where(user_ratings == 0)
        user_rated_indices = np.where(user_ratings != 0)

        unrated_score_preds = []
        for i, curr_item_idx in enumerate(user_unrated_indices[0]):
            curr_item = ratings_matrix[curr_item_idx][:]
            simscores = []
            for j, other_item_idx in enumerate(user_rated_indices[0]):
                if other_item_idx is not curr_item_idx:
                    other_item = ratings_matrix[other_item_idx][:]
                    sim_score = self.similarity(curr_item, other_item)
                    simscores.append((sim_score, other_item_idx))

            recscore = np.sum([simscores[l][0] * user_ratings[simscores[l][1]] for l, item in enumerate(simscores)])
            unrated_score_preds.append((recscore, curr_item_idx))
        sorted_unrated_scores_zip = sorted(unrated_score_preds, key=lambda tup: tup[0], reverse=True)
        recommendations_zip = []
        for i in range(k):
            recommendations_zip.append(sorted_unrated_scores_zip[i])
        recommendations = []
        for i in range(k):
            recommendations.append(recommendations_zip[i][1])


        ########################################################################
        #                        END OF YOUR CODE                              #
        ########################################################################
        return recommendations

    ############################################################################
    # 4. Debug info                                                            #
    ############################################################################

    def debug(self, line):
        """
        Return debug information as a string for the line string from the REPL

        NOTE: Pass the debug information that you may think is important for
        your evaluators.
        """
        debug_info = 'debug info'
        return debug_info

    ############################################################################
    # 5. Write a description for your chatbot here!                            #
    ############################################################################
    def intro(self):
        """Return a string to use as your chatbot's description for the user.

        Consider adding to this description any information about what your
        chatbot can do and how the user can interact with it.
        """
        return """
        Your task is to implement the chatbot as detailed in the PA7
        instructions.
        Remember: in the starter mode, movie names will come in quotation marks
        and expressions of sentiment will be simple!
        TODO: Write here the description for your own chatbot!
        """

def edit_distance(a, b):
    check = 0
    a_length = len(a)
    b_length = len(b)
    if a == b:
        return check
    elif a_length == check:
        return b_length
    elif b_length == check:
        return a_length

    b_plus = b_length + 1
    zz = [None] * b_plus
    yy = [None] * b_plus

    zz_length = len(zz)
    for i in range(zz_length):
        zz[i] = i
    for i in range(a_length):
        i_plus = i + 1
        yy[check] = i_plus
        for j in range(b_length):
            o = j
            ai = a[i]
            bj = b[o]
            if ai == bj:
                extra = check
            else:
                extra = check + 2
            yy[o + 1] = min(yy[o] + 1, zz[o + 1] + 1, zz[o] + extra)
        for j in range(zz_length):
            o = j
            zz[o] = yy[o]
    b_length = len(b)
    return yy[b_length]

if __name__ == '__main__':
    print('To run your chatbot in an interactive loop from the command line, '
          'run:')
    print('    python3 repl.py')

