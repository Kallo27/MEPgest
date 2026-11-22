#include "delegate.h"
#include "school.h"
#include "committee.h"

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
    // Set delegate id autmoatically
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

void Delegate::setSchool(School *school)
{
    m_school = school;
}

Committee *Delegate::getCommittee() const
{
    return m_committee;
}

void Delegate::setCommittee(Committee *committee)
{
    m_committee = committee;
}

int Delegate::getId() const
{
    return m_id;
}

void Delegate::setId(const int &id)
{
    m_id = id;
}
