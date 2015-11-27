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

    property string fileName: ""
    property alias moviesModel: moviesModel

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
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent

        ColumnLayout {
            id: loadingLayout
            Label {
                id: name
                text: fileName
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
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: ListModel {
                id: moviesModel

                ListElement {
                    originalName: "qwe"
                    newName: "rty"
                }
            }

            TableViewColumn{
                role: "originalName"
                title: "Original name"
            }
            TableViewColumn{
                role: "newName"
                title: "New name"
            }
        }

        ColumnLayout {
            Label {
                text: "Movie:"
            }
            ComboBox {
                Layout.fillWidth: true

            }
            GridLayout {
                columns: 2

                Label { text: "Title:" }
                Label { text: "titolo" }

                Label { text: "Original title:" }
                Label { text: "titolo originale" }

                Label { text: "Year:" }
                Label { text: "anno" }
            }
            Label {
                text: "Not the right movie? Search for another one:"
            }
            GridLayout {
                columns: 3

                Label { text: "Title:" }
                Label { text: "Year:" }
                Label { text: "Language:" }
                TextField { placeholderText: "Title" }
                TextField { placeholderText: "Year" }
                TextField { placeholderText: "Language" }
            }
            RowLayout {
                Button {
                    text: "Search"
                }
                ProgressBar {
                    Layout.fillWidth: true
                    indeterminate: true
                }
            }
        }

        Label {
            text: "This movie has been correctly renamed."
            color: "green"
        }

        ColumnLayout {
            Label {
                text: "There has been the following error during renaming:"
            }
            Label {
                text: "Error!"
                color: "red"
            }
        }
    }
}
