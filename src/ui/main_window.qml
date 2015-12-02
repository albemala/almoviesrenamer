import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import QtQuick.Window 2.0

ApplicationWindow {
    id: window
    visible: true
    width: 700
    height: 600
    title: "ALMoviesRenamer"

    signal addMovieButtonClicked()
    signal movieItemSelected(var row)
    signal movieAlternativeTitleChanged(var index)
    signal searchMovieButtonClicked()

    property alias moviesTableCurrentRow: moviesTableView.currentRow
    property alias searchAlternativeTitleText: searchAlternativeTitleTextField.text
    property alias searchAlternativeYearText: searchAlternativeYearTextField.text
    property alias searchAlternativeLanguageText: searchAlternativeLanguageTextField.text

    menuBar: MenuBar {
        Menu {
            title: "Movies"
            MenuItem {
                text: "Add movies..."
                iconSource: "../icons/movie_add.png"
            }
            MenuItem {
                text: "Add all movies in folder..."
                iconSource: "../icons/movies_from_folder.png"
            }
            MenuItem {
                text: "Add all movies in folder (including subfolders)..."
                iconSource: "../icons/movies_from_folder.png"
            }
            MenuSeparator {}
            MenuItem {
                text: "Remove selected movies from list"
                iconSource: "../icons/movie_remove.png"
            }
            MenuItem {
                text: "Remove all movies from list"
                iconSource: "../icons/movie_erase.png"
            }
            MenuSeparator {}
            MenuItem {
                text: "Change renaming rule..."
                iconSource: "../icons/tag.png"
            }
            MenuSeparator {}
            MenuItem {
                text: "Rename movies"
                iconSource: "../icons/pencil.png"
            }
        }
        Menu {
            title: "Application"
            MenuItem {
                text: "Preferences..."
            }
            MenuItem {
                text: "About..."
            }
        }
    }

    ColumnLayout {
        id: columnLayout1
        anchors.fill: parent

        RowLayout {
            spacing: 6
            Layout.leftMargin: 11
            Layout.rightMargin: 11
            Layout.topMargin: 11
            Layout.bottomMargin: 11

            Button {
                text: "Add movies"
                iconSource: "../icons/movie_add.png"
                onClicked: addMovieButtonClicked()
            }
            Button {
                text: "Remove movies"
                iconSource: "../icons/movie_remove.png"
//                onClicked: addMovieButtonClicked()
            }
            Item {
                width: 11
            }
            Button {
                text: "Renaming rule"
                iconSource: "../icons/tag.png"
//                onClicked: addMovieButtonClicked()
            }
            Item {
                width: 11
            }
            Button {
                text: "Rename movies"
                iconSource: "../icons/pencil.png"
//                onClicked: addMovieButtonClicked()
            }
        }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: "lightGray"
        }

        ColumnLayout {
            id: loadingPanel
            spacing: 6
            Layout.leftMargin: 11
            Layout.rightMargin: 11
            Layout.topMargin: 11
            Layout.bottomMargin: 11
            visible: loadingPanelVisible

            Label {
                text: "Getting information from:"
            }
            Label {
                text: loadingInfo
            }
            BusyIndicator {
                running: loadingPanelVisible
            }
            Label {
                text: "This may take a while... I will play a sound when it finishes."
            }
        }

        TableView{
            id: moviesTableView
            Layout.leftMargin: 11
            Layout.rightMargin: 11
            Layout.topMargin: 11
            Layout.bottomMargin: 11
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: moviesTableViewModel

            onClicked: movieItemSelected(row)

            TableViewColumn{
                role: "original_name"
                title: "Original name"
            }
            TableViewColumn{
                role: "new_name"
                title: "New name"
            }
        }

        ColumnLayout {
            spacing: 6
            visible: movieInfoPanelVisible
            Layout.leftMargin: 11
            Layout.rightMargin: 11
            Layout.topMargin: 11
            Layout.bottomMargin: 11

            Label {
                text: "Movie:"
            }
            ComboBox {
                Layout.fillWidth: true
                model: movieAlternativeTitlesModel
                currentIndex: movieAlternativeTitleIndex

                onCurrentIndexChanged: movieAlternativeTitleChanged(currentIndex)
            }
            GridLayout {
                rowSpacing: 6
                columnSpacing: 6
                columns: 2

                Label { text: "Title:" }
                Label { text: movieTitle }

                Label { text: "Original title:" }
                Label { text: movieOriginalTitle }

                Label { text: "Year:" }
                Label { text: movieYear }

                Label { text: "Director(s):" }
                Label { text: movieDirectors }

                Label { text: "Duration:" }
                Label { text: movieDuration }

                Label { text: "Language:" }
                Label { text: movieLanguage }
            }
            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: "lightGray"
            }
            Label {
                text: "Not the right movie? Search for another one:"
            }
            GridLayout {
                rowSpacing: 6
                columnSpacing: 6
                columns: 3

                Label { text: "Title:" }
                Label { text: "Year:" }
                Label { text: "Language:" }
                TextField {
                    id: searchAlternativeTitleTextField
                    Layout.fillWidth: true
                    placeholderText: "Title"
                }
                TextField {
                    id: searchAlternativeYearTextField
                    placeholderText: "Year"
                }
                TextField {
                    id: searchAlternativeLanguageTextField
                    placeholderText: "Language"
                }
            }
            RowLayout {
                spacing: 6
                Button {
                    text: "Search"

                    onClicked: searchMovieButtonClicked()
                }
                BusyIndicator {
                    running: searchAlternativeMovieProgressBarVisible
                }
            }
        }

        Label {
            visible: movieRenamedPanelVisible
            Layout.leftMargin: 11
            Layout.rightMargin: 11
            Layout.topMargin: 11
            Layout.bottomMargin: 11
            text: "This movie has been correctly renamed."
            color: "green"
        }

        ColumnLayout {
            spacing: 6
            visible: movieErrorPanelVisible
            Layout.leftMargin: 11
            Layout.rightMargin: 11
            Layout.topMargin: 11
            Layout.bottomMargin: 11

            Label {
                text: "There has been the following error during renaming:"
            }
            Label {
                text: movieError
                color: "red"
            }
        }
    }
}
