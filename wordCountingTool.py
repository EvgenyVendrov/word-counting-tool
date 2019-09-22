import sys
import os
import copy


def fix_word(s):
    """
    helping - internal method to "fix" words from text, i.e confirm that there are no not needed chars
    :param s:
    the word should be fixed
    :return:
    the word 'fixed' or an empty string in case the whole word was number for exmp.
    """
    string_to_return = ''
    for char in s:
        if char.isalpha() or char == "'" or char == '-':
            string_to_return += char
    if not string_to_return:
        return ''
    # in case the last char is non letter
    if not string_to_return[-1].isalpha():
        return string_to_return[:-1]

    return string_to_return


def read_file(filename):
    """
    helping - internal method which reads a file and returns a list of tuples,
    key is the word itself and values is the repetitions amount
    :param filename:
    path to chosen file
    :return:
    list of tuples,
    key is the word itself and values is the repetitions amount
    """
    f_handler = open(filename, 'r')
    text_from_file = f_handler.read()
    list_of_words = text_from_file.split()
    # turning all words to lower case and filtering out the empty words
    list_of_words_parsed = [s.lower() for s in list_of_words if s]
    # using extra list is not that good memory - complexity wise but much easier
    list_of_all_right_words = []
    for word in list_of_words_parsed:
        if word:
            if any(not char.isalpha() for char in word):
                # if at least one of words chars are non letters - fix it
                fixed_word = fix_word(word)
                # if the word returned from 'fixing' is empty - it was a number from the start
                if fixed_word:
                    list_of_all_right_words.append(fixed_word)
            else:
                list_of_all_right_words.append(word)
    f_handler.close()
    dict_of_words_count = {}
    # counting the amount of repetitions for every word
    for word in list_of_all_right_words:
        if word not in dict_of_words_count.keys():
            dict_of_words_count[word] = 1
        else:
            dict_of_words_count[word] += 1
    return dict_of_words_count.items()


def basic_count(filename):
    """
    creating a list of all words from the file, ordered in a lexicographic order with their amount of repetitions
    :param filename:
    path to the file
    :return:
    lexicographic ordered list of all words and their amount of repetitions
    """
    tuples_of_words_count = read_file(filename)
    tuples_of_words_count.sort(key=lambda tup: tup[0])
    return tuples_of_words_count


def top_count(filename):
    """
    creating a list of all the top 20 most common words in the file, ordered by the amount of repetitions with their amount of repetitions
    :param filename:
    path to the file
    :return:
    list which is ordered by the amount of repetition containing top 20 most common words
    :param filename:
    :return:
    """
    tuples_of_words_count = read_file(filename)
    tuples_of_words_count.sort(key=lambda tup: tup[1], reverse=True)
    return tuples_of_words_count[:20]


def getTopWords(returned_tuple_list):
    """
     helping - internal method to return top 3 most common words out of the tuple list received - used in "basic count" routine
    :param returned_tuple_list:
    tuple list of all the words with their amount of repetition
    :return:
    list of the top 3 most common words
    """
    returned_tuple_list.sort(key=lambda tup: tup[1], reverse=True)
    return returned_tuple_list[:3]


def main():
    # checking whether we got enough arguments to use the tool
    if len(sys.argv) != 3:
        print('WRONG USE: you should use it as [programName.py] --[flag] [path to file]')
        print('program shuts down')
        sys.exit(1)
    # checking the flag is correctly passed
    flag = sys.argv[1]
    if flag[:2] != '--':
        print('WRONG USE: cannot find "--" symbol for flag')
        print('program shuts down')
        sys.exit(1)
    # checking that flag argument is valid
    if flag[2:] != 'topcount' and flag[2:] != 'basiccount':
        print('WRONG USE: flag can be only "topcount" or "basiccount" - please check documentation')
        print('program shuts down')
        sys.exit(1)
    # checking that files path is valid
    file_name = sys.argv[2]
    if not os.path.exists(file_name) or not os.path.isfile(file_name):
        print('WRONG USE: path to file has to be a valid path to file')
        print('program shuts down')
        sys.exit(1)
    # checking that the file is indeed a .txt one
    if not file_name.endswith('.txt'):
        print("WRONG USE: file isn't txt - working only on txt files")
        print('program shuts down')
        sys.exit(1)
    # activating the right function and outputting the "CONCLUSION"
    count = 1
    returned_tuple_list = []
    top_3_words = []
    if flag == '--topcount':
        returned_tuple_list = top_count(file_name)
        for tuple in returned_tuple_list:
            print(str(count) + ')' + '"' + tuple[0] + '"' + ', repetitions:' + str(tuple[1]))
            count += 1
            top_3_words += returned_tuple_list[:3]

    elif flag == '--basiccount':
        returned_tuple_list = basic_count(file_name)
        top_3_words = getTopWords(copy.deepcopy(returned_tuple_list))
        for tuple in returned_tuple_list:
            print(str(count) + ')' + '"' + tuple[0] + '"' + ', repetitions:' + str(tuple[1]))
            count += 1
    all_words_rep_combined = [s[1] for s in returned_tuple_list]
    print('~' * 50)
    print('CONCLUSION:')
    print(
        'number of words in txt file: %d \nnumber of unique words in file: %d \ntop 3 most common words are: \n1.%s \n2.%s \n3.%s' % (
            sum(all_words_rep_combined), count - 1, top_3_words[0], top_3_words[1], top_3_words[2]))


if __name__ == '__main__':
    main()
