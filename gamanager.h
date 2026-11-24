#ifndef GAMANAGER_H
#define GAMANAGER_H

#include <QObject>
#include <QList>
#include <QString>
#include <QFile>

#include "school.h"
#include "committee.h"
#include "delegate.h"

class GAmanager : public QObject
{
    Q_OBJECT

public:
    explicit GAmanager(QObject *parent = nullptr);
    ~GAmanager();

    bool loadFromCSV(const QString &filePath);
    const QList<School*> &getSchools() const;
    const QList<Committee*> &getCommittees() const;
    const QList<Delegate*> &getDelegates() const;

private:
    QList<School*> m_schools;
    QList<Committee*> m_committees;
    QList<Delegate*> m_delegates;

    School* findSchool(const QString &schoolName);
    Committee* findCommittee(const QString &committeeName);

    static QStringList parseCsvLine(const QString &line, QChar delimiter = ',');

    void sortAll();
    void createIds();

signals:
};

#endif // GAMANAGER_H
