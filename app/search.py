import re


def search_author_from_paper(db_cursor, list_of_authors_from_paper):
    authors_from_table = db_cursor.execute('select name from authors').fetchall()
    result = [(a, False) for a in list_of_authors_from_paper]
    for index, a in enumerate(result):
        for b in authors_from_table:
            if a[0].lower().strip() == b[0].lower().strip():
                result[index] = (b[0], True)
                break
    return result


def search_paper_from_author(db_cursor, author_name):
    papers_from_table = db_cursor.execute('select * from papers').fetchall()
    result = []
    # row[3], row[6]
    for p in papers_from_table:
        author_list = [p[3]] + p[6].split(',')
        if author_name in author_list:
            result.append(p[0])

    return result


def calculate_rank(papers_or_authors, search_query):
    # calculate search page rank using cosine similarity metric
    score_rank = []
    title_or_authors_rank = []
    for index, paper in enumerate(papers_or_authors):
        title = re.sub(r'[^\w\s]|_', '', paper[0]).lower().split(' ') if paper[0] is not None else ['']
        length_of_intersection = len(set(search_query).intersection(set(title)))
        l2_norm = len(search_query) * len(title)
        cosine = (length_of_intersection / float(l2_norm)) if l2_norm != 0 else 0
        score_rank.append(cosine)
        title_or_authors_rank.append(paper[0] if paper[0] is not None else '')
    rank_index = [x for (y, x) in sorted(zip(score_rank, range(len(title_or_authors_rank))), reverse=True)]
    title_or_authors_rank = [title_or_authors_rank[i] for i in rank_index]
    score_rank = [score_rank[i] for i in rank_index]
    return title_or_authors_rank, rank_index, score_rank


def search(search_query, search_category, db_cursor, num_result):
    to_be_returned = ([], [], [], [])
    # search category for title
    db_cursor.execute('select * from papers')
    papers = db_cursor.fetchall()
    title_rank, rank_index_paper, score_rank_paper = calculate_rank(papers, search_query)
    db_cursor.execute('select * from authors')
    authors = db_cursor.fetchall()
    author_rank, rank_index_author, score_rank_author = calculate_rank(authors, search_query)
    num_of_papers = num_result
    num_of_authors = num_result
    for i in range(num_result):
        if score_rank_paper[i] == 0.0:
            num_of_papers = i
            break
    for i in range(num_result):
        if score_rank_author[i] == 0.0:
            num_of_authors = i
            break

    if search_category == 'p':
        if score_rank_paper[0] == 0.0:
            print("Your search did not match any paper!!!")
            to_be_returned = (["Your search did not match any paper!!!"], [])
        else:
            to_be_returned = (title_rank[0:num_of_papers], [])

    elif search_category == 'a':
        if score_rank_author[0] == 0.0:
            to_be_returned = ([], ["Your search did not match any author!!!"])
        else:
            to_be_returned = ([], author_rank[0:num_of_authors])

    # search category for both
    elif search_category == 'pa':
        if score_rank_paper[0] == 0.0 and score_rank_author[0] == 0.0:
            print("Your search did not match any shit!!!")
            to_be_returned = (["Your search did not match any paper!!!"], ["Your search did not match any author!!!"])

        elif score_rank_paper[0] == 0.0 and score_rank_author[0] > 0.0:
            print("Your search did not match any paper!!!")
            to_be_returned = (["Your search did not match any paper!!!"], author_rank[0:num_of_authors])

        elif score_rank_paper[0] > 0.0 and score_rank_author[0] == 0:
            print("Your search did not match any author!!!")
            to_be_returned = (title_rank[0:num_of_papers], ["Your search did not match any author!!!"])

        elif score_rank_paper[0] > 0.0 and score_rank_author[0] > 0.0:
            to_be_returned = (title_rank[0:num_of_papers], author_rank[0:num_of_authors])

    return to_be_returned
