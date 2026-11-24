#ifndef DELEGATE_H
#define DELEGATE_H

#include <QString>
#include <QDate>

class School;
class Committee;

class Delegate
{
public:
    Delegate(
        const QString &name,
        const QString &surname,
        const QDate &dateOfBirth,
        const QString &gender,
        School *school,
        Committee *committee
        );

    QString getName() const;
    void setName(const QString &name);

    QString getSurname() const;
    void setSurname(const QString &surname);

    QDate getDateOfBirth() const;
    void setDateOfBirth(const QDate &dateOfBirth);

    QString getGender() const;
    void setGender(const QString &gender);

    School *getSchool() const;
    bool setSchool(School *school);

    Committee *getCommittee() const;
    bool setCommittee(Committee *committee);

    int getId() const;
    void setId(int id);

private:
    QString m_name;
    QString m_surname;
    QDate m_dateOfBirth;
    QString m_gender;
    School *m_school;
    Committee *m_committee;
    int m_id;
};

#endif // DELEGATE_H
