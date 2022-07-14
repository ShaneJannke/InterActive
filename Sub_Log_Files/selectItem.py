#set Sub_Request_V equal to the selected sub request ID, only works after sub_log button has been pressed
def selectItem(Main_Tree, Sub_Request_V, e):
    curItem = Main_Tree.focus()
    data = Main_Tree.item(curItem)
    values = data.get("values")
    if "-" in str(values[0]):
        Sub_Request_V.set(None)
    else:
        Sub_Request_V.set(values[0])
    return