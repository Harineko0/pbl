function shiftswap() {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet1 = spreadsheet.getSheetByName("shifts");
    const sheet2 = spreadsheet.getSheetByName("swaps");
    if (sheet1==null||sheet2==null){
      return;
    }
    const lastRow1 = sheet1.getLastRow();
    const lastRow2 = sheet2.getLastRow();
    let range_a;
    let range_b;
    let list = sheet2.getRange(1, 2, lastRow2, 2).getValues();
    for (let i=1;i<lastRow2;i++){
      for (let j=0;j<lastRow1-1;j++){
        if(sheet1.getRange(j+2,1).getValue() == list[i][0]){
          range_a = sheet1.getRange(j+2,4);
        }
        else if(sheet1.getRange(j+2,1).getValue() == list[i][1]){
          range_b = sheet1.getRange(j+2,4);
        }
      }
    if(range_a==null||range_b==null){
      return;
    }
    let range_values_a = range_a.getValues(); 
    let range_values_b = range_b.getValues(); 
    range_a.setValues(range_values_b);
    range_b.setValues(range_values_a);
    }
  }