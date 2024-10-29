[{id:1,position:1},{id:3,position:2},{..},{..}]

drag and drop so that we can shorting, using this algorithm we can update position unique

1,2,3,4,5,6,7,8,9,10,11,12

breath_hold = 3
difference_value = current_value - target_value
total_items_from_target_position_from_first_item = first_item_position - target_value 
total_items_from_target_position_from_last_item = last_item_position - target_value 

case 1: when difference_value is less than equal to breath_hold value
    update_index(current_value,target_value)=> here we are going to drag and drop between less number of data so we can update all items.

case 2: when total_items_from_target_position_from_first_item is less than equal to breath_hold value:
    update_index_first_part(current_value,target_value)=> here we are going to update position and ensure unique position by updating all position of first part

case 3: when total_items_from_target_position_from_last_item is less than equal to breath_hold value:
    update_index_last_part(current_value,target_value)=> here we are going to update position and ensure unique position by updating all position of last part

else:
    decimal_update(current_value,target_value) => this update current_value to target value in decimal way. 