from __future__ import annotations

import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Variables for the script

README_START_PHRASE = "<!-- (begin - auto update-readme) -->"
README_END_PHRASE = "<!-- (end - auto update-readme) -->"

PREFIX_TO_REMOVE = [
    "Abschlusszertifikat_"
]

PROVIDER_URLS = {
    "linkedin-learning": "https://www.linkedin.com/learning",
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def main():
    # get all the certificates in the certificates folder
    # search recursively in all subdirectories in the folder
    certificates = []
    for root, dirs, files in os.walk("certificates"):
        for file in files:
            if file.endswith(".pdf"):
                certificates.append(os.path.join(root, file))

    # sort the certificates by the date they were created
    certificates.sort(key=os.path.getctime, reverse=True)
    # certificates = remove_prefix_from_certificates(certificates)

    # print(certificates)
    readme = split_readme(read_readme())

    readme_beginning = readme[0]
    readme_certificates = readme[1]
    readme_end = readme[2]

    new_part, diff = update_readme_certificates(certificates, readme_certificates)

    # concatenate the readme parts and save them
    save_readme(readme_beginning + new_part + readme_end)


def update_readme_certificates(collected_certificates: list, readme_certificates_part: str):
    """
    this function updates the certificates part of the readme file. It adds the certificates to the readme file.

    :param collected_certificates: the certificates to add
    :param readme_certificates_part: the part of the readme file that contains the certificates
    :return: the updated certificates part of the readme file
    """
    new_readme_certificates_part = f"{README_START_PHRASE}\n| Certificate | Provider |\n|-------------|----------|\n"

    for cert in collected_certificates:
        provider = os.path.basename(os.path.dirname(cert))
        linked_provider = update_provider_info(provider)
        display_name = remove_prefix_from_certificate(os.path.basename(cert)).replace("_", " ").removesuffix(".pdf")

        new_readme_certificates_part += f"| [{display_name}]({cert}) | {linked_provider} |\n"

    # remove the last line bread
    new_readme_certificates_part += f"{README_END_PHRASE}"
    diff = len(new_readme_certificates_part) - len(readme_certificates_part)

    print("Diff: ", diff)

    return new_readme_certificates_part, diff


def update_provider_info(provider: str):
    """
    this function updates the provider info in the readme file

    :param provider: the provider to update
    """
    if provider.lower() in PROVIDER_URLS:
        return f"[{provider}]({PROVIDER_URLS[provider.lower()]})"
    else:
        return provider


def remove_prefix_from_certificate(certificates: str):
    """
    this function removes the prefix from the certificates

    :param certificates: the certificates to remove the prefix from
    :return: the certificates without the prefix
    """
    for prefix in PREFIX_TO_REMOVE:
        return certificates.replace(prefix, "")


def read_readme():
    """
    simple function to read the readme file

    :return: the readme file as a string
    """
    with open("README.md", "r") as file:
        return file.read()


def save_readme(readme: str):
    """
    simple function to save the readme file

    :param readme: the readme file as a string
    """
    with open("README.md", "w") as file:
        file.write(readme)


def split_readme(readme: str):
    """
    this function splits the readme file in three logical parts. The first part ist the beginning of
    the document, the second part represents the certificates to be updated and the third part is
    the end of the document.

    :param readme: the readme file to split as a string
    :return: the readme as three parts
    """
    start = readme.find(README_START_PHRASE)
    end = readme.find(README_END_PHRASE)
    return readme[:start], readme[start:end + len(README_END_PHRASE)], readme[end + len(README_END_PHRASE):]


if __name__ == "__main__":
    main()
