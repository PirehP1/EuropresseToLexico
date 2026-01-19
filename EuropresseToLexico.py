#!/usr/bin/python3
# coding: utf-8

from bs4 import BeautifulSoup
import re
import calendar
import locale
from lxml import etree
import string
import csv


def get_date(date_string):
    """
    Gets date and formats it in friendly sorting way.

    :param date_string: The original date string parsed in HTML file
    :return: The date well formated
    """

    article_date = re.search(r"(\d{1,2}) (\w+) (\d{4})", date_string)
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
    # journal_title = journal_title.replace(" ", "-")
    # journal_title = journal_title.replace("'", "")
    # journal_title = journal_title.replace(",", "")
    journal_title = re.sub(r'\W+', '', journal_title)
    return journal_title


def get_title(title_string):
    """
    Return article's title well formated.

    :param title_string: The original title string parsed in HTML file
    :return: The article's title well formated
    """
    title = title_string.text
    title = re.sub(r'\W+', '', title)
    # for c in string.punctuation:
    #     title = title_string.text.replace(c, "")
    # title = title.replace(" ", "-")
    # title = title.replace("*", "")
    # title = title.replace("\"", "")
    # title = title.replace("'", "")
    # title = title.replace(",", "-")
    # title = title.replace(";", "-")
    # title = title.replace(":", "")
    return title


def get_author(author_string):
    """
    Returns article's author when there
    is one in the original HTML file.

    :param title_string: The original date string parsed in HTML file
    :return: The article's title well formated
    """

    if author_string is not None:
        author_string = author_string.text
        author_string = author_string.replace(" ", "-")
        author_string = author_string.replace(",", "-")
        author_string = author_string.replace(";", "-")
        author_string = author_string.replace("*", "")
        return author_string
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
        if article_title is not None:
            article["title"] = get_title(article_title)
        else:
            article["title"] = None

        article_author = a.find("div", {"class", "docAuthors"})
        if article_author is not None:
            author = get_author(article_author)
            article["author"] = author

        article_content = a.find("div", {"class", "docOcurrContainer"})
        # article_content_t = article_content.text
        # article_content_t = article_content_t.encode('utf-8', errors='ignore')
        # article_content_tp = article_content_t.decode()
        # article_content_tp = re.sub(r'[^\x00-\x7F]+', ' ', article_content_t)
        # removelist = r".,;!?:’'ʼ\s\n-"
        # article_content_tp = re.sub(r'[^\w'+removelist+']', '', article_content_t)
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
            adate = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", a["date"])
            day = adate.group(3)
            month = adate.group(2)
            year = adate.group(1)
            # file.write("\n**** *date_{} *journal_{} \n\n"
            #            .format(a["date"], a["journal"]))
            if "author" in a:
                file.write("\n**** *date_{} *annee_{} *mois_{} *jour_{} *journal_{} *author_{} *title_{}\n"
                           .format(a["date"], year, month, day, a["journal"],
                                   a["author"], a["title"]))
                # file.write("\n**** *date_{} *annee_{} *mois_{} *jour_{}"
                #            .format(a["date"], year, month, day))
            else:
                file.write("\n**** *date_{} *annee_{} *mois_{} *jour_{} *journal_{} *title_{}\n".format(a["date"], year, month, day, a["journal"], a["title"]))
                # file.write("\n**** *date_{} *annee_{} *mois_{} *jour_{}"
                #            .format(a["date"], year, month, day))
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
        final_content = "\n".join(lines_lenght(a["content"], 10))
        texte = final_content
        texte = texte.replace("<", "")
        texte = texte.replace(">", "")
        texte = texte.replace("&", "et")
        article_node.text = texte
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
                file.write(
                    "Date : {} Journal : {} Title : {} Auteur : {}\n".format(
                        a["date"], a["journal"], a["title"], a["author"]))
            else:
                file.write("Date : {} Journal : {} Title : {}\n".format(
                    a["date"], a["journal"], a["title"]))

            file.write("{}\n".format(a["content"]))
    return print("Corpus exporté au format textuel simple !")


def export_csv(articles):
    """
    Exports the corpus of articles in csv file.

    :param articles: list containing all the dictionnaries
    of articles.
    :return : csv file in current dir.
    """

    csv_columns = ["date", "journal", "title", "author", "content"]
    with open("corpus.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for a in articles:
            if "author" in a:
                writer.writerow(a)
            else:
                a["author"] = ""
                writer.writerow(a)

    return print("Corpus exporté au CSV !")


if __name__ == "__main__":
    # Set the path to Europress exported HTML file

    mess = "Entrez le chemin vers le fichier HTML Europress : "
    html_source = input(mess)

    # Set locale variable for french calendar
    locale.setlocale(locale.LC_ALL, "fr_FR.utf8")

    # Calling the functions
    results = html_parser(html_source)

    corpus_t = input("Format de corpus (lexico, iramuteq, txm, text ou csv) : ")

    if corpus_t == "lexico":
        export_lexico3(results)
    elif corpus_t == "iramuteq":
        export_iramuteq(results)
    elif corpus_t == "txm":
        export_txm(results)
    elif corpus_t == "text":
        export_text(results)
    elif corpus_t == "csv":
        export_csv(results)
    else:
        print("Format de corpus non reconnu.")
