import os
import collections
import glob


SearchResult = collections.namedtuple('SearchResult',
                                      'file, line, text')


def main():
    print_header()

    folder = get_folder()

    if not folder:
        print('no such folder')
        return

    text = get_search_text()

    if not text:
        print('cant find this text')
        return

    matches = search_folders(folder, text)

    for each_match in matches:
        print('------------MATCH------------')
        print('file: ' + each_match.file)
        print('line: {}'.format(each_match.line))
        print('text: ' + each_match.text)
        print()


def print_header():
    print('---------------------------')
    print('--------file search--------')
    print('---------------------------')


def get_folder():
    user_input_folder = input('search folder: ')

    if not user_input_folder or not user_input_folder.strip():
        return None

    if not os.path.isdir(user_input_folder):
        return None

    return os.path.abspath(user_input_folder)


def get_search_text():
    text = input('search text: ')
    return text.lower()


def search_folders(folder, text):
    print('searching for {} from {}'.format(text, folder))

    # all_matches = []
    items_in_folder = glob.glob(os.path.join(folder, '*'))

    for each_item in items_in_folder:
        item_full_path = os.path.join(folder, each_item)
        if os.path.isdir(item_full_path):
            matches = search_folders(item_full_path, text)
            # all_matches.extend(matches)

            # for each_match in matches:
            #     yield each_match

            yield from matches
        else:
            matches = search_file(item_full_path, text)
            # all_matches.extend(matches)
            for each_match in matches:
                yield each_match

            yield from matches

    # return all_matches


def search_file(filename, search_text):
    # matches = []

    with open(filename, 'r', encoding='utf-8') as fin:
        line_number = 0
        for line in fin:
            line_number += 1
            if line.find(search_text) >= 0:
                each_match = SearchResult(line=line_number, file=filename, text=line)
                # matches.append(each_match)
                yield each_match


if __name__ == '__main__':
    main()
