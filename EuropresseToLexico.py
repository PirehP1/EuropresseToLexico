#!/usr/bin/python3
# coding: utf-8

from bs4 import BeautifulSoup
import re
import calendar
import locale
from lxml import etree
import string


def get_date(date_string):
    """
    Gets date and formats it in friendly sorting way.

    :param date_string: The original date string parsed in HTML file
    :return: The date well formated
    """

    article_date = re.search("(\d{1,2}) (\w+) (\d{4})", date_string)
    day = article_date.group(1)
    day = "{num:02d}".format(num=int(day))
    month = article_date.group(2)
    year = article_date.group(3)
    abbr_to_num = {name: num for num,
                   name in enumerate(calendar.month_name) if num}
    month = abbr_to_num[month]
    month = "{num:02d}".format(num=month)
    good_date = "{}-{}-{}".format(year, month, day)
    return good_date


def get_journal(journal_string):
    """
    Returns journal's title well formated.

    :param journal_string: The original journal's title
    string parsed in HTML file
    :return: The journal's title well formated
    """

    journal_title = journal_string.text.strip()
    journal_title = journal_title.replace(" ", "-")
    return journal_title


def get_title(title_string):
    """
    Return article's title well formated.

    :param title_string: The original title string parsed in HTML file
    :return: The article's title well formated
    """

    for c in string.punctuation:
        title = title_string.text.replace(c, "")
    title = title.replace(" ", "-")
    title = title.replace("*", "")
    title = title.replace("\"", "")
    return title


def get_author(author_string):
    """
    Returns article's author when there
    is one in the original HTML file.

    :param title_string: The original date string parsed in HTML file
    :return: The article's title well formated
    """

    if author_string is not None:
        journal_title = author_string.text.replace(" ", "-")
        journal_title = journal_title.replace("*", "")
        return journal_title
    else:
        return None


def html_parser(source):
    """
    Parses the html file exported from Europress
    and call the above functions to get the variables
    and the contents of the articles.

    :param source: Path to the original HTML file
    :return: a list of dictionnaries containing
    the variables and the content for each article
    """

    html = open(source, "r")
    content = html.read()
    soup = BeautifulSoup(content, "lxml")

    exported_articles = []

    articles = soup.findAll("article")
    for a in articles:
        article = {}

        journal_title = a.find("span", {"class", "DocPublicationName"})
        article["journal"] = get_journal(journal_title)

        article_date = a.find("span", {"class", "DocHeader"})
        article["date"] = get_date(article_date.text)

        article_title = a.find("p", {"class",
                                     "titreArticleVisu rdp__articletitle"})
        article["title"] = get_title(article_title)

        article_author = a.find("div", {"class", "docAuthors"})
        if article_author is not None:
            author = get_author(article_author)
            article["author"] = author

        article_content = a.find("div", {"class", "docOcurrContainer"})
        article["content"] = article_content.text

        exported_articles.append(article)

    return exported_articles


def lines_lenght(string, width):
    """
    Slices a string according a number of words
    as length limit.

    :param string: string to slice.
    :param width: number of words.
    :return : a list containing the lines
    """

    words = string.split()
    for i in range(0, len(words), width):
        yield " ".join(words[i:i+width])


def export_lexico3(articles):
    """
    Exports the corpus of articles in a text
    file formated for Lexico3 software.

    :param articles: list containing all the dictionnaries
    of articles.
    :return : confirmation string in stdout.
    """

    with open("corpus_lexico3.txt", "w") as file:
        for a in articles:
            file.write("<date={}>\r".format(a["date"]))
            file.write("<journal={}>\r".format(a["journal"]))
            file.write("<title={}>\r".format(a["title"]))
            if "author" in a:
                file.write("<author={}>\r".format(a["author"]))

            file.write("{}\r".format(a["content"]))
    return print("Corpus exporté au format Lexico3 !")


def export_iramuteq(articles):
    """
    Exports the corpus of articles in a text
    file formated for Iramuteq software.

    :param articles: list containing all the dictionnaries
    of articles.
    :return : confirmation string in stdout.
    """

    with open("corpus_Iramuteq.txt", "w") as file:
        for a in articles:
            if "author" in a:
                file.write("**** *date_{} *journal_{} *author_{} *title_{}\n"
                           .format(a["date"], a["journal"],
                                   a["author"], a["title"]))
            else:
                file.write("**** *date_{} *journal_{} *title_{}\n"
                           .format(a["date"], a["journal"], a["title"]))

            contenu = a["content"].replace("*", "")
            file.write("{}\n".format(contenu))
    return print("Corpus exporté au format Iramuteq !")


def export_txm(articles):
    """
    Exports the corpus of articles in a XML
    file formated for TXM software.

    :param articles: list containing all the dictionnaries
    of articles.
    :return : confirmation string in stdout.
    """

    root_final = etree.Element("corpus")
    doc = etree.ElementTree(root_final)
    for a in articles:
        if "author" in a:
            article_node = etree.SubElement(root_final, "article",
                                            date="{}".format(a["date"]),
                                            journal="{}".format(a["journal"]),
                                            titre="{}".format(a["title"]),
                                            auteur="{}".format(a["author"]))
        else:
            article_node = etree.SubElement(root_final, "article",
                                            date="{}".format(a["date"]),
                                            journal="{}".format(a["journal"]),
                                             titre="{}".format(a["title"]))
        final_content = "\n\r".join(lines_lenght(a["content"], 10))
        article_node.text = final_content
    doc.write("corpus_TXM.xml", xml_declaration=True, encoding="utf-8")
    return print("Corpus exporté au format TXM !")


def export_text(articles):
    """
    Exports the corpus of articles in a simple
    text file with no specific formating.

    :param articles: list containing all the dictionnaries
    of articles.
    :return : confirmation string in stdout.
    """

    with open("corpus_text.txt", "w") as file:
        for a in articles:
            if "author" in a:
                file.write("Date : {} Journal : {} Title : {} Auteur : {}\n".format(a["date"], a["journal"], a["title"], a["author"]))
            else:
                file.write("Date : {} Journal : {} Title : {}\n".format(a["date"], a["journal"], a["title"]))

            file.write("{}\n".format(a["content"]))
    return print("Corpus exporté au format textuel simple !")


if __name__ == "__main__":
    # Set the path to Europress exported HTML file

    mess = "Entrez le chemin vers le fichier HTML Europress : "
    html_source = input(mess)

    # Set locale variable for french calendar
    locale.setlocale(locale.LC_ALL, "fr_FR.utf8")

    # Calling the functions
    results = html_parser(html_source)

    corpus_t = input("Format de corpus (lexico, iramuteq, txm ou text) : ")

    if corpus_t == "lexico":
        export_lexico3(results)
    elif corpus_t == "iramuteq":
        export_iramuteq(results)
    elif corpus_t == "txm":
        export_txm(results)
    elif corpus_t == "text":
        export_text(results)
    else:
        print("Format de corpus non reconnu.")
