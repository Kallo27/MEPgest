#include "gamanager.h"

#include <algorithm>

GAmanager::GAmanager(QObject *parent)
    : QObject{parent}
{}

GAmanager::~GAmanager()
{
    qDeleteAll(m_schools);
    qDeleteAll(m_committees);
    qDeleteAll(m_delegates);
}

const QList<School *> &GAmanager::getSchools() const
{
    return m_schools;
}

const QList<Committee *> &GAmanager::getCommittees() const
{
    return m_committees;
}

const QList<Delegate *> &GAmanager::getDelegates() const
{
    return m_delegates;
}

School *GAmanager::findSchool(const QString &schoolName)
{
    for(School *school : std::as_const(m_schools)){
        if(QString::compare(school->getName(), schoolName, Qt::CaseInsensitive) == 0)
            return school;
    }

    School *newSchool = new School(schoolName);
    m_schools.append(newSchool);
    qInfo() << "New school added:" << schoolName;
    return newSchool;
}

Committee *GAmanager::findCommittee(const QString &committeeName)
{
    for(Committee *committee : std::as_const(m_committees)){
        if(QString::compare(committee->getName(), committeeName, Qt::CaseInsensitive) == 0)
            return committee;
    }

    Committee *newCommittee = new Committee(committeeName);
    m_committees.append(newCommittee);
    qInfo() << "New Committee added" << committeeName;
    return newCommittee;
}

QStringList GAmanager::parseCsvLine(const QString &line, QChar delimiter)
{
    QStringList fields;
    QString current;
    bool inQuotes = false;

    for (int i = 0; i < line.size(); ++i) {
        const QChar c = line[i];

        if (c == '"') {
            if(inQuotes && i + 1 < line.size() && line[i + 1] == '"'){
                current.append('"');
                ++i;
            } else {
                inQuotes = !inQuotes;
            }
        }
        else if (c == delimiter && !inQuotes) {
            fields.append(current);
            current.clear();
        }
        else {
            current.append(c);
        }
    }

    fields.append(current);
    return fields;
}


bool GAmanager::loadFromCSV(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qWarning() << "Cannot open" << filePath;
        return false;
    }

    QTextStream in(&file);
    in.setEncoding(QStringConverter::Utf8);

    // 1) Header: find the columns by name
    QStringList header = parseCsvLine(in.readLine());
    for(QString &h : header)
        h = h.trimmed();

    const int colName    = header.indexOf("Nome");
    const int colSurname = header.indexOf("Cognome");
    const int colBirth = header.indexOf("Data di nascita");
    const int colGender = header.indexOf("Genere");
    const int colSchool = header.indexOf("Scuola");
    const int colCommittee = header.indexOf("Commissione");

    const QList<QPair<QString, int>> required = {
        {"Nome", colName},
        {"Cognome", colSurname},
        {"Data di nascita", colBirth},
        {"Genere", colGender},
        {"Scuola", colSchool},
        {"Commissione", colCommittee},
    };

    for (const auto &col : required) {
        if (col.second == -1) {
            qWarning() << "Missing column:" << col.first;
            return false;
        }
    }

    const int maxCol = std::max({colName, colSurname, colBirth, colGender, colSchool, colCommittee});

    // 2) Rows
    int lineNumber = 1;
    while (!in.atEnd()) {
        ++lineNumber;
        const QString line = in.readLine();
        if (line.trimmed().isEmpty())
            continue;

        const QStringList f = parseCsvLine(line);
        if(f.size() <= maxCol) {
            qWarning() << "Line" << lineNumber << "is missing at least one column";
            continue;
        }

        const QString name = f[colName].trimmed();
        const QString surname = f[colSurname].trimmed();
        const QString birth = f[colBirth].trimmed();
        const QString gender = f[colGender].trimmed();
        const QString schoolName = f[colSchool].trimmed();
        const QString committeeName = f[colCommittee].trimmed();

        const QDate dateOfBirth = QDate::fromString(birth, "d/M/yyyy");
        if(!dateOfBirth.isValid()) {
            qWarning() << "Delegate at line " << lineNumber << "has a wrong date format";
            continue;
        }

        if(name.isEmpty() || surname.isEmpty() || gender.isEmpty() || schoolName.isEmpty() || committeeName.isEmpty()){
            qWarning() << "Delegate at line " << lineNumber << "is missing one field";
            continue;
        }

        School *school = findSchool(schoolName);
        Committee *committee = findCommittee(committeeName);

        Delegate *newDelegate = new Delegate(name, surname, dateOfBirth, gender, school, committee);
        m_delegates.append(newDelegate);
    }

    sortAll();
    createIds();
    return true;
}
