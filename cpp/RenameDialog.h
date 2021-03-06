// -*- C++ -*- generated by wxGlade 0.6.3 on Fri Feb 25 18:55:11 2011

#include <wx/wx.h>
#include <wx/image.h>

#ifndef RENAMEDIALOG_H
#define RENAMEDIALOG_H

// begin wxGlade: ::dependencies
// end wxGlade

// begin wxGlade: ::extracode

// end wxGlade


class RenameDialog: public wxDialog {
public:
    // begin wxGlade: RenameDialog::ids
    // end wxGlade

    RenameDialog(wxWindow* parent, int id, const wxString& title, const wxPoint& pos=wxDefaultPosition, const wxSize& size=wxDefaultSize, long style=wxDEFAULT_DIALOG_STYLE);

private:
    // begin wxGlade: RenameDialog::methods
    void set_properties();
    void do_layout();
    // end wxGlade

protected:
    // begin wxGlade: RenameDialog::attributes
    wxStaticText* nameLabel;
    wxTextCtrl* nameTextCtrl;
    wxButton* cancelButton;
    wxButton* okButton;
    // end wxGlade

    DECLARE_EVENT_TABLE();

public:
    virtual void OnOkPressed(wxCommandEvent &event); // wxGlade: <event_handler>
    virtual void OnCancelPressed(wxCommandEvent &event); // wxGlade: <event_handler>
}; // wxGlade: end class


#endif // RENAMEDIALOG_H
