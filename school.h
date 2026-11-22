#ifndef SCHOOL_H
#define SCHOOL_H

#include <QString>

class School
{
    friend class GA_manager;

private:
    QString m_name;
    int m_id;
    int m_score;

    void setId(int id);
    void setScore(int score);

public:
    School(const QString &name);

    QString getName() const;
    void setName(const QString &name);

    int getId() const;
    int getScore() const;
};

#endif // SCHOOL_H
