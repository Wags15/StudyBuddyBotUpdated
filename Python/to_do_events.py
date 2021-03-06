from events import Event
import datetime
import discord
import csv
import os


class CreateToDoCommand(Event):

    to_do_item: str

    def __init__(self, start_time: datetime.datetime, length: datetime.timedelta, user_id: discord.User, to_do_item: str):
        super().__init__(start_time, length, user_id)
        self.to_do_item = to_do_item

    def run_event(self, event_queue):
        file = os.path.abspath(
            'Python/database/to_do_lists/' + str(self.user_id) + '.csv')
        #  Adds the to do item to the users to do list
        items = []

        with open(file, 'a') as creation:
            creation.close()

        with open(file, 'r') as to_do_list:
            reader = csv.reader(to_do_list)
            for row in reader:
                items.append(row)

            to_do_list.close()

        items.append([len(items) + 1, self.to_do_item])

        with open(file, 'w', newline='') as to_do_list:
            writer = csv.writer(to_do_list)
            for item in items:
                writer.writerow(item)

            to_do_list.close()

    def clone_event(self):
        return CreateToDoCommand(self.start_time, self.length, self.user_id, self.to_do_item)


class DeleteToDoCommand(Event):
    to_do_number: str

    def __init__(self, start_time: datetime.datetime, length: datetime.timedelta, user_id: discord.User, to_do_number: str):
        super().__init__(start_time, length, user_id)
        self.to_do_number = to_do_number

    def run_event(self, event_queue):
        file = os.path.abspath(
            'Python/database/to_do_lists/' + str(self.user_id) + '.csv')
        items = []
        with open(file, 'r') as to_do_list:
            reader = csv.reader(to_do_list)
            for row in reader:
                items.append(row)

        for item in items:
            if item[0] == self.to_do_number:
                items.remove(item)
                break

        with open(file, 'w', newline='') as to_do_list:
            writer = csv.writer(to_do_list)
            for i in range(0, len(items)):
                writer.writerow([str(i + 1), items[i][1]])

            to_do_list.close()

    def clone_event(self):
        return DeleteToDoCommand(self.start_time, self.length, self.user_id, self.to_do_number)


class ViewToDoCommand(Event):

    def __init__(self, start_time: datetime.datetime, length: datetime.timedelta, user_id: discord.User):
        super().__init__(start_time, length, user_id)

    def run_event(self, event_queue):
        file = os.path.abspath(
            'Python/database/to_do_lists/' + str(self.user_id) + '.csv')
        output_message = 'This is your to-do list: ' + '\n'

        with open(file, 'r') as to_do_list:
            reader = csv.reader(to_do_list)

            for row in reader:
                output_message += row[0] + '. ' + row[1] + '\n'

        return output_message

    def clone_event(self):
        return ViewToDoCommand(self.start_time, self.length, self.user_id)
