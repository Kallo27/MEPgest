#include "committee.h"

Committee::Committee(const QString &name)
    : m_name(name),
    m_id(-1),
    m_score(0)
{
}

QString Committee::getName() const
{
    return m_name;
}

void Committee::setName(const QString &name)
{
    m_name = name;
}

int Committee::getId() const
{
    return m_id;
}

void Committee::setId(int id)
{
    m_id = id;
}

int Committee::getScore() const
{
    return m_score;
}

void Committee::setScore(int score)
{
    m_score = score;
}
