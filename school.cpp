#include "school.h"

School::School(const QString &name)
    : m_name(name),
    m_id(-1),
    m_score(0)
{
}

QString School::getName() const
{
    return m_name;
}

void School::setName(const QString &name)
{
    m_name = name;
}

int School::getId() const
{
    return m_id;
}

void School::setId(int id)
{
    m_id = id;
}

int School::getScore() const
{
    return m_score;
}

void School::setScore(int score)
{
    m_score = score;
}
