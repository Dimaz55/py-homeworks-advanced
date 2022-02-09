# coding: utf-8
import re
import csv

if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    result = [contacts_list[0]]
    contacts_list.pop(0)

    pattern = r"([А-Я][а-я]+)(,| )([А-Я][а-я]+)(,| )([А-Я][а-я]+)*,*([А-Я]+[а-я]*)*,*([А-Яа-яc –]+)*,*(\+7|8)* *\(*(\d{3})?\)* *-*(\d{3})?-?(\d{2})?-?(\d{2})?,? ?\(?(доб)*\.? *(\d{4})?\)?,(\w+.?\w+?@\w+.\w+)?"

    for line in contacts_list:
        res = re.search(pattern, ",".join(line))
        new_line = []
        for i in range(len(res.groups())+1):
            if i in [1, 3, 5, 6, 7, 15]:
                r = res.group(i) if res.group(i) else ''
                new_line.append(r)
            elif i == 9:
                if res.group(i):
                    code = res.group(i)
                    nnn1 = res.group(i+1)
                    nn2 = res.group(i+2)
                    nn3 = res.group(i+3)
                    phone = '+7(' + code + ')' + nnn1 + '-' + nn2 + '-' + nn3
                    if res.group(i+4):
                        ext = res.group(i+4)
                        nnnn = res.group(i+5)
                        phone += ' ' + ext + '.' + nnnn
                    new_line.append(phone)
                else:
                    new_line.append('')
        result.append(new_line)

    dup_fam = {}
    for row in range(1, len(result)-1):
        count = []
        for i in range(row+1, len(result)):
            if (result[row][0] == result[i][0]
                    and result[row][1] == result[i][1]):
                count.append(row)
                count.append(i)
        if count:
            dup_fam.setdefault(result[row][0], list(set(count)))

    for lines_to_merge in reversed(dup_fam.values()):
        lines_to_merge.sort()
        for ind in range(len(lines_to_merge)-1):
            line_index = lines_to_merge[ind]
            for i in range(len(result[line_index])):
                line = result[line_index]
                if result[lines_to_merge[ind]][i] == '':
                    result[lines_to_merge[ind]][i] = result[lines_to_merge[ind+1]][i]
        for dup_index in reversed(lines_to_merge[1:]):
            result.pop(dup_index)

    print(*result, sep='\n')

    # код для записи файла в формате CSV
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(result)
