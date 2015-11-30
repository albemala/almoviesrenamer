import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import QtQuick.Window 2.0

ApplicationWindow {
    id: window
    visible: true
    width: 600
    height: 600
    title: "ALMoviesRenamer"

    signal addMovieButtonClicked()
    signal movieItemSelected(var row)
    signal movieAlternativeTitleChanged(var index)
    signal searchMovieButtonClicked()

    property alias moviesTableCurrentRow: moviesTableView.currentRow

    menuBar: MenuBar {
        Menu {
            title: "Movies"
            MenuItem {
                text: "Add movies..."
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

    toolBar: ToolBar {
        id: toolBar
        RowLayout {
            ToolButton {
                text: "Add"

                onClicked: addMovieButtonClicked()
            }
        }
    }

    ColumnLayout {
        id: columnLayout1
        anchors.fill: parent

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
            ProgressBar {
                Layout.fillWidth: true
                indeterminate: true
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
                    Layout.fillWidth: true
                    placeholderText: "Title"
                }
                TextField { placeholderText: "Year" }
                TextField { placeholderText: "Language" }
            }
            RowLayout {
                spacing: 6
                Button {
                    text: "Search"

                    onClicked: searchMovieButtonClicked()
                }
                ProgressBar {
                    Layout.fillWidth: true
                    indeterminate: true
                    visible: searchAlternativeMovieProgressBarVisible
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
