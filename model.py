from typing import List
from typing import Any
from dataclasses import dataclass
import json


@dataclass
class ImageLinks:
    smallThumbnail: str
    thumbnail: str

    @staticmethod
    def from_dict(obj: Any) -> 'ImageLinks':
        _smallThumbnail = str(obj.get("smallThumbnail"))
        _thumbnail = str(obj.get("thumbnail"))
        return ImageLinks(_smallThumbnail, _thumbnail)


@dataclass
class PanelizationSummary:
    containsEpubBubbles: bool
    containsImageBubbles: bool

    @staticmethod
    def from_dict(obj: Any) -> 'PanelizationSummary':
        if obj is None:
            _containsEpubBubbles = False
            _containsImageBubbles = False
        else:
            _containsEpubBubbles = obj.get("containsEpubBubbles")
            _containsImageBubbles = obj.get("containsImageBubbles")
        return PanelizationSummary(_containsEpubBubbles, _containsImageBubbles)


@dataclass
class ReadingModes:
    text: bool
    image: bool

    @staticmethod
    def from_dict(obj: Any) -> 'ReadingModes':
        _text = obj.get("text")
        _image = obj.get("image")
        return ReadingModes(_text, _image)


@dataclass
class VolumeInfo:
    title: str
    subtitle: str
    authors: List[str]
    publisher: str
    publishedDate: str
    description: str
    readingModes: ReadingModes
    pageCount: int
    printType: str
    categories: List[str]
    maturityRating: str
    allowAnonLogging: bool
    contentVersion: str
    panelizationSummary: PanelizationSummary
    imageLinks: ImageLinks
    language: str
    previewLink: str
    infoLink: str
    canonicalVolumeLink: str

    @staticmethod
    def from_dict(obj: Any) -> 'VolumeInfo':
        _title = str(obj.get("title"))
        _subtitle = str(obj.get("subtitle"))
        _authors = obj.get("authors")
        _publisher = str(obj.get("publisher"))
        _publishedDate = str(obj.get("publishedDate"))
        _description = str(obj.get("description"))
        _readingModes = ReadingModes.from_dict(obj.get("readingModes"))
        _pageCount = str(obj.get("pageCount"))
        _printType = str(obj.get("printType"))
        _categories = obj.get("categories")
        _maturityRating = str(obj.get("maturityRating"))
        _allowAnonLogging = obj.get("allowAnonLogging")
        _contentVersion = str(obj.get("contentVersion"))
        _panelizationSummary = PanelizationSummary.from_dict(obj.get("panelizationSummary"))
        _imageLinks = ImageLinks.from_dict(obj.get("imageLinks"))
        _language = str(obj.get("language"))
        _previewLink = str(obj.get("previewLink"))
        _infoLink = str(obj.get("infoLink"))
        _canonicalVolumeLink = str(obj.get("canonicalVolumeLink"))
        return VolumeInfo(_title, _subtitle, _authors, _publisher, _publishedDate, _description, _readingModes,
                          _pageCount, _printType, _categories, _maturityRating, _allowAnonLogging, _contentVersion,
                          _panelizationSummary, _imageLinks, _language, _previewLink, _infoLink, _canonicalVolumeLink)


@dataclass
class Book:
    kind: str
    id: str
    etag: str
    selfLink: str
    volumeInfo: VolumeInfo

    @staticmethod
    def from_dict(obj: Any) -> 'Book':
        _kind = str(obj.get("kind"))
        _id = str(obj.get("id"))
        _etag = str(obj.get("etag"))
        _selfLink = str(obj.get("selfLink"))
        _volumeInfo = VolumeInfo.from_dict(obj.get("volumeInfo"))
        return Book(_kind, _id, _etag, _selfLink, _volumeInfo)


