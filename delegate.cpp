#include "delegate.h"
#include "school.h"
#include "committee.h"

#include <QtGlobal>

Delegate::Delegate(const QString &name, const QString &surname, const QDate &dateOfBirth,
                   const QString &gender, School *school, Committee *committee)
    : m_name(name),
    m_surname(surname),
    m_dateOfBirth(dateOfBirth),
    m_gender(gender),
    m_school(school),
    m_committee(committee),
    m_id(-1) // Garbage id
{
    Q_ASSERT(school != nullptr);
    Q_ASSERT(committee != nullptr);
}

QString Delegate::getName() const
{
    return m_name;
}

void Delegate::setName(const QString &name)
{
    m_name = name;
}

QString Delegate::getSurname() const
{
    return m_surname;
}

void Delegate::setSurname(const QString &surname)
{
    m_surname = surname;
}

QDate Delegate::getDateOfBirth() const
{
    return m_dateOfBirth;
}

void Delegate::setDateOfBirth(const QDate &dateOfBirth)
{
    m_dateOfBirth = dateOfBirth;
}

QString Delegate::getGender() const
{
    return m_gender;
}

void Delegate::setGender(const QString &gender)
{
    m_gender = gender;
}

School *Delegate::getSchool() const
{
    return m_school;
}

bool Delegate::setSchool(School *school)
{
    if(school == nullptr)
        return false;
    m_school = school;
    return true;
}

Committee *Delegate::getCommittee() const
{
    return m_committee;
}

bool Delegate::setCommittee(Committee *committee)
{
    if(committee == nullptr)
        return false;
    m_committee = committee;
    return true;
}


int Delegate::getId() const
{
    return m_id;
}

void Delegate::setId(int id)
{
    m_id = id;
}
