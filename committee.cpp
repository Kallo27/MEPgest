#include "committee.h"
#include <qdebug.h>

Committee::Committee(const QString &name)
    : m_name(name),
    m_id(-1),
    m_score(0)
{
    bool ok = false;
    const int number = name.section(' ', 0, 0).toInt(&ok);
    if (ok)
        m_id = number;
    else
        qWarning() << "Committee name has no leading number:" << name;
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
